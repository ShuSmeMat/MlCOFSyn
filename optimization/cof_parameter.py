import sys
import re
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QDialog, QMessageBox
from PyQt5.QtGui import QFont

class ParameterUI(QDialog):  # 修改为继承 QDialog
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Modify Parameters")  # Set the window title
        self.setGeometry(300, 300, 400, 300)

        # Default values from cof_function.h
        self.kbf1 = 0.40667
        self.kbf2 = 1210.7
        self.kbf3 = 20361.1
        self.d = 0.346
        self.S = 1
        self.kappa = 3.897

        # Set up UI elements
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Add a bold label at the top
        header_label = QLabel("Modify COF parameters")
        font = QFont()
        font.setBold(True)
        header_label.setFont(font)

        # Create input fields with placeholder text set to default values
        self.kbf1_input = QLineEdit()
        self.kbf1_input.setPlaceholderText(str(self.kbf1))  # Set placeholder for kbf1
        self.kbf1_input.setText("")  # Clear text to simulate editable input

        self.kbf2_input = QLineEdit()
        self.kbf2_input.setPlaceholderText(str(self.kbf2))  # Set placeholder for kbf2
        self.kbf2_input.setText("")  # Clear text to simulate editable input

        self.kbf3_input = QLineEdit()
        self.kbf3_input.setPlaceholderText(str(self.kbf3))  # Set placeholder for kbf3
        self.kbf3_input.setText("")  # Clear text to simulate editable input

        self.d_input = QLineEdit()
        self.d_input.setPlaceholderText(str(self.d))  # Set placeholder for d
        self.d_input.setText("")  # Clear text to simulate editable input

        self.S_input = QLineEdit()
        self.S_input.setPlaceholderText(str(self.S))  # Set placeholder for S
        self.S_input.setText("")  # Clear text to simulate editable input

        self.kappa_input = QLineEdit()
        self.kappa_input.setPlaceholderText(str(self.kappa))  # Set placeholder for kappa
        self.kappa_input.setText("")  # Clear text to simulate editable input

        # Add the header label to the layout
        layout.addWidget(header_label)

        # Add input fields to form layout
        form_layout.addRow("kbf1:", self.kbf1_input)
        form_layout.addRow("kbf2:", self.kbf2_input)
        form_layout.addRow("kbf3:", self.kbf3_input)
        form_layout.addRow("d:", self.d_input)
        form_layout.addRow("S:", self.S_input)
        form_layout.addRow("κ:", self.kappa_input)

        # Create save button
        self.save_button = QPushButton("Save Parameters")
        self.save_button.clicked.connect(self.save_parameters)

        layout.addLayout(form_layout)
        layout.addWidget(self.save_button)

        # Set the layout
        self.setLayout(layout)

    def save_parameters(self):
        # Get the values from the input fields
        self.kbf1 = self.get_parameter_value(self.kbf1_input)
        self.kbf2 = self.get_parameter_value(self.kbf2_input)
        self.kbf3 = self.get_parameter_value(self.kbf3_input)
        self.d = self.get_parameter_value(self.d_input)
        self.S = self.get_parameter_value(self.S_input)
        self.kappa = self.get_parameter_value(self.kappa_input)

        # Save the new parameters to cof_function.h
        success = self.update_cof_function()

        # Show a message box based on success/failure
        if success:
            QMessageBox.information(self, "Success", "Parameters saved successfully!")
        else:
            QMessageBox.warning(self, "Error", "Failed to save parameters.")

    def get_parameter_value(self, input_field):
        # If the input field is empty, return the placeholder value (default value)
        return float(input_field.text()) if input_field.text() else float(input_field.placeholderText())

    def update_cof_function(self):
        # Read the existing cof_function.h content
        try:
            with open("../negen1o/cof_function.h", "r") as file:
                content = file.readlines()
        except FileNotFoundError:
            print("Error: cof_function.h not found.")
            return False  # Return False if the file is not found

        # Update the lines containing the parameters using regex
        content = self.update_parameter(content, "kbf1", self.kbf1)
        content = self.update_parameter(content, "kbf2", self.kbf2)
        content = self.update_parameter(content, "kbf3", self.kbf3)
        content = self.update_parameter(content, "d", self.d)
        content = self.update_parameter(content, "S", self.S)
        content = self.update_parameter(content, "kappa", self.kappa)

        # Write the updated content back to cof_function.h
        try:
            with open("../negen1o/cof_function.h", "w") as file:
                file.writelines(content)
        except Exception as e:
            print(f"Error writing to cof_function.h: {e}")
            return False  # Return False if there was an error writing the file

        print("cof_function.h has been updated successfully.")
        return True  # Return True if the file was successfully updated

    def update_parameter(self, content, param_name, new_value):
        # Use regular expression to match the line that defines the parameter and replace its value
        pattern = re.compile(rf"const double {param_name} = ([0-9.e+-]+);")
        new_line = f"const double {param_name} = {new_value};"
        return [pattern.sub(new_line, line) if param_name in line else line for line in content]

    def open_modify_window(self):
        # Function to open the 'cof_function.h' modification window
        modify_window = ParameterUI()  # 这里假设你已经定义了一个 ParameterUI 类用于修改参数
        modify_window.exec_()  # 使用 exec_() 启动模态窗口


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ParameterUI()
    window.show()
    sys.exit(app.exec_())
