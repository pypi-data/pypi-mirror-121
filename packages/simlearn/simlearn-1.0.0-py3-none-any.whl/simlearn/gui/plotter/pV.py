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

        self.cardinality_averaged_pressure = 0
        self.widget_guard['averaged_pressure'].hideAxis('top')

    
    def average_pressure(self):
        """
        contributing the mean of pressure by using a formular II.1 from DOI: 10.1109/CLUSTR.2009.5289161
        """
        if len(self.figures_info['averaged_pressure']['y']) == 0:
            self.figures_info['averaged_pressure']['y'].append(self.espresso_instance.pressure)
            self.cardinality_averaged_pressure = 1
        else:
            self.cardinality_averaged_pressure += 1
            new_averaged_pressure = self.figures_info['averaged_pressure']['y'][-1] + \
                                    (self.figures_info['pressure']['y'][-1] -
                                     self.figures_info['averaged_pressure']['y'][-1]) / (
                                        self.cardinality_averaged_pressure)
            self.figures_info['averaged_pressure']['y'].append(new_averaged_pressure)

            self.widget_guard['averaged_pressure'].setLabel('top', f'{new_averaged_pressure:.5f}')
    
    def delete_averages(self):
        print("previous averaged pressure values are deleted")
        self.figures_info['averaged_pressure']['x'] = []
        self.figures_info['averaged_pressure']['y'] = []
        self.cardinality_averaged_pressure = 0

