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
from collections import defaultdict
from typing      import Dict

from PyQt5.QtWidgets           import QApplication
from .ui.star                  import Ui_mainWindow
from .espresso_scripts.estar   import EStars
# from espresso_scripts.EBuckyBallClass import EBuckyBallClass as EStarsClass
from .plotter.star              import Plotter

from .bot import Bot

class MainWindow(Bot):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.__version__:   str  = "0.0.3"
        self.internal_name: str  = "Stars"
        self.figures_info: Dict  = dict(
            total_energy=defaultdict(list, {t: [v] for t, v in zip(*[iter([
                'label', 'Total Energy',
                'title', '',
                'xlabel', 'Time',
                'ylabel', 'Total Energy in kJ/mol'])] * 2)}),
            kinetic_energy=defaultdict(list, {t: [v] for t, v in zip(*[iter([
                'label', 'Kinetic Energy',
                'title', '',
                'xlabel', 'Time',
                'ylabel', 'Kinetic Energy in kJ/mol'])] * 2)}),
            potential_energy=defaultdict(list, {t: [v] for t, v in zip(*[iter([
                'label', 'Potential Energy',
                'title', '',
                'xlabel', 'Time',
                'ylabel', 'Potential Energy in kJ/mol'])] * 2)}),
        )

        self.setup_window(Ui_mainWindow, self.figures_info, plotter=Plotter)

    def system_check(self):
        self.get_parameter()
        self.create_system(espresso_class=EStars)

    def update_parameters(self):
        self.espresso_instance.turn_on_interactions()
        self.espresso_instance.toggle_gravity()
        self.espresso_instance.set_langevin()
        self.espresso_instance.visualizer.specs['particle_sizes'] = [self.espresso_instance.simulation_parameters_dict['value_sigma'] / 2]

    def get_parameter(self):
        self.simulation_parameters_dict = dict(
            system_name           = str(self.uim.particles_system_name.text()),
            number_particle       = int(self.uim.particles_np.text()),
            arm_number            = int(self.uim.arms_np.text()),
            box_length            = self.uim.box_length_auto.text().split(','),
            temperature           = int(self.uim.temperature_change.text()),
            espresso_time_step    = int(self.uim.espresso_time_step.text()),
            gravity_check         = self.uim.gravity_check.text(),
            check_savingdata      = self.uim.check_savingdata.isChecked(),
            check_savingpositions = self.uim.save_xyz.isChecked(),
            check_savingenergy    = self.uim.save_energies.isChecked(),
            check_savingpressure  = self.uim.save_pressure.isChecked(),
            input_directory       = self.uim.input_directory.text(),
            gravity_slider        = float(self.uim.gravity_slide.value()),
            gravity_value         = float(self.uim.grav_red_unit.value()),
            value_epsilon         = float(self.uim.value_epsilon.text()),
            value_sigma           = float(self.uim.value_sigma.text()),
            thermostat_check      = self.uim.thermostat_check.isChecked(),
            periodic_x_check      = self.uim.periodic_x_check.isChecked(),
            periodic_y_check      = self.uim.periodic_y_check.isChecked(),
            periodic_z_check      = self.uim.periodic_z_check.isChecked(),
            skin                  = float(0.4*self.uim.value_sigma.value()),
            cut_off               = 5.5  # hardcoded?
        )

    def set_parameters(self):
        self.get_parameter()

        if self.espresso_instance:

            self.uim.apply_changes.setText("Working...")
            self.uim.centralwidget.repaint()

            self.espresso_instance.time_steps_per_frame = int(self.uim.espresso_time_step.text())
            self.espresso_instance.simulation_parameters_dict['thermostat_check'] = self.uim.thermostat_check.isChecked()
            self.espresso_instance.simulation_parameters_dict['temperature'] = int(self.uim.temperature_change.text())
            self.espresso_instance.simulation_parameters_dict['value_epsilon'] = float(self.uim.value_epsilon.text())
            self.espresso_instance.simulation_parameters_dict['wanted_sigma'] = float(self.uim.value_sigma.text())
            self.espresso_instance.simulation_parameters_dict['gravity_check'] = self.uim.gravity_check.isChecked()
            self.espresso_instance.simulation_parameters_dict['gravity_value'] = self.uim.grav_red_unit.value()
            self.espresso_instance.simulation_parameters_dict['periodic_x_check'] = self.uim.periodic_x_check.isChecked()
            self.espresso_instance.simulation_parameters_dict['periodic_y_check'] = self.uim.periodic_y_check.isChecked()
            self.espresso_instance.simulation_parameters_dict['periodic_z_check'] = self.uim.periodic_z_check.isChecked()

            self.change_sigma(wanted_sigma=self.espresso_instance.simulation_parameters_dict['wanted_sigma'])
            self.uim.value_sigma.setProperty("value", self.espresso_instance.simulation_parameters_dict['value_sigma'])
            self.uim.apply_changes.setText("Apply")

            print(
                "[set_parameters]\n"
                "Visualization step changed to: {0} \n"
                "             Thermostat is on: {1} \n"
                "       Temperature changed to: {2} \n"
                "           Epsilon changed to: {3} \n"
                "             Sigma changed to: {4} \n"
                "                   Gravity is: {5} \n"
                "   Gravity value in red. unit: {6} \n".format(
                    int(self.uim.espresso_time_step.text()),
                    self.uim.thermostat_check.isChecked(),
                    int(self.uim.temperature_change.text()),
                    float(self.uim.value_epsilon.text()),
                    self.espresso_instance.simulation_parameters_dict['value_sigma'],
                    self.uim.gravity_check.isChecked(),
                    self.uim.grav_red_unit.value()
                )
            )
            self.update_parameters()


def run():
    app    = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    run()
