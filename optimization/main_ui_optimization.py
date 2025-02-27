from PyQt5 import QtCore, QtWidgets
import pandas as pd
import numpy as np
from bayesian import bayesian_optimization
import sys
import os
from cof_parameter import ParameterUI
from function import generate_parameter_file
class OptimizationThread(QtCore.QThread):
    result_signal = QtCore.pyqtSignal(str)
    max_value_signal = QtCore.pyqtSignal(float)
    sequence_signal = QtCore.pyqtSignal(str)  # 新增信号

    def __init__(self, conditions, conditions_file_path,csv_file_path, max_iterations, stability_threshold, num_best_conditions):
        super().__init__()
        self.conditions = conditions
        self.conditions_file_path =conditions_file_path
        self.csv_file_path = csv_file_path
        self.max_iterations = max_iterations
        self.stability_threshold = stability_threshold
        self.num_best_conditions = num_best_conditions

    def run(self):
        # 在此调用贝叶斯优化
        bayesian_optimization(
            conditions=self.conditions,
            conditions_file_path = self.conditions_file_path,
            csv_file_path=self.csv_file_path,
            max_iterations=self.max_iterations,
            stability_threshold=self.stability_threshold,
            num_best_conditions=self.num_best_conditions,
            update_result_text=self.update_result_text,
            update_max_value_text=self.update_max_value_text,
            send_sequence=self.send_sequence  # 将信号传递到 bayesian_optimization
        )

    def update_result_text(self, text):
        self.result_signal.emit(text)  # 发射信号到UI线程

    def update_max_value_text(self, value):
        self.max_value_signal.emit(value)  # 发射信号到UI线程

    def send_sequence(self, sequence_str):
        self.sequence_signal.emit(sequence_str)  # 发射信号到UI线程，显示添加序列

class BayesianApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.global_max_value = -np.inf

    def initUI(self):
        self.setWindowTitle("Bayesian Optimization GUI")
        layout = QtWidgets.QGridLayout()

        # Add the "Set COF parameters" button at the top
        self.open_parameter_ui_button = QtWidgets.QPushButton("Set COF parameters", self)
        self.open_parameter_ui_button.clicked.connect(self.open_parameter_ui)
        layout.addWidget(self.open_parameter_ui_button, 0, 0, 1, 3)  # This places the button at the top

        # ------------------ Monomer Concentration Field ------------------
        self.MonomerCoreConcentrationLabel = QtWidgets.QLabel("Monomer (core) Concentration (mol/L):", self)
        self.monomer_core_concentration_entry = QtWidgets.QLineEdit(self)
        self.monomer_core_concentration_entry.setPlaceholderText("0.002")
        layout.addWidget(self.MonomerCoreConcentrationLabel, 1, 0)
        layout.addWidget(self.monomer_core_concentration_entry, 1, 1)

        # Save Button for Monomer Concentration
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
        self.stability_entry.setPlaceholderText("Please enter the maximum value without changing times")
        layout.addWidget(QtWidgets.QLabel("No-improvement Criterion:"), 5, 0)
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

        # Load Pre-trained Data
        layout.addWidget(QtWidgets.QLabel("Load Pre-trained Data:"), 8, 0)
        self.csv_path_entry = QtWidgets.QLineEdit(self)
        layout.addWidget(self.csv_path_entry, 8, 1)
        self.load_csv_button = QtWidgets.QPushButton("Load CSV", self)
        self.load_csv_button.clicked.connect(self.load_csv)
        layout.addWidget(self.load_csv_button, 8, 2)

        # Start Button
        self.start_button = QtWidgets.QPushButton("Start Bayesian Optimization", self)
        self.start_button.clicked.connect(self.start_optimization)
        layout.addWidget(self.start_button, 9, 1)

        # Result Display
        self.result_text = QtWidgets.QTextEdit(self)
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text, 10, 0, 1, 3)

        # Global Maximum Value Display
        layout.addWidget(QtWidgets.QLabel("Maximum Q:"), 10, 3)
        self.max_value_text = QtWidgets.QLineEdit(self)
        self.max_value_text.setReadOnly(True)
        layout.addWidget(self.max_value_text, 10, 4)

        # Reset Button
        self.reset_button = QtWidgets.QPushButton("Reset", self)
        self.reset_button.clicked.connect(self.reset_parameters)
        layout.addWidget(self.reset_button, 9, 2)

        layout.addWidget(QtWidgets.QLabel("Monomer Addition Sequence Found (Maximum Q):"), 11, 0)
        self.sequence_text = QtWidgets.QLineEdit(self)
        layout.addWidget(self.sequence_text, 11, 1, 1, 3)

        self.setLayout(layout)

    def update_result_text(self, text):
        self.result_text.append(text)  # Append the text to result_text

    def open_parameter_ui(self):
        # Open ParameterUI (QDialog)
        parameter_ui = ParameterUI()  # Create instance of ParameterUI
        parameter_ui.setModal(True)  # Set it as a modal dialog
        parameter_ui.exec_()  # Execute the dialog (modal)
        self.show()  # Return to the main window after closing the dialog

    def update_sequence_text(self, sequence_str):
        self.sequence_text.setText(sequence_str)

    def update_max_value_text(self, value):
        self.max_value_text.setText(str(value))

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
        self.lock_button.setDisabled(True)
        self.load_conditions_button.setDisabled(True)
        self.unlock_button.setEnabled(True)

    def unlock_parameters(self):
        self.conditions_path_entry.setDisabled(False)
        self.iterations_entry.setDisabled(False)
        self.stability_entry.setDisabled(False)
        self.candidates_entry.setDisabled(False)
        self.lock_button.setDisabled(False)
        self.load_conditions_button.setDisabled(False)
        self.unlock_button.setEnabled(False)
    def update_result_text(self, text):
        self.result_text.append(text)  # Append the text to result_text

    def update_max_value_text(self, value):
        self.max_value_text.setText(str(value))  # Update max value text

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

    def start_optimization(self):
        candidate_str = self.candidates_entry.text().strip() or '5'
        stability_str = self.stability_entry.text().strip()
        iteration_str = self.iterations_entry.text().strip()

        # Convert inputs to integers
        try:
            candidate = int(candidate_str)
        except ValueError:
            self.candidates_entry.setPlainText("Initial value is incorrect!")
            return
        try:
            stability = int(stability_str)
        except ValueError:
            self.stability_entry.setPlainText("Initial value is incorrect!")
            return
        try:
            iteration = int(iteration_str)
        except ValueError:
            self.iterations_entry.setPlainText("Initial value is incorrect!")
            return

        conditions_file_path = self.conditions_path_entry.text().strip()
        if not conditions_file_path or not os.path.exists(conditions_file_path):
            QtWidgets.QMessageBox.warning(self, "Error", "Invalid conditions file path!")
            return
        try:
            conditions = pd.read_csv(conditions_file_path)
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", f"Failed to load conditions file: {e}")
            return

        csv_file_path = self.csv_path_entry.text().strip()
        if not csv_file_path or not os.path.exists(csv_file_path):
            if not csv_file_path and os.path.exists('pre_data.csv'):
                os.remove('pre_data.csv')  # 删除文件

                # 设置 csv_file_path 为默认路径
            csv_file_path = 'pre_data.csv'

        # Start the optimization in a separate thread
        self.optimization_thread = OptimizationThread(
            conditions=conditions,
            conditions_file_path = conditions_file_path,
            csv_file_path=csv_file_path,
            max_iterations=int(iteration),
            stability_threshold=int(stability),
            num_best_conditions=int(candidate)
        )

        # Connect the signals to the UI slots
        self.optimization_thread.result_signal.connect(self.update_result_text)
        self.optimization_thread.max_value_signal.connect(self.update_max_value_text)
        self.optimization_thread.sequence_signal.connect(self.update_sequence_text)
        # Start the thread
        self.optimization_thread.start()

    def reset_parameters(self):
        # Reset all input fields and values to default
        self.conditions_path_entry.clear()
        self.iterations_entry.clear()
        self.stability_entry.clear()
        self.candidates_entry.clear()
        self.csv_path_entry.clear()
        self.result_text.clear()
        self.max_value_text.clear()
        self.global_max_value = -np.inf

        self.lock_button.setDisabled(False)
        self.unlock_button.setEnabled(False)
        self.conditions_path_entry.setDisabled(False)
        self.iterations_entry.setDisabled(False)
        self.stability_entry.setDisabled(False)
        self.candidates_entry.setDisabled(False)
        self.load_conditions_button.setDisabled(False)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = BayesianApp()
    mainWin.show()
    sys.exit(app.exec_())