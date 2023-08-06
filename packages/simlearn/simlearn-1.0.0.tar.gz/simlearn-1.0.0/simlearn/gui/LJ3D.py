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
from PyQt5.QtWidgets         import QApplication
from .ui.LJ3D                import Ui_mainWindow_3D
from .espresso_scripts.eLJ3D import ELJ3D
from .LJ2D                   import MainWindow as Main2D
from .plotter.LJND           import Plotter


class MainWindow(Main2D):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.__version__: str   = "0.0.3"
        self.internal_name: str = "LJ3D"
        self.setup_window(Ui_mainWindow_3D, self.figures_info, plotter=Plotter)

    def system_check(self):
        self.get_parameter()
        self.create_system(espresso_class=ELJ3D)


def run():
    app    = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    run()
