#!/usr/bin/python

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

from .bot import Bot


class Plotter(Bot):

    def __init__(self, parent=None, GUI_instance=None, figures_info=None):
        super(Plotter, self).__init__(parent, GUI_instance, figures_info)

        self.rdf_counter = 0
        self.rdf_ = []

    
    def rdf_updater(self):
        """
        calculating the mean of rdf by using a formular II.1 from DOI: 10.1109/CLUSTR.2009.5289161
        """

        if len(self.figures_info["rdf"]['y']) == 0:
            self.figures_info["rdf"]['y'] = self.espresso_instance.rdf_y
            self.rdf_counter = 1
        else:
            self.rdf_counter += 1
            old = self.figures_info["rdf"]['y']
            new = self.espresso_instance.rdf_y
            try:
                self.figures_info["rdf"]['y'] = old + ((new - old)/self.rdf_counter)
            except ValueError:
                # print("[Plotter] THERE IS AN EXCEPTION!")
                self.figures_info["rdf"]['y'] = self.espresso_instance.rdf_y
                self.rdf_counter = 1
    
    def delete_rdf(self):
        print("previous RDF values are deleted")
        self.figures_info['rdf']['x'] = []
        self.figures_info['rdf']['y'] = []
        self.rdf_counter = 0

