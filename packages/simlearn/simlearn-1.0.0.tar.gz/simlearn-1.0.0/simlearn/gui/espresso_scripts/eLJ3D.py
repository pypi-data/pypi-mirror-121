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

from .eLJ2D import ELJ2D
from .etools import random_pos
from .etools import adaptive_position_generator
import numpy as np


class ELJ3D(ELJ2D):
    """
    LJballsClass for LJ ball task
    """

    def __init__(self, simulation_parameters_dict=None, espresso_instance=None):
        super().__init__(simulation_parameters_dict=simulation_parameters_dict, espresso_instance=espresso_instance)
        if espresso_instance:
            self.system = espresso_instance.system
            self.visualizer = espresso_instance.visualizer
        if simulation_parameters_dict: self.simulation_parameters_dict = simulation_parameters_dict
        self.internal_name = "[ELJ3D] "
        self.general_system_name = "LJ_Balls_3D"
        self.simulation_parameters_dict['can_plot'] = False

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
            TwoD=False,
            )
        for ppos in poses4particles:
            self.system.part.add(
                pos=ppos + wall_distance,
                fix=[0, 0, 0],
                # use Maxwell--Boltzmann distribution as an initial guess for the velocity
                v=np.random.normal(0, self.simulation_parameters_dict['temperature'] / self.temperature_inunit, 3),
                type=1
            )
        print("Particles positions in system:")
        print(self.system.part[:].pos)
        print("")
