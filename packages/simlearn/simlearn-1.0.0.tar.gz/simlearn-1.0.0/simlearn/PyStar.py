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

import sys
from typing          import Union
from .gui.ui.welcome import Ui_WelcomeWindow

from PyQt5.QtCore    import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QAction
from PyQt5.QtGui     import QIcon

from .gui.LJ2D import MainWindow as LJBalls2D
from .gui.LJ3D import MainWindow as LJBalls3D
from .gui.pV   import MainWindow as Worksheet3D
from .gui.star import MainWindow as Stars3D

#
try:                from espresso_scripts.secret_class import SecretClass; possibility = True
except ImportError: possibility = False

log = open(".log", "a")
sys.stdout = log
sys.stderr = log

class Storer:
    def __init__(self):
        self.data = dict()

    def put(self, what=None, name: str = None) -> None:
        self.data[name] = what

    def get(self, name: str = None):
        if name in self.data: return self.data[name]
        else: return False

    def print_all(self):
        for name in self.data:
            print("key: {}, value {}".format(name, self.data[name]))


class WelcomeWindow(QMainWindow, Ui_WelcomeWindow):
    def __init__(self):
        super().__init__()
        self.__version: str     = "1.0.0"
        self.internal_name: str = "PyStar"

        self.storer: Storer     = Storer()
        self.current_task: Union[
            LJBalls2D,
            LJBalls3D,
            Worksheet3D,
            Stars3D,
            ]                   = None
        self.setupUi(self)

        self.LJ2D_button.clicked.connect(self.start_LJ2D)
        self.LJ3D_button.clicked.connect(self.start_LJ3D)
        self.worksheet_pV_button.clicked.connect(self.start_pV)

        self.stars_button.setDisabled(True) # Stars are not stable yet.
        self.stars_button.clicked.connect(self.start_star)

        self.create_menu() # menu bar
        self.show()

    def start_LJ2D(self):
        self.current_task = LJBalls2D(self)
        self.current_task.prepare()
        self.current_task.show()

    def start_LJ3D(self):
        self.current_task = LJBalls3D(self)
        self.current_task.prepare()
        self.current_task.show()

    def start_pV(self):
        self.current_task = Worksheet3D(self)
        self.current_task.prepare()
        self.current_task.show()

    def start_star(self):
        self.current_task = Stars3D(self)
        self.current_task.prepare()
        self.current_task.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape: self.closeEvent(e)

    def closeEvent(self, event):
        print(f"[{self.internal_name}] exit...")
        try:                   self.storer.get("thread_worker_espresso_instance").stop()
        except AttributeError: sys.exit(0)

    def create_action(self, text, slot=None, shortcut=None, icon=None, tip=None, checkable=False):
        action = QAction(text, self)
        if icon is not None:     action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None: action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:     action.triggered.connect(slot)
        if checkable: action.setCheckable(True)
        return action

    def add_actions(self, target, actions):
        for action in actions:
            if action is None: target.addSeparator()
            else:              target.addAction(action)

    def create_menu(self):
        self.help_menu = self.menuBar().addMenu("&Help")
        about_action  = self.create_action("&About", shortcut='F1', slot=self.on_about, tip='About the PyStar')
        secret_action = self.create_action("Secret", shortcut='F5', slot=self.secret,   tip='')
        self.add_actions(self.help_menu, (about_action,))
        self.add_actions(self, (secret_action,))

    def on_about(self):
        msg = f"""
PyStar is a user-friendly application for anyone who would like to learn simulations.
Explore and enjoy.

Version: {self.__version}
For details, please, contact us:
    https://gitlab.com/alexander.d.kazakov/pystar
"""
        QMessageBox.about(self, "About the PyStar", msg.strip())

    def secret(self):
        if possibility:
            self.simulation_running = True
            self.get_parameter()
            self.simulation_object = SecretClass(box_length=[40, 20, 2])
            self.start_loop()
        else: print("Sorry. Not ready.")


def run():
    app    = QApplication(sys.argv)
    window = WelcomeWindow()
    window.show()
    app.exec_()

if __name__ == '__main__':
    run()
