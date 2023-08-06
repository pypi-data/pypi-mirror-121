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
from typing                  import Dict
from collections             import defaultdict
from PyQt5.QtWidgets         import QApplication
from .ui.LJ2D                import Ui_mainWindow as Ui_mainWindow_2D
from .espresso_scripts.eLJ2D import ELJ2D
from .bot                    import Bot
from .plotter.LJND           import Plotter

class MainWindow(Bot):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.__version__: str   = "0.0.3"
        self.internal_name: str = "LJ2D"

        self.figures_info: Dict = dict(
            total_energy=defaultdict(list, {t: [v] for t, v in zip(*[iter([
                'label', 'Total Energy',
                'title', '',
                'xlabel', 'Time',
                'ylabel', 'Total Energy [kJ/mol]'])] * 2)}),
            kinetic_energy=defaultdict(list, {t: [v] for t, v in zip(*[iter([
                'label', 'Kinetic Energy',
                'title', '',
                'xlabel', 'Time',
                'ylabel', 'Kinetic Energy [kJ/mol]'])] * 2)}),
            potential_energy=defaultdict(list, {t: [v] for t, v in zip(*[iter([
                'label', 'Potential Energy',
                'title', '',
                'xlabel', 'Time',
                'ylabel', 'Potential Energy [kJ/mol]'])] * 2)}),
            pressure=defaultdict(list, {t: [v] for t, v in zip(*[iter([
                'label', 'Pressure',
                'title', '',
                'xlabel', 'Time',
                'ylabel', 'Pressure [Bar]'])] * 2)}),
            rdf=defaultdict(list, {t: [v] for t, v in zip(*[iter([
                'label', 'Radial Distribution Function',
                'title', '',
                'xlabel', 'r',
                'ylabel', 'g(r)'])] * 2)}),
        )

        self.setup_window(Ui_mainWindow_2D, self.figures_info, plotter=Plotter)

    def system_check(self):
        self.get_parameter()
        self.create_system(espresso_class=ELJ2D)

def run():
    app    = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    run()
