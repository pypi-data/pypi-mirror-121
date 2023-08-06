# -*- coding: utf-8 -*-

# Copyright (C) 2010-2021 The PyStar project
#
# This file is part of PyStar.
#
# PyStar is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyStar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from typing import List
import time
import sys
import numpy as np
from threading import Thread

from espressomd                      import System
from espressomd                      import shapes
from espressomd.visualization_opengl import openGLLive
import espressomd.constraints

from .etools import save_particle_positions, save_energy, save_pressure, \
    prepare_output_energy, prepare_output_pressure, dir_init



import itertools
spinner = itertools.cycle(['-', '/', '|', '\\'])

SLEEP_1s = 1
SLEEP_100ms = 0.1
SLEEP_500ms = 0.5


class EBot:
    """
    Bot class for subclass inheritance
    """

    def __init__(self, simulation_parameters_dict=None, espresso_instance=None):

        self.internal_name              = "EBOT"
        self.simulation_parameters_dict = simulation_parameters_dict
        self.first_task                 = True
        self.simulation_seed            = 42
        self.visualizer                 = None

        self.time_steps_per_frame       = self.simulation_parameters_dict['espresso_time_step']
        self.warming_settings           = dict(warm_steps=10, max_steps=1000, energy_accuracy=1e-4)

        if not espresso_instance:
            print(f"{self.internal_name} creating a system...")
            self.system = System(box_l=[float(self.simulation_parameters_dict['box_length'][0]),
                                        float(self.simulation_parameters_dict['box_length'][1]),
                                        float(self.simulation_parameters_dict['box_length'][2])])
        else:
            self.system     = espresso_instance.system
            self.visualizer = espresso_instance.visualizer
        
        self.fene = None
        # By default, use the n_square cell list. It is the most robust
        self.system.cell_system.set_n_square(use_verlet_lists=False)
        self.system.cell_system.skin = self.simulation_parameters_dict['skin']  # Not sure
        self.system.seed = self.simulation_seed
        np.random.seed(self.simulation_seed)
        self.system.time_step = 0.001

        self.saving_data_path     = None
        self.pause_button_pressed = False
        self.stopSimulation       = False
        self.time_simulation      = None

        self.total_energy         = None
        self.kinetic_energy       = None
        self.pressure             = None
        self.instance_gravity     = None
        self.gravity_inside       = False
        self.atom_mass            = 1.660539040 * 1e-27  # kg
        self.k_boltzmann          = 1.380649 * 1e-23  # J/K
        self.temperature_inunit   = 298  # K # measure of energy in KT with T=previous value
        self.temperature          = None

        self.integrator_nsteps    = 1

        self.integrator_thread    = None
        print(f"{self.internal_name} initialized!")

    def change_volume_box(self, target_ls: List[float]) -> None:
        print('change_volume to the size L = ', target_ls)
        axis = ['x', 'y', 'z']
        for i in range(3):
            box_l = self.system.box_l[i]
            target_l = target_ls[i]
            ax = axis[i]
            while box_l != target_l:
                if target_l < box_l:
                    # print('compression to box_l = ', box_l)
                    box_l = box_l * 0.95
                    if target_l > box_l: box_l = target_l
                else:
                    # print('blowing up to box_l = ', box_l)
                    box_l = box_l * 1.05
                    if box_l > target_l: box_l = target_l
                self.system.change_volume_and_rescale_particles(d_new=box_l, dir=ax)
                self.system.integrator.run(500)
                # print('box_l = ', box_l)
        print('volume change done')

    def make_walls(self) -> None:
        """
        It makes 6 walls for simulation box
        :return:
        """
        print(f"{self.internal_name} making walls...")
        penetrable: bool = False
        wtype: int       = 0
        dist: float      = 0.0001

        if not self.simulation_parameters_dict['periodic_x_check']:
            self.vert1 = self.system.constraints.add(
            shape=shapes.Wall(dist=dist, normal=[1.0, 0.0, 0.0]),
            particle_type=wtype,
            penetrable=penetrable)

            self.vert2 = self.system.constraints.add(
            shape=shapes.Wall(dist=-(self.system.box_l[0] - dist), normal=[-1.0, 0.0, 0.0]),
            particle_type=wtype,
            penetrable=penetrable)

        # make horizontal walls
        if not self.simulation_parameters_dict['periodic_y_check']:
            self.hori1 = self.system.constraints.add(
            shape=shapes.Wall(dist=dist, normal=[0.0, 1.0, 0.0]),
            particle_type=wtype,
            penetrable=penetrable)

            self.hori2 = self.system.constraints.add(
            shape=shapes.Wall(dist=-(self.system.box_l[1] - dist), normal=[0.0, -1.0, 0.0]),
            particle_type=wtype,
            penetrable=penetrable)

        # make top and bottom wall
        if not self.simulation_parameters_dict['periodic_z_check']:
            self.top = self.system.constraints.add(
            shape=shapes.Wall(dist=dist, normal=[0.0, 0.0, 1.0]),
            particle_type=wtype,
            penetrable=penetrable)

            self.bottom = self.system.constraints.add(
            shape=shapes.Wall(dist=-(self.system.box_l[2] - dist), normal=[0.0, 0.0, -1.0]),
            particle_type=wtype,
            penetrable=penetrable)

    def set_langevin(self) -> None:
        """
        Depending on the number of particles in the simulation box, we change kT and gamma parameters for
        decreasing equilibration time.
        :return:
        """
        print(f"{self.internal_name} setting up Langevin thermostat...")
        if self.simulation_parameters_dict['thermostat_check']:
            self.system.thermostat.set_langevin(
                kT    = self.simulation_parameters_dict['temperature'] / self.temperature_inunit,
                gamma = 1.,
                seed  = 42
            )
            print("Thermostat turned on")
        else:
            self.system.thermostat.turn_off()
            print("Thermostat turned off")

    def turn_on_interactions(self):
        """
        Depending on the task, please, specify the procedure in your subclasses
        """
        print("Depending on the task, please, specify the procedure in your subclasses")

    def make_structure(self):
        """
        Depending on the task, please, specify the procedure in your subclasses
        :return:
        """
        print("Depending on the task, please, specify the procedure in your subclasses")

    def init_visualizer(self) -> None:
        print(f"{self.internal_name} visualizer initialization...")
        camera = (
                np.array([0.5, 0.5, 0]) * self.system.box_l + np.array([0, 0, 2.5]) * np.amax(self.system.box_l[0:1])
        ).tolist()

        self.visualizer = openGLLive(
            self.system,
            window_size       =[600, 600], background_color=[0, 0, 0],
            camera_position   = camera,
            particle_coloring = 'node',
            draw_nodes=False, draw_cells=False,
            particle_sizes    = [0.5 * self.simulation_parameters_dict['value_sigma']],
            draw_constraints  = False,
            drag_enabled=False, rasterize_resolution=50.0, draw_bonds=True, bond_type_radius=[0.1 * self.simulation_parameters_dict['value_sigma']],
            ext_force_arrows  =False,
        )

    def set_cellsystem(self) -> None:
        """ Check the neighbour list. If the system is too small, then do not use a neighbour list """
        cell_system_state = self.system.cell_system.get_state()
        print(cell_system_state)
        try:
            max_range = cell_system_state["max_range"]
            n_cells = int(np.product((np.floor(self.system.box_l/max_range))))
            if n_cells > cell_system_state["min_num_cells"]:
                self.system.cell_system.set_domain_decomposition()
                self.system.cell_system.resort()
                print("Turning on cell system", self.system.cell_system.get_state())
            else:
                print("Do not use cell system", self.system.cell_system.get_state())
        except KeyError:
            print("No max_range")
            pass

    def prepare_simulation(self) -> None:
        self.stopSimulation: bool = False
        self.change_volume_box(target_ls=[float(self.simulation_parameters_dict['box_length'][0]),
                                          float(self.simulation_parameters_dict['box_length'][1]),
                                          float(self.simulation_parameters_dict['box_length'][2])])
        self.make_structure()
        self.turn_on_interactions()
        self.set_cellsystem()
        self.set_langevin()
        self.warmup(minimization=True, warmingup=True)
        self.simulation_parameters_dict['can_plot'] = True

    def simulate(self, continue_: bool = False) -> None:
        self.prepare_simulation()
        if not continue_: self.init_visualizer()
        self.create_thread4vi()

        if not self.stopSimulation and self.simulation_parameters_dict['check_savingdata']:
            saving_thread = Thread(target=self.save_data); saving_thread.start()

        # if not self.stopSimulation:
        #     validation_thread = Thread(target=self.position_validation); validation_thread.start()

        if not continue_: self.visualizer.start()
        self.visualizer.specs['particle_sizes'] = [self.simulation_parameters_dict['value_sigma'] / 2]

    def create_thread4vi(self) -> None:
        self.integrator_thread = Thread(target=self.visual_integrator, name="visual_integration_thread")
        print("Run integration...")
        self.integrator_thread.start()

    def visual_integrator(self) -> None:
        min_frame_time = 1.0 / 60.0
        if self.time_steps_per_frame < 1:
            min_frame_time = min_frame_time / self.time_steps_per_frame
            self.time_steps_per_frame = 1
        self.time_steps_per_frame = int(max(1, int(self.time_steps_per_frame + 0.5)))
        while not self.stopSimulation:
            if self.pause_button_pressed: time.sleep(SLEEP_100ms)
            else:
                start_time = time.time()
                self.visualizer.update()
                self.update_pointers()
                self.system.integrator.run(self.time_steps_per_frame)
                end_time = time.time()
                time_diff = end_time - start_time
                if min_frame_time > time_diff:
                    self.time2sleep = min_frame_time - time_diff
                    time.sleep(self.time2sleep)
        else:
            print("Cleaning particles...")
            self.system.part.clear()
            print("Cleaning constrains...")
            self.system.constraints.clear()

    def update_pointers(self) -> None:
        """ TODO: get rid of hardcoded constants
        returns energy and pressure in SI units
        Energy   = energy   [reduced units] * k_b * T * factor(for kJ/mol)
        Pressure = pressure [reduced units] * k_b * T * (10^-9m)^-3 * factor(for Pa to bar)
        """

        self.time_simulation = self.system.time
        self.total_energy = float(
            self.system.analysis.energy()['total'] * self.k_boltzmann * self.temperature_inunit * 6.022 * 1e+20)
        self.kinetic_energy = float(
            self.system.analysis.energy()['kinetic'] * self.k_boltzmann * self.temperature_inunit * 6.022 * 1e+20)
        self.pressure = float(
            self.system.analysis.pressure()['total'] * self.k_boltzmann * self.temperature_inunit * 1e+27 * 1e-5)
        r_bins = int((self.system.box_l[0] / 2) / (0.3 * self.simulation_parameters_dict['value_sigma']))
        self.rdf_r, self.rdf_y = self.system.analysis.rdf(rdf_type='rdf', type_list_a=[1], type_list_b=[1], r_min=0.0,
                                                          r_max=self.system.box_l[0] / 2.0, r_bins=r_bins)
        self.particles_info = list(zip(self.system.part[:].id, self.system.part[:].type, self.system.part[:].pos))

    def warmup(self, minimization: bool = True, warmingup: bool = True) -> None:
        """
        Warming up the system
        :param minimization:
        :param warmingup:
        :return:
        """
        if minimization:
            print(f"{self.internal_name} do energy minimization...")
            self.system.integrator.set_steepest_descent(f_max = 0, gamma = 1.0,
                max_displacement=0.01*self.simulation_parameters_dict['value_sigma']
            )
            continue_steepest_descent: bool = True
            old_etot: float = self.system.analysis.energy()["total"]
            n_step:   int   = self.warming_settings['warm_steps']
            i_warmup: int   = 0
            while continue_steepest_descent:
                self.system.integrator.run(n_step)
                new_etot: float = self.system.analysis.energy()["total"]
                if abs(abs(new_etot) / abs(old_etot) - 1.0) <\
                   self.warming_settings['energy_accuracy'] * n_step:
                    continue_steepest_descent = False
                old_etot = new_etot
                i_warmup += 1
                if i_warmup >= self.warming_settings['max_steps']:
                    print("Did not succeed in initializing the system (energy minimization)")
                    sys.exit(1)
            self.system.integrator.set_vv()
            print(f"{self.internal_name} Minimization done.\n")

        if warmingup:
            print(f"{self.internal_name} warming up...")
            # set LJ cap
            lj_cap: float              = 48.0 * self.simulation_parameters_dict['value_epsilon'] / self.simulation_parameters_dict['value_sigma']
            target_min_distance: float = 0.9*self.simulation_parameters_dict['value_sigma']
            self.system.force_cap = lj_cap
            warmup_complete: bool = False

            act_min_dist = self.system.analysis.min_dist()
            print(f"Start with minimal distance {act_min_dist}")
            # Warmup Integration Loop
            i_warmup: int  = 0
            while not warmup_complete:
                self.system.integrator.run(self.warming_settings['warm_steps'])
                act_min_dist: float = self.system.analysis.min_dist()
                i_warmup += 1
                check_cap = np.all(
                    np.sum(np.power(self.system.part[:].f, 2), axis=1)
                    < 0.9999 * np.power(lj_cap, 2)
                )
                check_dist = act_min_dist > target_min_distance

                if i_warmup % 20 == 0:
                    print(
                        "run {:d} at time={:f} (LJ cap={:f}):".format(i_warmup, self.system.time, lj_cap) +
                        "min dist = {}; met distance target: {}, met force target: {}".format(act_min_dist, check_dist, check_cap,)
                    )
                if check_cap and check_dist:  warmup_complete = True
                else:
                    if i_warmup >= self.warming_settings['max_steps']:
                        print("Did not succeed in initializing the system (force capping)")
                        sys.exit(1)
                    # Increase LJ cap
                    lj_cap *= 1.01
                    self.system.force_cap = lj_cap

            self.system.force_cap = 0.0
            print(
                "finished warmupt at run {:d}, time={:f} (LJ cap={:f}):".format(i_warmup, self.system.time, lj_cap) +
                "min dist = {}; met distance target: {}, met force target: {}".format(act_min_dist, check_dist, check_cap,)
            )

        print(f"{self.internal_name} Warming up is done.")

    def save_data(self) -> None:
        """
        Main function for saving data. Please, put all procedures here.
        :return:
        """
        if self.simulation_parameters_dict['input_directory']: 
            self.saving_data_path = dir_init(self, self.simulation_parameters_dict['input_directory'])
        else: 
            self.saving_data_path = dir_init(self)

        print(f"Saving data path: {self.saving_data_path}")
        if self.simulation_parameters_dict['check_savingenergy']:   prepare_output_energy(self, path=self.saving_data_path)
        if self.simulation_parameters_dict['check_savingpressure']: prepare_output_pressure(self, path=self.saving_data_path)

        while not self.stopSimulation:
            if self.pause_button_pressed: time.sleep(SLEEP_500ms)
            else:
                time.sleep(SLEEP_500ms)
                if self.simulation_parameters_dict['check_savingpositions']: save_particle_positions(self, path=self.saving_data_path)
                if self.simulation_parameters_dict['check_savingenergy']:    save_energy(self, path=self.saving_data_path)
                if self.simulation_parameters_dict['check_savingpressure']:  save_pressure(self, path=self.saving_data_path)
                print("Saving data " + next(spinner), end='\r')
        if self.stopSimulation: print("Waiting ...     ")

    def toggle_gravity(self) -> None:
        if not self.gravity_inside:
            if self.simulation_parameters_dict['gravity_check']:
                # print("Added!")
                self.gravity_value_ = self.simulation_parameters_dict['gravity_value']
                self.gravity_instance = espressomd.constraints.Gravity(g=[0., -self.gravity_value_, 0.])
                self.system.constraints.add(self.gravity_instance)
                self.gravity_inside = True
        else:
            if not self.simulation_parameters_dict['gravity_check']:
                # print("Removed!")
                self.system.constraints.remove(self.gravity_instance)
                self.gravity_inside = False
            else:
                if self.gravity_value_ != self.simulation_parameters_dict['gravity_value']:
                    # print("Updated!")
                    self.gravity_value_ = self.simulation_parameters_dict['gravity_value']
                    self.system.constraints.remove(self.gravity_instance)
                    self.gravity_instance = espressomd.constraints.Gravity(g=[0., -self.gravity_value_, 0.])
                    self.system.constraints.add(self.gravity_instance)

    ##### Technical functions.
    def position_validation(self) -> None:
        time.sleep(1)
        list_pid = []
        dims = ["x", "y", "z"]
        wall_check = np.logical_not(np.array([self.simulation_parameters_dict["periodic_" + dim + "_check"] for dim in dims]))
        for pid in self.system.part[:].id:
            if np.any(np.logical_and(wall_check,(self.system.part[pid].pos > self.system.box_l))):
                list_pid.append(pid)
        if len(list_pid) > 0:
            print("Warning! Particles are outside the box!")
            print("IDs: ", list_pid)
