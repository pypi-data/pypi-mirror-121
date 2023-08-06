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
import time
from typing import Union

from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtCore    import Qt, QThread

from .worker         import EspressoWorker
# from .plotter.bot    import Bot as Plotter

# Substitution
from .espresso_scripts.eLJ2D  import ELJ2D
from .espresso_scripts.eLJ3D  import ELJ3D
from .espresso_scripts.eOB    import EOB
from .espresso_scripts.estar  import EStars

class Bot(QMainWindow):
    def __init__(self, parent = None):
        super(Bot, self).__init__(parent)

        self.internal_name: str = "template"
        self.parent = parent
        self.parent.hide()

        self.uim                = None
        self.thread_espresso    = None
        self.worker_espresso    = None
        self.thread_plotting    = None
        self.espresso_instance  = None
        self.simulation_running: bool = False
        self.plotter            = None

    def system_check(self):    pass
    def prepare_figures(self): pass

    def setup_window(self, gui_object = None, figure_info = None, plotter = None):
        print(f"[{self.internal_name} setup GUI...]")
        self.uim = gui_object()
        self.uim.setupUi(self)
        # run button
        self.uim.run_button.clicked.connect(self.system_check)
        # pause button
        self.uim.pause_button.hide()
        self.uim.pause_button.clicked.connect(self.pause_run_simulation)
        # apply changes (e.g. in temperature)
        self.uim.apply_changes.clicked.connect(self.set_parameters)
        self.uim.select_directory.clicked.connect(self.openFileDialog)
        self.plotter = plotter(GUI_instance=self.uim, figures_info=figure_info)

    def create_system(self, espresso_class=None):
        self.simulation_running = True
        # fmt = '{:<25} | {:<15}'
        for variable in self.simulation_parameters_dict:
            print('{:<25} | {:<15}'.format(variable, str(self.simulation_parameters_dict[variable])))

        if not self.parent.storer.get(name="espresso_instance"):
            print(f"[{self.internal_name}] Creating new simulation object...")
            self.espresso_instance = espresso_class(simulation_parameters_dict=self.simulation_parameters_dict)
            self.create_thread()
        else:
            print(f"[{self.internal_name}] Object is found in [Storer] and should be passed!")
            self.get_parameter()
            self.espresso_instance = self.parent.storer.get(name="espresso_instance")
            self.worker_espresso   = self.parent.storer.get(name="thread_worker_espresso_instance")
            self.thread_espresso   = self.parent.storer.get(name="thread_espresso_instance")

            # gui_name = self.internal_name.strip("[ ]")
            self.change_substitution(gui_name=self.internal_name)
            self.espresso_instance.simulation_parameters_dict = self.simulation_parameters_dict
            self.espresso_instance.simulate(continue_=True)

            time.sleep(1)
            while not self.espresso_instance.simulation_parameters_dict['can_plot']:
                # print("sleeping>>")
                time.sleep(1)
            else:
                self.plotter.run(espresso_instance=self.espresso_instance)

        self.uim.run_button.hide()  # no need new simulation button; at least now
        self.uim.pause_button.show()

    def change_substitution(self, gui_name):
        working_class: Union[ELJ2D, ELJ3D, EOB, EStars] = None

        if   gui_name == "LJ3D":     working_class = ELJ3D
        elif gui_name == "LJ2D":     working_class = ELJ2D
        elif gui_name == "pV_curve": working_class = ELJ3D
        elif gui_name == "Stars":    working_class = EStars
        elif gui_name == "Welcome":  working_class = EOB

        else: raise Exception(f"[Error] Working class instance is undefined. Was provided: `{gui_name}`")
        self.espresso_instance = working_class(simulation_parameters_dict=self.simulation_parameters_dict, espresso_instance=self.espresso_instance)

        self.worker_espresso.espresso_instance = self.espresso_instance
        self.parent.storer.put(what=self.espresso_instance, name="espresso_instance")
        self.parent.storer.put(what=self.espresso_instance.integrator_thread, name="integrator_espresso")
        self.parent.storer.put(what=self.worker_espresso, name="thread_worker_espresso_instance")
        self.parent.storer.put(what=self.thread_espresso, name="thread_espresso_instance")

    def create_thread(self):
        self.thread_espresso = QThread()
        self.worker_espresso = EspressoWorker(espresso_instance=self.espresso_instance)

        self.worker_espresso.moveToThread(self.thread_espresso)
        self.thread_espresso.started.connect(self.worker_espresso.run)
        self.thread_espresso.start()

        time.sleep(1)
        while not self.espresso_instance.simulation_parameters_dict['can_plot']: time.sleep(1)
        else:
            self.plotter.run(self.espresso_instance)

            self.parent.storer.put(what=self.worker_espresso, name="thread_worker_espresso_instance")
            self.parent.storer.put(what=self.thread_espresso, name="thread_espresso_instance")
            self.parent.storer.put(what=self.plotter,         name="thread_plotter_instance")
            self.parent.storer.put(what=self.espresso_instance.integrator_thread, name="integrator_espresso")

    def pause_run_simulation(self):
        self.worker_espresso.toggle_pause_run()
        self.plotter.simulation_running = not self.plotter.simulation_running

        if self.plotter.simulation_running: self.uim.pause_button.setText("Pause")
        else:                               self.uim.pause_button.setText("Resume")

    def openFileDialog(self):
        directoryname = QFileDialog.getExistingDirectory(self, 'Select')
        self.uim.input_directory.setText(directoryname)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape: self.closeEvent(e)

    def closeEvent(self, event):
        try:
            self.espresso_instance.time_steps_per_frame = 2
            time.sleep(1)  # some lag for MPI issue [will be deleted/substituted in futures]
        except AttributeError: pass

        self.hide()
        self.parent.show()

        try:
            self.plotter.stop_plotting()
            self.parent.storer.put(what=self.espresso_instance, name="espresso_instance")
            self.parent.storer.put(what=self.espresso_instance.integrator_thread, name="integrator_espresso")
            self.espresso_instance.stopSimulation = True

            # TODO DEMO
            time.sleep(.1)
            self.run_demo()
        except AttributeError: pass

    def run_demo(self):
        """
        Purpose is to entertain the user in while simulating

        """

        print(f"[{self.internal_name}] go to demo...")
        self.espresso_instance.stopSimulation = False
        self.change_substitution(gui_name="Welcome")
        # self.espresso_instance.simulation_parameters_dict = self.simulation_parameters_dict # ??
        self.espresso_instance.simulate(continue_=True)

    def prepare(self):
        try:
            self.espresso_instance = self.parent.storer.get(name="espresso_instance")
            self.worker_espresso   = self.parent.storer.get(name="thread_worker_espresso_instance")
            self.thread_espresso   = self.parent.storer.get(name="thread_espresso_instance")

            self.espresso_instance.system.part.clear()
            self.espresso_instance.system.constraints.clear()
            self.espresso_instance.stopSimulation = True
        except AttributeError: pass

    def update_parameters(self):
        self.espresso_instance.turn_on_interactions()
        self.espresso_instance.toggle_gravity()
        self.espresso_instance.set_langevin()
        self.espresso_instance.visualizer.specs['particle_sizes'] = [self.espresso_instance.simulation_parameters_dict['value_sigma'] / 2]
        # self.espresso_instance.walls_updater()
        self.plotter.delete_rdf()

    def get_parameter(self):
        self.simulation_parameters_dict = dict(
            system_name           = str(self.uim.particles_system_name.text()),
            number_particle       = int(self.uim.particles_np.text()),
            density_box           = float(self.uim.particles_density.text()),
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
            cut_off               = 5.5 # hardcoded?
        )

    def set_parameters(self):
        self.get_parameter()

        if self.espresso_instance:
            self.uim.apply_changes.setText("Working...")
            self.uim.centralwidget.repaint()

            self.espresso_instance.time_steps_per_frame                           = int(self.uim.espresso_time_step.text())
            self.espresso_instance.simulation_parameters_dict['thermostat_check'] = self.uim.thermostat_check.isChecked()
            self.espresso_instance.simulation_parameters_dict['temperature']      = int(self.uim.temperature_change.text())
            self.espresso_instance.simulation_parameters_dict['value_epsilon']    = float(self.uim.value_epsilon.text())
            self.espresso_instance.simulation_parameters_dict['wanted_sigma']     = float(self.uim.value_sigma.text())
            self.espresso_instance.simulation_parameters_dict['gravity_check']    = self.uim.gravity_check.isChecked()
            self.espresso_instance.simulation_parameters_dict['gravity_value']    = self.uim.grav_red_unit.value()
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

    def change_sigma(self, wanted_sigma: float) -> None:
        '''
        Change sigma gradually taking into account time_step of simulation.
        TODO: refactoring is required
        '''

        step_increase = self.espresso_instance.system.time_step
        particle_test_forces = []
        about2crash = False
        while abs(wanted_sigma - self.espresso_instance.simulation_parameters_dict['value_sigma']) > step_increase and not about2crash:
            # time2step should be slightly higher for equilibration purpose
            time2sleep = max(self.espresso_instance.time2sleep * 3, self.espresso_instance.system.time_step * 3)
            print("[set_parameters] value_sigma: {}".format(self.espresso_instance.simulation_parameters_dict['value_sigma']))

            if wanted_sigma > self.espresso_instance.simulation_parameters_dict['value_sigma']:
                self.espresso_instance.simulation_parameters_dict['value_sigma'] += step_increase
                self.update_parameters()
                for i in range(5):
                    try:    particle_test_forces.append(self.espresso_instance.system.part[0].f[0])
                    except Exception as e: print(f"[CHANGE_SIGMA][WARNING] {e}")
                time.sleep(time2sleep)

                if max(particle_test_forces) > 200:
                    print("[set_parameters] [WARNING!] Particles experience great force... \n"
                          "                            Please, wait for a while and try again \n"
                          "                            I hope that you know what you doing!"
                          )
                    about2crash = True

            if wanted_sigma < self.espresso_instance.simulation_parameters_dict['value_sigma']:
                self.espresso_instance.simulation_parameters_dict['value_sigma'] -= step_increase
                self.update_parameters()
                time.sleep(time2sleep)

        if not about2crash:
            self.espresso_instance.simulation_parameters_dict['value_sigma'] = wanted_sigma


def run():
    app    = QApplication(sys.argv)
    window = Bot()
    window.show()
    app.exec_()


if __name__ == '__main__':
    run()
