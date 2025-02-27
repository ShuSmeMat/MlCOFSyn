import os
from PyQt5 import QtWidgets, QtCore
import sys
import pandas as pd
import numpy as np
from design_test import run_design
import io
from cof_parameter import ParameterUI
from function import generate_parameter_file
class DesignThread(QtCore.QThread):
    # 定义信号
    update_signal = QtCore.pyqtSignal(str)
    valid_count_signal = QtCore.pyqtSignal(int)
    max_value_signal = QtCore.pyqtSignal(float)  # 新增信号用于传递最大 Q 值

    def __init__(self, conditions_file_path, iteration, stability, candidates, lower, upper):
        super().__init__()
        self.conditions_file_path = conditions_file_path
        self.iteration = iteration
        self.stability = stability
        self.candidates = candidates
        self.lower = lower
        self.upper = upper

    def run(self):
        try:
            num, max_Q = run_design(
                n_initial=self.candidates,
                n_iters=self.iteration,
                design_sequence_count=self.stability,
                data_path=self.conditions_file_path,
                threshold_lower=self.lower,
                threshold_upper=self.upper,
                update_signal=self.update_signal
            )

            # 发射最终的有效序列数
            self.valid_count_signal.emit(num)
            self.max_value_signal.emit(max_Q)  # 发射最大 Q 值信号

        except Exception as e:
            self.update_signal.emit(f"Error: {str(e)}")
            num = 0
            max_Q = -np.inf
            self.valid_count_signal.emit(num)
            self.max_value_signal.emit(max_Q)


class BayesianApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.global_max_value = -np.inf
        self.valid_sequence_count = 0

    def initUI(self):
        self.setWindowTitle("Bayesian Design GUI")
        layout = QtWidgets.QGridLayout()

        # Add the "Set COF parameters" button at the top
        self.open_parameter_ui_button = QtWidgets.QPushButton("Set COF parameters", self)
        self.open_parameter_ui_button.clicked.connect(self.open_parameter_ui)
        layout.addWidget(self.open_parameter_ui_button, 0, 0, 1, 3)  # Place the button in the first row, spanning 3 columns

        # **Add Monomer (core) Concentration input field here**
        self.MonomerCoreConcentrationLabel = QtWidgets.QLabel("Monomer (core) Concentration (mol/L):", self)
        self.monomer_core_concentration_entry = QtWidgets.QLineEdit(self)
        self.monomer_core_concentration_entry.setPlaceholderText("0.002")
        layout.addWidget(self.MonomerCoreConcentrationLabel, 1, 0)
        layout.addWidget(self.monomer_core_concentration_entry, 1, 1)

        # Add "Save" button next to Monomer Concentration
        self.save_button = QtWidgets.QPushButton("Save", self)
        self.save_button.clicked.connect(self.on_start_button_click)
        layout.addWidget(self.save_button, 1, 2)

        # Input Reaction Space
        layout.addWidget(QtWidgets.QLabel("Load Monomer Addition Sequence Space File:"), 2, 0)
        self.conditions_path_entry = QtWidgets.QLineEdit(self)
        layout.addWidget(self.conditions_path_entry, 2, 1)
        self.load_conditions_button = QtWidgets.QPushButton("Browse", self)
        self.load_conditions_button.clicked.connect(self.load_conditions_file)
        layout.addWidget(self.load_conditions_button, 2, 2)

        # Termination Conditions
        layout.addWidget(QtWidgets.QLabel("Stop Conditions:"), 3, 0)

        # Total Iterations
        layout.addWidget(QtWidgets.QLabel("Maximum Number of Iterations:"), 4, 0)
        self.iterations_entry = QtWidgets.QLineEdit(self)
        self.iterations_entry.setPlaceholderText("Please enter the total number of iterations")
        layout.addWidget(self.iterations_entry, 4, 1)

        # Stability Threshold
        self.stability_entry = QtWidgets.QLineEdit(self)
        self.stability_entry.setPlaceholderText("Please enter the number of designs")
        layout.addWidget(QtWidgets.QLabel("Number of Design Sequences:"), 5, 0)
        layout.addWidget(self.stability_entry, 5, 1)

        # Candidates Per Iteration
        self.candidates_entry = QtWidgets.QLineEdit(self)
        self.candidates_entry.setPlaceholderText("5")
        self.candidates_entry.setReadOnly(True)
        layout.addWidget(QtWidgets.QLabel("Candidates Per Iteration:"), 6, 0)
        layout.addWidget(self.candidates_entry, 6, 1)

        # Lock and Unlock Buttons
        self.lock_button = QtWidgets.QPushButton("Lock Parameters", self)
        self.lock_button.clicked.connect(self.lock_parameters)
        layout.addWidget(self.lock_button, 7, 0)
        self.unlock_button = QtWidgets.QPushButton("Unlock Parameters", self)
        self.unlock_button.setEnabled(False)
        self.unlock_button.clicked.connect(self.unlock_parameters)
        layout.addWidget(self.unlock_button, 7, 1)

        # Add target Q range section
        layout.addWidget(QtWidgets.QLabel("Target Q Range:"), 8, 0)
        self.lower_bound_entry = QtWidgets.QLineEdit(self)
        self.lower_bound_entry.setPlaceholderText("Please enter the lower limit of Q")
        layout.addWidget(self.lower_bound_entry, 8, 1)
        self.upper_bound_entry = QtWidgets.QLineEdit(self)
        self.upper_bound_entry.setPlaceholderText("Please enter the upper limit of Q")
        layout.addWidget(self.upper_bound_entry, 8, 2)

        # Start Button
        self.start_button = QtWidgets.QPushButton("Start Bayesian Design", self)
        self.start_button.clicked.connect(self.start_design)
        layout.addWidget(self.start_button, 9, 1)

        # Reset Button
        self.reset_button = QtWidgets.QPushButton("Reset", self)
        self.reset_button.clicked.connect(self.reset_parameters)
        layout.addWidget(self.reset_button, 9, 2)

        # Result Display
        self.result_text = QtWidgets.QTextEdit(self)
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text, 10, 0, 1, 4)

        # Valid Sequence Count Display
        layout.addWidget(QtWidgets.QLabel("Valid Sequence Count:"), 10, 4)
        self.valid_count_text = QtWidgets.QLineEdit(self)
        self.valid_count_text.setPlaceholderText('')
        layout.addWidget(self.valid_count_text, 10, 5)

        self.setLayout(layout)


    # def update_max_value(self, max_value):
    #     # 更新最大 Q 值显示
    #     self.max_value_text.setText(str(max_value))  # 设置文本框中的值为最大 Q

    def on_start_button_click(self):
        # Get the value of Monomer Concentration from the input field
        monomer_concentration = self.monomer_core_concentration_entry.text().strip() or "0.002"  # Default to 0.002 if empty

        # Use default values for other parameters
        initial_volume = 0.0  # Default value
        time_interval = 1200  # Default value
        nuclei_concentration = 0  # Default value
        nuclei_diameter = 0  # Default value
        nuclei_height = 0  # Default value

        # Validation and generate file
        try:
            initial_volume = float(initial_volume)
            time_interval = float(time_interval)
            nuclei_concentration = float(nuclei_concentration)
            nuclei_diameter = float(nuclei_diameter)
            nuclei_height = float(nuclei_height)
            monomer_concentration = float(monomer_concentration)

            # Call the generate_parameter_file function
            generate_parameter_file(initial_volume, time_interval, nuclei_concentration, nuclei_diameter, nuclei_height,
                                    monomer_concentration)

            # Show a confirmation message after saving the concentration
            QtWidgets.QMessageBox.information(self, "Save Successful", "Monomer (core) Concentration saved successfully!")

            # After file generation, open the App window
            # self.open_app_window()

        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Please enter valid numerical values.")
            return
    def start_design(self):
        iteration_str = self.iterations_entry.text().strip()
        stability_str = self.stability_entry.text().strip()
        candidates_str = self.candidates_entry.text().strip() or '5'
        upper_str = self.upper_bound_entry.text().strip()
        lower_str = self.lower_bound_entry.text().strip()

        try:
            iteration = int(iteration_str)
            stability = int(stability_str)
            candidates = int(candidates_str)
            upper = float(upper_str)
            lower = float(lower_str)
        except ValueError:
            self.result_text.setPlainText("Incorrect input value！")
            return

        conditions_file_path = self.conditions_path_entry.text().strip()
        if not conditions_file_path or not os.path.exists(conditions_file_path):
            QtWidgets.QMessageBox.warning(self, "Error", "Invalid conditions file path!")
            return

        # Start the background thread
        self.design_thread = DesignThread(
            conditions_file_path=conditions_file_path,
            iteration=iteration,
            stability=stability,
            candidates=candidates,
            lower=lower,
            upper=upper
        )

        # Connect signals AFTER thread creation
        self.design_thread.update_signal.connect(self.update_result_text)  # 连接信号更新 UI
        self.design_thread.valid_count_signal.connect(self.update_valid_count)  # 更新 valid count
        # self.design_thread.max_value_signal.connect(self.update_max_value)  # 连接信号更新最大 Q 值

        # 启动线程
        self.design_thread.start()
    def open_parameter_ui(self):
        # Open ParameterUI (QDialog)
        parameter_ui = ParameterUI()  # Create instance of ParameterUI
        parameter_ui.setModal(True)  # Set it as a modal dialog
        parameter_ui.exec_()  # Execute the dialog (modal)
        self.show()  # Return to the main window after closing the dialog
    def update_result_text(self, new_text):
        self.result_text.append(new_text)

    def update_valid_count(self, count):
        self.valid_count_text.setText(str(count))

    def load_conditions_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Conditions File", "", "CSV Files (*.csv)")
        if file_path:
            self.conditions_path_entry.setText(file_path)

    def load_csv(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv)")
        if file_path:
            self.csv_path_entry.setText(file_path)

    def lock_parameters(self):
        self.conditions_path_entry.setDisabled(True)
        self.iterations_entry.setDisabled(True)
        self.stability_entry.setDisabled(True)
        self.candidates_entry.setDisabled(True)
        self.lower_bound_entry.setDisabled(True)
        self.upper_bound_entry.setDisabled(True)
        self.lock_button.setDisabled(True)
        self.load_conditions_button.setDisabled(True)
        self.unlock_button.setEnabled(True)

    def unlock_parameters(self):
        self.conditions_path_entry.setDisabled(False)
        self.iterations_entry.setDisabled(False)
        self.stability_entry.setDisabled(False)
        self.candidates_entry.setDisabled(False)
        self.lower_bound_entry.setDisabled(False)
        self.upper_bound_entry.setDisabled(False)
        self.lock_button.setDisabled(False)
        self.load_conditions_button.setDisabled(False)
        self.unlock_button.setEnabled(False)

    def reset_parameters(self):
        self.conditions_path_entry.clear()
        self.iterations_entry.clear()
        self.stability_entry.clear()
        self.candidates_entry.clear()
        # self.csv_path_entry.clear()
        self.lower_bound_entry.clear()
        self.upper_bound_entry.clear()
        self.result_text.clear()
        # self.max_value_text.clear()
        self.valid_count_text.clear()
        # self.global_max_value = -np.inf
        self.valid_sequence_count = 0
        self.lock_button.setDisabled(False)
        self.unlock_button.setEnabled(False)
        self.conditions_path_entry.setDisabled(False)
        self.iterations_entry.setDisabled(False)
        self.stability_entry.setDisabled(False)
        self.candidates_entry.setDisabled(False)
        self.lower_bound_entry.setDisabled(False)
        self.upper_bound_entry.setDisabled(False)
        self.load_conditions_button.setDisabled(False)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = BayesianApp()
    mainWin.show()
    sys.exit(app.exec_())
