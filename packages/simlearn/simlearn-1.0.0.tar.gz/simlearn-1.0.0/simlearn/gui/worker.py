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

from PyQt5.QtCore import QObject, pyqtSignal

class EspressoWorker(QObject):
    finished = pyqtSignal()  # our signal out to the main thread to alert it we've completed our work

    def __init__(self, espresso_instance, plotter_instance=None):
        super(EspressoWorker, self).__init__()
        self.espresso_instance = espresso_instance
        self.plotter_instance  = plotter_instance

    def run(self):
        self.espresso_instance.simulate()
        self.finished.emit()  # alert to gui that the loop stopped

    def toggle_pause_run(self):
        # TODO: convert it to explicit functions!!
        self.espresso_instance.pause_button_pressed = not self.espresso_instance.pause_button_pressed
    
    def pause_run(self):    self.espresso_instance.pause_button_pressed = True
    def continue_run(self): self.espresso_instance.pause_button_pressed = False

    def stop(self):
        # print("Termination...")
        self.espresso_instance.visualizer._quit()
        self.espresso_instance.visualizer.update()
