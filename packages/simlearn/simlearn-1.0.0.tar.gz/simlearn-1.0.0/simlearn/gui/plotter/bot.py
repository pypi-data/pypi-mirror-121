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
"""
    Plotter class is general class for plotting_init procedure in PyStar.py.
"""

from typing import Dict
import time
import numpy as np
from collections import defaultdict

from PyQt5        import QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtCore import QObject

from threading    import Thread, Event

import pyqtgraph as pg
from pyqtgraph.Qt       import QtCore, QtGui
from pyqtgraph.dockarea import *
import pyqtgraph.console


BLACK  = "#000000"
BLUE   = "#2490d2"
GREEN  = "#2d834e"
ORANGE = "#d24224"
PINK   = "#a43aa1"

def get_color(figure_info: str) -> str:
    color = "#000000"
    if figure_info == "total_energy":     color = BLACK
    if figure_info == "kinetic_energy":   color = BLUE
    if figure_info == "potential_energy": color = GREEN
    if figure_info == "pressure":         color = ORANGE
    if figure_info == "rdf":              color = PINK

    return color

class MDock(Dock):
    """
    Reduce functionality of the Dock
    """
    def __init__(self, name, area=None, size=(10, 10), widget=None, hideTitle=False, autoOrientation=True):
        Dock.__init__(self, name, area, size, widget, hideTitle, autoOrientation)
        self.label.mouseDoubleClickEvent = self.noopEvent

    def dragEventEnter(self, ev): pass
    def dragMoveEvent(self, ev):  pass
    def dragLeaveEvent(self, ev): pass
    def dragDropEvent(self, ev):  pass
    def noopEvent(self, ev):      pass

class MDockArea(DockArea):
    def dragEventEnter(self, ev): pass
    def dragMoveEvent(self, ev):  pass
    def dragLeaveEvent(self, ev): pass
    def dragDropEvent(self, ev):  pass


# Routine to acquire and serve data
def waiter4generated_data(callback, threadkill, espresso_instance):
    while not threadkill.is_set():
        data  = np.zeros(10)
        try:
            timediff = espresso_instance.time2sleep
        except AttributeError:
            timediff = 0.1
        callback(data)
        time.sleep(timediff+0.1)


class Bot(QObject):
    # Signal to indicate new data acquisition
    # Note: signals need to be defined inside a QObject class/subclass
    data_acquired = pyqtSignal(np.ndarray)

    def __init__(
        self, 
        parent             = None, 
        GUI_instance       = None, 
        figures_info: Dict = None, 
        number_samples:int = 500,
        line_width: float  = 1.5,
        ):
        
        # QObject.__init__(self, parent)
        super().__init__()

        self.line_width   = line_width
        self.data_len     = number_samples
        self.figures_info = figures_info

        self.espresso_instance  = None
        self.simulation_running = True

        # self.rdf_counter = 0
        # self.rdf_ = []

        self.curve_guard  = dict()
        self.widget_guard = dict()
        self.dock_guard   = dict()

        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        self.hbox = QtWidgets.QHBoxLayout()
        self.win = GUI_instance.life_plots

        self.area = DockArea()
        self.hbox.addWidget(self.area)

        for figure_info in self.figures_info:
            dock = Dock(self.figures_info[figure_info]['label'][0], size=(500, 200))
            self.dock_guard[figure_info] = self.area.addDock(dock)
            
            widget = pg.PlotWidget(labels = {
                'left':   self.figures_info[figure_info]['ylabel'],
                'bottom': self.figures_info[figure_info]['xlabel']
                })
            self.widget_guard[figure_info] = widget
            dock.addWidget(widget)

        self.win.setLayout(self.hbox)

    def run(self, espresso_instance=None):
        self.espresso_instance = espresso_instance

        for figure_info in self.figures_info:
            widget = self.widget_guard[figure_info]
            self.curve_guard[figure_info] = widget.plot(
                *self.data_passer(figure=figure_info), 
                pen=pg.mkPen(get_color(figure_info),  width=self.line_width)
            )

        # Connect the signal
        self.data_acquired.connect(self.update_data)

        # Make and start the background thread to acquire data
        # Pass it the signal.emit as the callback function
        self.threadkill = Event()
        thread = Thread(
            target = waiter4generated_data, 
            args   = (
                self.data_acquired.emit, 
                self.threadkill, 
                self.espresso_instance
                ), 
            name="PLOTTER_THREAD"
            )
        thread.start()

    # Kill our data acquisition thread when shutting down
    def closeEvent(self, close_event):
        self.threadkill.set()

    def stop_plotting(self):
        try: self.threadkill.set()
        except AttributeError: pass

    def data_passer(self, figure):

        if figure != "rdf":
            if len(self.figures_info[figure]['x']) > self.data_len: self.figures_info[figure]['x'].pop(0)
            if len(self.figures_info[figure]['y']) > self.data_len: self.figures_info[figure]['y'].pop(0)
            self.figures_info[figure]['x'].append(self.espresso_instance.time_simulation)

        if   figure == "total_energy":      self.figures_info[figure]['y'].append(self.espresso_instance.total_energy)
        elif figure == "kinetic_energy":    self.figures_info[figure]['y'].append(self.espresso_instance.kinetic_energy)
        elif figure == "potential_energy":  self.figures_info[figure]['y'].append(self.espresso_instance.total_energy - self.espresso_instance.kinetic_energy)
        elif figure == "pressure":          self.figures_info[figure]['y'].append(self.espresso_instance.pressure)
        elif figure == "averaged_pressure": self.average_pressure()
        elif figure == "rdf":               self.figures_info[figure]['x'] = self.espresso_instance.rdf_r; self.rdf_updater()

        return self.figures_info[figure]['x'], self.figures_info[figure]['y']

    # Slot to receive acquired data and update plot
    @pyqtSlot(np.ndarray)
    def update_data(self, data):
        if self.simulation_running:
            for figure_info in self.figures_info: self.curve_guard[figure_info].setData(*self.data_passer(figure=figure_info))
