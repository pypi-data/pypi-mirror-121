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

import numpy as np
from .ebot import EBot
from .etools import random_pos, adaptive_position_generator, dir_init


class ELJ2D(EBot):
    """
    LJballsClass for LJ ball task
    """

    def __init__(self, simulation_parameters_dict=None, espresso_instance=None):
        super().__init__(simulation_parameters_dict=simulation_parameters_dict, espresso_instance=espresso_instance)
        if espresso_instance:
            self.system = espresso_instance.system
            self.visualizer = espresso_instance.visualizer
        if simulation_parameters_dict: self.simulation_parameters_dict = simulation_parameters_dict
        else: self.simulation_parameters_dict = dict()

        self.internal_name = "[ELJ2D] "
        self.system.periodicity = [1, 1, 1]  # XYZ
        self.general_system_name = "LJ_Balls_2D"
        self.system_name = simulation_parameters_dict['system_name']
        self.path = dir_init(obj=self)
        self.simulation_parameters_dict['can_plot'] = False

    def turn_on_interactions(self) -> None:
        """
        Setting up interaction between [particles and particles] [types 1,1] and [particles and walls] [type 0, 1]
        :return:
        """
        print(self.internal_name + "turn up interactions...")
        print("sigma:", self.simulation_parameters_dict['value_sigma'])
        print("epsilon:", self.simulation_parameters_dict['value_epsilon'] / self.temperature_inunit)
        # LJ-Potential for particle-particle-interaction
        self.system.non_bonded_inter[1, 1].lennard_jones.set_params(
            epsilon=self.simulation_parameters_dict['value_epsilon'] / self.temperature_inunit,
            sigma=self.simulation_parameters_dict['value_sigma'],
            cutoff=self.simulation_parameters_dict['cut_off'] * self.simulation_parameters_dict['value_sigma'],
            shift=0)
        # WCA-Potential for particle-wall-interaction
        self.system.non_bonded_inter[0, 1].lennard_jones.set_params(
            epsilon=self.simulation_parameters_dict['value_epsilon'] / self.temperature_inunit,
            sigma=0.5 * self.simulation_parameters_dict['value_sigma'],
            cutoff=2 ** (1 / 6) * 0.5 * self.simulation_parameters_dict['value_sigma'],
            shift="auto")

    def prepare_simulation(self) -> None:
        self.stopSimulation = False
        self.change_volume_box(target_ls=[float(self.simulation_parameters_dict['box_length'][0]),
                                          float(self.simulation_parameters_dict['box_length'][1]),
                                          float(self.simulation_parameters_dict['box_length'][2])])
        self.make_walls()
        self.make_structure()
        self.turn_on_interactions()
        self.set_cellsystem()
        self.set_langevin()
        self.warmup(minimization=True, warmingup=True)
        self.simulation_parameters_dict['can_plot'] = True
        # print("###DEBUG: self.simulation_parameters_dict['can_plot']: ", self.simulation_parameters_dict['can_plot'])

    def make_structure(self) -> None:
        print(self.internal_name + "building structure...")
        print("system name: ", self.simulation_parameters_dict['system_name'])
        print("number of particles: ", self.simulation_parameters_dict['number_particle'])
        dims = ["x", "y", "z"]
        wall_distance = np.where(
            np.array([self.simulation_parameters_dict["periodic_" + dim + "_check"] for dim in dims]),
            np.zeros(3),
            (2 ** (1/6) * 0.5 * self.simulation_parameters_dict['value_sigma']) * np.ones(3)
        )
        poses4particles = adaptive_position_generator(
            function=random_pos,
            value_start=self.simulation_parameters_dict['value_sigma'],
            value_break=0.5*self.simulation_parameters_dict['value_sigma'],
            key="rmin",
            factor=0.9,
            N=self.simulation_parameters_dict['number_particle'],
            box_l=(self.system.box_l[0] - 2*wall_distance),
            TwoD=True,
            fix_z=1.0,
        )
        for ppos in poses4particles:
            self.system.part.add(
                pos=ppos + wall_distance,
                fix=[0, 0, 1],
                # use Maxwell--Boltzmann distribution as an initial guess for the velocity
                v=np.concatenate([
                    np.random.normal(0, self.simulation_parameters_dict['temperature'] / self.temperature_inunit, 2),
                    np.zeros(1)
                    ]),
                type=1
            )
        print("Particles positions in system:")
        print(self.system.part[:].pos)
        print("")
