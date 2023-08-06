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
from typing          import Dict
from collections     import defaultdict
from PyQt5.QtWidgets import QApplication, QFileDialog
from .ui.pV          import Ui_mainWindow_3D as pV_GUI
from .LJ3D           import MainWindow       as Main3D
from .plotter.pV     import Plotter

class MainWindow(Main3D):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.__version__: str   = "0.0.3"
        self.internal_name: str = "pV_curve"

        self.figures_info: Dict = dict(
            total_energy=defaultdict(list, {t: [v] for t, v in zip(*[iter([
                'label', 'Total Energy',
                'title', '',
                'xlabel', 'Time',
                'ylabel', 'Total Energy in kJ/mol'])] * 2)}),
            pressure=defaultdict(list, {t: [v] for t, v in zip(*[iter([
                'label', 'Pressure',
                'title', '',
                'xlabel', 'Time',
                'ylabel', 'Pressure in bar'])] * 2)}),
            averaged_pressure=defaultdict(list, {t: [v] for t, v in zip(*[iter([
                'label', 'Averaged Pressure',
                'title', '',
                'xlabel', 'Time',
                'ylabel', 'Averaged Pressure in bar'])] * 2)}),
        )

        self.setup_window(pV_GUI, self.figures_info, plotter=Plotter)

    def update_parameters(self):
        self.espresso_instance.turn_on_interactions()
        self.espresso_instance.set_langevin()
        self.espresso_instance.visualizer.specs['particle_sizes'] = [self.espresso_instance.simulation_parameters_dict['value_sigma'] / 2]
        self.plotter.delete_averages()

    def get_parameter(self):
        self.simulation_parameters_dict = dict(
            system_name           = str(self.uim.particles_system_name.text()),
            number_particle       = int(self.uim.particles_np.text()),
            density_box           = float(self.uim.particles_density.text()),
            box_length            = self.uim.box_length_auto.text().split(','),
            temperature           = int(self.uim.temperature_change.text()),
            espresso_time_step    = int(self.uim.espresso_time_step.text()),
            value_epsilon         = float(self.uim.value_epsilon.text()),
            value_sigma           = float(self.uim.value_sigma.text()),
            thermostat_check      = self.uim.thermostat_check.isChecked(),
            periodic_x_check      = self.uim.periodic_x_check.isChecked(),
            periodic_y_check      = self.uim.periodic_y_check.isChecked(),
            periodic_z_check      = self.uim.periodic_z_check.isChecked(),
            skin                  = float(0.4*self.uim.value_sigma.value()),
            cut_off               = 5.5,
            check_savingdata      = self.uim.check_savingdata.isChecked(),
            check_savingpositions = self.uim.save_xyz.isChecked(),
            check_savingenergy    = self.uim.save_energies.isChecked(),
            check_savingpressure  = self.uim.save_pressure.isChecked(),
            input_directory       = self.uim.input_directory.text(),
        )

    def set_parameters(self):
        if not self.espresso_instance:
            self.get_parameter()
        else:
            self.get_parameter()

            self.uim.apply_changes.setText("Working...")
            self.uim.centralwidget.repaint()

            self.espresso_instance.time_steps_per_frame = int(self.uim.espresso_time_step.text())
            self.espresso_instance.simulation_parameters_dict['temperature'] = int(self.uim.temperature_change.text())
            self.espresso_instance.simulation_parameters_dict['value_epsilon'] = float(self.uim.value_epsilon.text())
            self.espresso_instance.simulation_parameters_dict['value_sigma'] = float(self.uim.value_sigma.text())

            self.uim.apply_changes.setText("Apply")

            print(
                "[set_parameters]\n"
                "Visualization step changed to: {0} \n"
                "       Temperature changed to: {1} \n"
                "           Epsilon changed to: {2} \n"
                "             Sigma changed to: {3} \n".format(
                    int(self.uim.espresso_time_step.text()),
                    int(self.uim.temperature_change.text()),
                    float(self.uim.value_epsilon.text()),
                    self.espresso_instance.simulation_parameters_dict['value_sigma'],
                )
            )
            self.update_parameters()

def run():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    run()
