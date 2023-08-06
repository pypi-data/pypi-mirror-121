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

from .ebot import EBot

class EOB(EBot):
    """
    Like ScreenSaver. TODO: make better
    
    """

    def __init__(self, simulation_parameters_dict=None, espresso_instance=None):
        super().__init__(simulation_parameters_dict=simulation_parameters_dict, espresso_instance=espresso_instance)
        if espresso_instance:
            self.system = espresso_instance.system
            self.visualizer = espresso_instance.visualizer
        if simulation_parameters_dict: self.simulation_parameters_dict = simulation_parameters_dict

        self.time_steps_per_frame = 2
        self.internal_name = "Welcome"

    def prepare_simulation(self) -> None:
        self.stopSimulation = False
        self.change_volume_box(target_ls=[5, 5, 5])

        self.make_walls()
        self.make_structure()
        self.turn_on_interactions()
        self.set_cellsystem()
        self.system.thermostat.turn_off()
        # self.warmup(minimization=True, warmingup=True)

    def turn_on_interactions(self) -> None:
        self.system.non_bonded_inter[0, 1].lennard_jones.set_params(epsilon=1, sigma=1, cutoff=1.12, shift="auto")

    def make_structure(self) -> None:
        self.system.part.add(pos=[3, 3, 3], fix=[0, 0, 0], v=[0, 1, 1], type=1)
        self.system.part.add(pos=[1, 1, 1], fix=[0, 0, 0], v=[0, 1, 1], type=1)
        self.system.part.add(pos=[4, 4, 4], fix=[0, 0, 0], v=[0, 1, 1], type=1)

