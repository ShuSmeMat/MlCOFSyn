import os
import re
import subprocess
from tkinter import messagebox
import threading
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from cof_parameter import ParameterUI
from function import constant_sequence, arithmetic_progression, geometric_progression,generate_parameter_file,generate_addition_file
import psutil

class Worker(QtCore.QObject):
    output_signal = QtCore.pyqtSignal(str)
    error_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.processes = []  # 用于存储进程对象

    def run_batch_script(self, script_path, script_dir):
        try:
            # 使用 subprocess.Popen 来启动进程，并返回进程对象
            process = subprocess.Popen(
                ["python", script_path],
                cwd=script_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                errors='ignore'
            )
            self.processes.append(process)  # 保存进程对象

            # 实时获取标准输出和标准错误
            for line in process.stdout:
                self.output_signal.emit(line)  # 通过信号发送输出到 UI

            for err_line in process.stderr:
                self.error_signal.emit(f"error: {err_line}")  # 通过信号发送错误信息到 UI

            process.stdout.close()
            process.stderr.close()
            process.wait()

        except Exception as e:
            self.error_signal.emit(f"error:\n{str(e)}")

    def stop_processes(self):
        """停止所有进程"""
        for proc in self.processes:
            try:
                p = psutil.Process(proc.pid)
                for child in p.children(recursive=True):  # 获取所有子进程
                    child.terminate()  # 终止所有子进程
                p.terminate()  # 然后终止父进程
                p.wait(timeout=5)  # 等待最多 5 秒，看看它是否能正常退出
                print(f"Process {proc.pid} terminated.")
            except psutil.NoSuchProcess:
                print(f"Process {proc.pid} already terminated.")
            except subprocess.TimeoutExpired:
                proc.kill()  # 如果无法在 5 秒内终止，则强制终止
                print(f"Process {proc.pid} killed.")


class Ui_MainWindow(object):
    def __init__(self):
        # 初始化 worker 对象
        self.worker = Worker()
        self.process = None
    # --------------------------------------
    # setupUi方法：在MainWindow上设置各类控件
    # --------------------------------------
    def setupUi(self, MainWindow):
        # 设置窗口对象名称
        MainWindow.setObjectName("MainWindow")
        # 设置窗口大小
        MainWindow.resize(1230, 500)

        # 设置窗口图标
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("picture1.tif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)

        # 创建中央窗口部件
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # ----------------------------------
        # 创建主TabWidget：ParametersLayer
        # ----------------------------------
        self.ParametersLayer = QtWidgets.QTabWidget(self.centralwidget)
        self.ParametersLayer.setGeometry(QtCore.QRect(10, 10, 1181, 531))
        self.ParametersLayer.setObjectName("ParametersLayer")

        # ----------------------------------
        # 第1个Tab页：tab
        # ----------------------------------
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")

        # --------------------------------------------
        # 在第1个Tab页上创建 PreparationConditionsWidget
        # --------------------------------------------
        self.PreparationConditionsWidget = QtWidgets.QWidget(self.tab)
        self.PreparationConditionsWidget.setGeometry(QtCore.QRect(270, 85, 230, 300))
        self.PreparationConditionsWidget.setObjectName("PreparationConditionsWidget")

        # 为PreparationConditionsWidget设置垂直布局
        # self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.PreparationConditionsWidget)
        # self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        # self.verticalLayout_3.setObjectName("verticalLayout_3")

        # --------------------------
        # 配制条件的若干标签和编辑框
        # --------------------------
        # 序列输入 Label
        self.MonomerConcentrationLabel = QtWidgets.QLabel(self.PreparationConditionsWidget)
        self.MonomerConcentrationLabel.setObjectName("MonomerConcentrationLabel")
        self.MonomerConcentrationLabel.setGeometry(QtCore.QRect(0, 17, 225, 20))
        # self.verticalLayout_3.addWidget(self.MonomerConcentrationLabel)

        self.MonomerConcentrationLineEdit = QtWidgets.QLineEdit(self.PreparationConditionsWidget)
        self.MonomerConcentrationLineEdit.setObjectName("MonomerConcentrationLineEdit")
        # self.verticalLayout_3.addWidget(self.MonomerConcentrationLineEdit)
        self.MonomerConcentrationLineEdit.setGeometry(QtCore.QRect(0, 45, 221, 20))

        self.sequenceInputLabel = QtWidgets.QLabel(self.PreparationConditionsWidget)
        self.sequenceInputLabel.setObjectName("sequenceInputLabel")
        self.sequenceInputLabel.setGeometry(QtCore.QRect(0, 74, 190, 20))
        # self.verticalLayout_3.addWidget(self.sequenceInputLabel)

        # 序列输入框 QLineEdit
        self.sequenceInputLineEdit = QtWidgets.QLineEdit(self.PreparationConditionsWidget)
        self.sequenceInputLineEdit.setObjectName("sequenceInputLineEdit")
        self.sequenceInputLineEdit.setGeometry(QtCore.QRect(0, 102, 221, 19))
        # self.verticalLayout_3.addWidget(self.sequenceInputLineEdit)

        # 创建按钮
        self.calculateButton = QtWidgets.QPushButton("Check input", self.PreparationConditionsWidget)
        self.calculateButton.setObjectName("calculateButton")
        self.calculateButton.setGeometry(QtCore.QRect(0, 123, 221, 20))
        # self.verticalLayout_3.addWidget(self.calculateButton)

        self.NumberofAdditionsLabel = QtWidgets.QLabel(self.PreparationConditionsWidget)
        self.NumberofAdditionsLabel.setObjectName("NumberofAdditionsLabel")
        self.NumberofAdditionsLabel.setGeometry(QtCore.QRect(0, 140, 221, 19))
        # self.verticalLayout_3.addWidget(self.NumberofAdditionsLabel)

        self.NumberofAdditionsLineEdit = QtWidgets.QLineEdit(self.PreparationConditionsWidget)
        self.NumberofAdditionsLineEdit.setObjectName("NumberofAdditionsLineEdit")
        self.NumberofAdditionsLineEdit.setGeometry(QtCore.QRect(0, 160, 221, 19))
        self.NumberofAdditionsLineEdit.setReadOnly(True)
        # self.verticalLayout_3.addWidget(self.NumberofAdditionsLineEdit)

        # 连接按钮点击事件
        self.calculateButton.clicked.connect(self.calculateTotal)

        self.AddVolumeLabel = QtWidgets.QLabel(self.PreparationConditionsWidget)
        self.AddVolumeLabel.setObjectName("AddVolumeLabel")
        self.AddVolumeLabel.setGeometry(QtCore.QRect(0, 188, 221, 19))
        # self.verticalLayout_3.addWidget(self.AddVolumeLabel)

        self.AddVolumeLineEdit = QtWidgets.QLineEdit(self.PreparationConditionsWidget)
        self.AddVolumeLineEdit.setObjectName("AddVolumeLineEdit")
        self.AddVolumeLineEdit.setGeometry(QtCore.QRect(0, 215, 221, 19))
        self.AddVolumeLineEdit.setReadOnly(True)
        # self.verticalLayout_3.addWidget(self.AddVolumeLineEdit)

        # --------------------------------
        # “PreparationConditions” 文字标签
        # --------------------------------
        self.PreparationConditionsLabel = QtWidgets.QLabel(self.tab)
        self.PreparationConditionsLabel.setGeometry(QtCore.QRect(270, 70, 165, 16))
        self.PreparationConditionsLabel.setTextFormat(QtCore.Qt.AutoText)
        self.PreparationConditionsLabel.setObjectName("PreparationConditionsLabel")

        # --------------------------------------------
        # 在第1个Tab页上创建 InitialSystemWidget
        # --------------------------------------------
        self.InitialSystemWidget = QtWidgets.QWidget(self.tab)
        self.InitialSystemWidget.setGeometry(QtCore.QRect(20, 40, 221, 280))
        self.InitialSystemWidget.setObjectName("InitialSystemWidget")

        # 为InitialSystemWidget设置垂直布局
        self.verticalLayout = QtWidgets.QVBoxLayout(self.InitialSystemWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        # --------------------------
        # 初始系统的若干标签和编辑框
        # --------------------------
        self.cof_function_parameter_button = QtWidgets.QPushButton(self.InitialSystemWidget)
        self.cof_function_parameter_button.setObjectName("cof_function_parameter_button")
        self.cof_function_parameter_button.setText("Set COF parameters")


        self.verticalLayout.addWidget(self.cof_function_parameter_button)

        # 连接按钮点击事件到 open_modify_window 方法
        self.cof_function_parameter_button.clicked.connect(self.open_modify_window)

        self.InitialSystemLabel = QtWidgets.QLabel(self.tab)
        # self.InitialSystemLabel.setGeometry(QtCore.QRect(20, 20, 161, 16))
        self.InitialSystemLabel.setObjectName("InitialSystemLabel")
        self.verticalLayout.addWidget(self.InitialSystemLabel)

        self.InitialVolumeLabel = QtWidgets.QLabel(self.InitialSystemWidget)
        self.InitialVolumeLabel.setObjectName("InitialVolumeLabel")
        self.verticalLayout.addWidget(self.InitialVolumeLabel)

        self.InitialVolumeLineEdit = QtWidgets.QLineEdit(self.InitialSystemWidget)
        self.InitialVolumeLineEdit.setObjectName("InitialVolumeLineEdit")
        self.verticalLayout.addWidget(self.InitialVolumeLineEdit)

        self.InitialNucleiConcentrationLabel = QtWidgets.QLabel(self.InitialSystemWidget)
        self.InitialNucleiConcentrationLabel.setObjectName("InitialNucleiConcentrationLabel")
        self.verticalLayout.addWidget(self.InitialNucleiConcentrationLabel)

        self.InitialNucleiConcentrationLineEdit = QtWidgets.QLineEdit(self.InitialSystemWidget)
        self.InitialNucleiConcentrationLineEdit.setObjectName("InitialNucleiConcentrationLineEdit")
        self.verticalLayout.addWidget(self.InitialNucleiConcentrationLineEdit)

        self.InitialNucleiDiameterLabel = QtWidgets.QLabel(self.InitialSystemWidget)
        self.InitialNucleiDiameterLabel.setObjectName("InitialNucleiDiameterLabel")
        self.verticalLayout.addWidget(self.InitialNucleiDiameterLabel)

        self.InitialNucleiDiameterLineEdit = QtWidgets.QLineEdit(self.InitialSystemWidget)
        self.InitialNucleiDiameterLineEdit.setObjectName("InitialNucleiDiameterLineEdit")
        self.verticalLayout.addWidget(self.InitialNucleiDiameterLineEdit)

        self.InitialNucleiHeightLabel = QtWidgets.QLabel(self.InitialSystemWidget)
        self.InitialNucleiHeightLabel.setObjectName("InitialNucleiHeightLabel")
        self.verticalLayout.addWidget(self.InitialNucleiHeightLabel)

        self.InitialNucleiHeightLineEdit = QtWidgets.QLineEdit(self.InitialSystemWidget)
        self.InitialNucleiHeightLineEdit.setObjectName("InitialNucleiHeightLineEdit")
        self.verticalLayout.addWidget(self.InitialNucleiHeightLineEdit)

        # self.MonomerConcentrationLabel = QtWidgets.QLabel(self.PreparationConditionsWidget)
        # self.MonomerConcentrationLabel.setObjectName("MonomerConcentrationLabel")
        # self.verticalLayout.addWidget(self.MonomerConcentrationLabel)

        # self.MonomerConcentrationLineEdit = QtWidgets.QLineEdit(self.PreparationConditionsWidget)
        # self.MonomerConcentrationLineEdit.setObjectName("MonomerConcentrationLineEdit")
        # self.verticalLayout.addWidget(self.MonomerConcentrationLineEdit)


        # 将 InputSpecificationTextEdit 从原来的位置移动到新的 Tab 页

        # -------------------------------------------
        # 在第1个Tab页中，用于展示输入说明的文本编辑区
        # --------------------------------------------
        self.InputSpecificationTextEdit = QtWidgets.QTextEdit(self.tab)
        self.InputSpecificationTextEdit.setGeometry(QtCore.QRect(600, 40, 500, 350))
        self.InputSpecificationTextEdit.setObjectName("InputSpecificationTextEdit")

        # 将tab页加入ParametersLayer
        self.ParametersLayer.addTab(self.tab, "")

        # ----------------------------------
        # 第2个Tab页：NEgenOutput
        # ----------------------------------
        self.NEgenOutput = QtWidgets.QWidget()
        self.NEgenOutput.setObjectName("NEgenOutput")

        # 文本编辑区，用于输出NEgen1结果
        self.NEgen1OutputLabelTextEdit = QtWidgets.QTextEdit(self.NEgenOutput)
        self.NEgen1OutputLabelTextEdit.setGeometry(QtCore.QRect(20, 60, 1100, 350))
        self.NEgen1OutputLabelTextEdit.setObjectName("NEgen1OutputLabelTextEdit")

        # 标签：NEgen1 输出
        self.NEgen1OutputLabel = QtWidgets.QLabel(self.NEgenOutput)
        self.NEgen1OutputLabel.setGeometry(QtCore.QRect(20, 20, 121, 21))
        self.NEgen1OutputLabel.setObjectName("NEgen1 OutputLabel")

        # 启动按钮
        self.NEgen1StartPushButton = QtWidgets.QPushButton(self.NEgenOutput)
        self.NEgen1StartPushButton.setGeometry(QtCore.QRect(120, 20, 75, 23))
        self.NEgen1StartPushButton.setObjectName("NEgen1 StartPushButton")

        self.stop_button = QtWidgets.QPushButton(self.NEgenOutput)
        self.stop_button.setGeometry(QtCore.QRect(200, 20, 75, 23))
        self.stop_button.setObjectName("StopPushButton")
        self.stop_button.setText("Stop")
        self.stop_button.clicked.connect(self.stop_task)

        #链接函数
        self.worker.output_signal.connect(self.update_output_text)
        self.worker.error_signal.connect(self.display_error_message)
        self.NEgen1StartPushButton.clicked.connect(self.task_list_output_clicked)

        self.stop_button.clicked.connect(self.stop_task)

        # 将NEgenOutput页加入ParametersLayer
        self.ParametersLayer.addTab(self.NEgenOutput, "")

        # ----------------------------------
        # 第3个Tab页：widget
        # ----------------------------------
        self.widget = QtWidgets.QWidget()
        self.widget.setObjectName("widget")

        # 数据处理部件
        self.DataProcessingWidget = QtWidgets.QWidget(self.widget)
        self.DataProcessingWidget.setGeometry(QtCore.QRect(20, 50, 291, 300))
        self.DataProcessingWidget.setObjectName("DataProcessingWidget")

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.DataProcessingWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        # 以下为各种数据统计指标的标签与输入框
        self.QLabel_2 = QtWidgets.QLabel(self.DataProcessingWidget)
        self.QLabel_2.setObjectName("QLabel_2")
        self.verticalLayout_2.addWidget(self.QLabel_2)

        self.QLineEdit_2 = QtWidgets.QLineEdit(self.DataProcessingWidget)
        self.QLineEdit_2.setObjectName("QLineEdit_2")
        self.verticalLayout_2.addWidget(self.QLineEdit_2)

        self.RSDLabel_2 = QtWidgets.QLabel(self.DataProcessingWidget)
        self.RSDLabel_2.setObjectName("RSDLabel_2")
        self.verticalLayout_2.addWidget(self.RSDLabel_2)

        self.RSDLineEdit_2 = QtWidgets.QLineEdit(self.DataProcessingWidget)
        self.RSDLineEdit_2.setObjectName("RSDLineEdit_2")
        self.verticalLayout_2.addWidget(self.RSDLineEdit_2)

        self.LargesDiameterLabel_2 = QtWidgets.QLabel(self.DataProcessingWidget)
        self.LargesDiameterLabel_2.setObjectName("LargesDiameterLabel_2")
        self.verticalLayout_2.addWidget(self.LargesDiameterLabel_2)

        self.LargestDiameterLineEdit_2 = QtWidgets.QLineEdit(self.DataProcessingWidget)
        self.LargestDiameterLineEdit_2.setObjectName("LargestDiameterLineEdit_2")
        self.verticalLayout_2.addWidget(self.LargestDiameterLineEdit_2)

        self.AverageDiameterLabel_2 = QtWidgets.QLabel(self.DataProcessingWidget)
        self.AverageDiameterLabel_2.setObjectName("AverageDiameterLabel_2")
        self.verticalLayout_2.addWidget(self.AverageDiameterLabel_2)

        self.AverageDiameterLineEdit_2 = QtWidgets.QLineEdit(self.DataProcessingWidget)
        self.AverageDiameterLineEdit_2.setObjectName("AverageDiameterLineEdit_2")
        self.verticalLayout_2.addWidget(self.AverageDiameterLineEdit_2)

        self.DHRatioLabel = QtWidgets.QLabel(self.DataProcessingWidget)
        self.DHRatioLabel.setObjectName("DHRatioLabel")
        self.verticalLayout_2.addWidget(self.DHRatioLabel)

        self.DHRatioLineEdit = QtWidgets.QLineEdit(self.DataProcessingWidget)
        self.DHRatioLineEdit.setObjectName("DHRatioLineEdit")
        self.verticalLayout_2.addWidget(self.DHRatioLineEdit)

        # self.TotalReactionTimesLabel = QtWidgets.QLabel(self.DataProcessingWidget)
        # self.TotalReactionTimesLabel.setObjectName("TotalReactionTimesLabel")
        # self.verticalLayout_2.addWidget(self.TotalReactionTimesLabel)

        # self.TotalReactionTimesLineEdit = QtWidgets.QLineEdit(self.DataProcessingWidget)
        # self.TotalReactionTimesLineEdit.setObjectName("TotalReactionTimesLineEdit")
        # self.verticalLayout_2.addWidget(self.TotalReactionTimesLineEdit)

        # self.TotalVolumeLabel = QtWidgets.QLabel(self.DataProcessingWidget)
        # self.TotalVolumeLabel.setObjectName("TotalVolumeLabel")
        # self.verticalLayout_2.addWidget(self.TotalVolumeLabel)
        #
        # self.TotalVolumeLineEdit = QtWidgets.QLineEdit(self.DataProcessingWidget)
        # self.TotalVolumeLineEdit.setObjectName("TotalVolumeLineEdit")
        # self.verticalLayout_2.addWidget(self.TotalVolumeLineEdit)

        # self.DHRatioLabel = QtWidgets.QLabel(self.DataProcessingWidget)
        # self.DHRatioLabel.setObjectName("DHRatioLabel")
        # self.verticalLayout_2.addWidget(self.DHRatioLabel)
        #
        # self.DHRatioLineEdit = QtWidgets.QLineEdit(self.DataProcessingWidget)
        # self.DHRatioLineEdit.setObjectName("DHRatioLineEdit")
        # self.verticalLayout_2.addWidget(self.DHRatioLineEdit)

        # 直径分布图显示区域
        self.DiameterDistributionPicWidget = QtWidgets.QWidget(self.widget)
        self.DiameterDistributionPicWidget.setGeometry(QtCore.QRect(340, 10, 520, 411))
        self.DiameterDistributionPicWidget.setObjectName("DiameterDistributionPicWidget")

        self.label = QtWidgets.QLabel(self.DiameterDistributionPicWidget)
        self.label.setGeometry(QtCore.QRect(30, 0, 520, 411))
        self.label.setText("")
        # self.label.setPixmap(QtGui.QPixmap("0.5_1_10_-1_10_20.png"))
        self.label.setPixmap(QtGui.QPixmap("egf1.png"))
        self.label.setObjectName("label")

        # 直径分布图标签
        self.DiameterDistributionLabel = QtWidgets.QLabel(self.widget)
        self.DiameterDistributionLabel.setGeometry(QtCore.QRect(360, 20, 131, 16))
        self.DiameterDistributionLabel.setObjectName("DiameterDistributionLabel")

        # 数据输出按钮
        self.DataoutputPushButton = QtWidgets.QPushButton(self.widget)
        self.DataoutputPushButton.setGeometry(QtCore.QRect(20, 10, 200, 23))
        self.DataoutputPushButton.setObjectName("DataoutputPushButton")

        #数据输出链接按钮
        self.DataoutputPushButton.clicked.connect(self.data_out_clicked)

        # 将widget页加入ParametersLayer
        self.ParametersLayer.addTab(self.widget, "")

        # 设置主窗口的中心组件为centralwidget
        MainWindow.setCentralWidget(self.centralwidget)

        # 设置状态栏
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # --------------------------------------
        # 调用函数进行UI翻译等以及页面默认索引
        # --------------------------------------
        self.retranslateUi(MainWindow)
        self.ParametersLayer.setCurrentIndex(0)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        # 为按钮绑定点击事件，打开修改参数窗口

        # 在某个地方（例如点击按钮后）创建并打开窗口：
    def open_modify_window(self):
        # 创建并显示修改窗口
        modify_window = ParameterUI()  # 这里假设你已经定义了一个 ParameterUI 类用于修改参数
        modify_window.setModal(True)  # 将新窗口设置为模态
        modify_window.exec_()  # 使用 exec_() 来启动模态对话框

    def stop_task(self):
        # 调用 Worker 的 stop_processes 方法来停止进程
        if self.worker:
            self.worker.stop_processes()  # 停止所有进程
        print("UI stopped the task.")

    def closeEvent(self, event):
        # 在关闭窗口时调用 stop_task 停止进程
        self.stop_task()
        event.accept()

    def update_output_text(self, text):
        self.NEgen1OutputLabelTextEdit.append(text)

    def display_error_message(self, message):
        QMessageBox.warning(self.centralwidget, "错误", message)

    def task_list_output_clicked(self):
        initial_volume_str = self.InitialVolumeLineEdit.text().strip() or '0'
        time_interval_str = '1200'
        # time_interval_str = self.TimeIntervalLineEdit.text().strip() or '1200'
        nuclei_concentration_str = self.InitialNucleiConcentrationLineEdit.text().strip() or '0'
        nuclei_diameter_str = self.InitialNucleiDiameterLineEdit.text().strip() or '0'
        nuclei_height_str = self.InitialNucleiHeightLineEdit.text().strip() or '0'
        monomer_concentration_str = self.MonomerConcentrationLineEdit.text().strip() or '0.002'
        sequence_str = self.sequenceInputLineEdit.text().strip()

        # 输入验证
        if not sequence_str or not re.fullmatch(r'(\d+(\.\d+)?)(,\d+(\.\d+)?)*', sequence_str):
            self.sequenceInputLineEdit.setText("Please input monomer addition sequence")
            return

        # 转换数据
        try:
            sequence_numbers = [float(num) for num in sequence_str.split(',')]
            initial_volume = float(initial_volume_str)
            time_interval = float(time_interval_str)
            nuclei_concentration = float(nuclei_concentration_str)
            nuclei_diameter = float(nuclei_diameter_str)
            nuclei_height = float(nuclei_height_str)
            monomer_concentration = float(monomer_concentration_str)
            total_sum = sum(sequence_numbers)

            self.AddVolumeLineEdit.setText(str(total_sum))
        except ValueError:
            self.InitialNucleiConcentrationLineEdit.setPlainText("Incorrect input！")
            return
        self.NumberofAdditionsLineEdit.setText(str(len(sequence_numbers)))
        self.AddVolumeLineEdit.text()


        # 生成文件
        generate_parameter_file(initial_volume, time_interval, nuclei_concentration, nuclei_diameter, nuclei_height,monomer_concentration)
        generate_addition_file(sequence_str)

        # 启动子线程执行脚本
        script_dir = os.path.join(os.path.dirname(__file__), "../negen1o")
        script_path = os.path.join(script_dir, "batch_sub_cpp.py")

        # 使用线程来执行脚本
        thread = threading.Thread(target=self.worker.run_batch_script, args=(script_path, script_dir), daemon=True)
        thread.start()

    def data_out_clicked(self):
        out_dir = os.path.join(os.path.dirname(__file__), "../negen1o")
        out_path = os.path.join(out_dir, "nuc_data.py")
        all_txt_path = os.path.join(out_dir, "all.txt")
        picture_path = os.path.join(out_dir, "picture.py")
        try:
            # 如果 batch_sub_cpp.py 输出是 UTF-8，这里用 encoding='utf-8'
            data_output = subprocess.run(
                ["python", out_path],
                cwd=out_dir
            )
        except Exception as e:
            QMessageBox.warning(self, "error", f"error:\n{str(e)}")
            return

        try:
            with open(all_txt_path, 'r', encoding='utf-8') as f:
                content = f.read()
                outputs = content.split()
                self.QLineEdit_2.setText(outputs[16])
                self.RSDLineEdit_2.setText(outputs[7])
                self.LargestDiameterLineEdit_2.setText(outputs[5])
                self.AverageDiameterLineEdit_2.setText(outputs[6])
                # self.TotalReactionTimesLineEdit.setText(outputs[3])
                # self.TotalVolumeLineEdit.setText(outputs[4])
                self.DHRatioLineEdit.setText(outputs[10])



        except Exception as e:
            QMessageBox.warning(self, "error", f"Failed to read the file:\n{str(e)}")
            return

        # 启动子线程执行图片生成脚本
        thread = threading.Thread(target=self.run_picture_script, args=(picture_path, out_dir), daemon=True)
        thread.start()

    def calculateTotal(self):
        sequence_str = self.sequenceInputLineEdit.text().strip()
        if not sequence_str or not re.fullmatch(r'(\d+(\.\d+)?)(,\d+(\.\d+)?)*', sequence_str):
            self.sequenceInputLineEdit.setText("Please input monomer addition sequence")
            return

        try:
            sequence_str = self.sequenceInputLineEdit.text().strip()
            sequence_numbers = [float(num) for num in sequence_str.split(',')]
            total_sum = sum(sequence_numbers)

            self.AddVolumeLineEdit.setText(str(total_sum))
            self.NumberofAdditionsLineEdit.setText(str(len(sequence_numbers)))

        except ValueError:
            QtWidgets.QMessageBox.warning(self, "error", "请确保添加次数是一个有效的数字。")


    def run_picture_script(self, picture_path, out_dir):
        try:
            picture = subprocess.run(
                ["python", picture_path],
                cwd=out_dir,
                check=True,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore'
                 # 遇到无法解码的字符时用替代字符代替
            )
            if picture.stdout:
                image_path = picture.stdout.strip()
                image_path = image_path.replace("\\", "/")  # 替换 `\` 为 `/`
                self.label.setPixmap(QtGui.QPixmap(image_path))
            else:
                raise ValueError("No valid image path was generated")
        except Exception as e:
            # 确保这里传递的父组件是 QWidget 或 QMainWindow 的实例
            QMessageBox.warning(self.main_window, "error", f"Failed to generate the image:\n{str(e)}")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Prediction"))
        self.NumberofAdditionsLabel.setText(_translate("MainWindow", "Number of Additions"))
        self.NumberofAdditionsLineEdit.setPlaceholderText(_translate("MainWindow", "10"))
        # self.TimeIntervalLabel.setText(_translate("MainWindow", "Time Interval (s)"))
        # self.TimeIntervalLineEdit.setPlaceholderText(_translate("MainWindow", "1200.00"))
        self.MonomerConcentrationLabel.setText(_translate("MainWindow", "Monomer (core) Concentration (mol/L)"))
        self.MonomerConcentrationLineEdit.setPlaceholderText(_translate("MainWindow", "0.002"))
        self.AddVolumeLabel.setText(_translate("MainWindow", "Total Added Volume (L)"))
        self.AddVolumeLineEdit.setPlaceholderText(_translate("MainWindow", "0.01"))
        self.PreparationConditionsLabel.setText(_translate("MainWindow", "<b>Conditions to Add Monomers: </b>"))
        self.InitialVolumeLabel.setText(_translate("MainWindow", "Initial Volume (L)"))
        self.InitialVolumeLineEdit.setPlaceholderText(_translate("MainWindow", "0.00"))
        self.InitialNucleiConcentrationLabel.setText(_translate("MainWindow", "Initial Nuclei Concentration (mol/L)"))
        self.InitialNucleiConcentrationLineEdit.setPlaceholderText(_translate("MainWindow", "0.00"))
        self.InitialNucleiDiameterLabel.setText(_translate("MainWindow", "Nuclei Diameter (nm)"))
        self.InitialNucleiDiameterLineEdit.setPlaceholderText(_translate("MainWindow", "0.00"))
        self.InitialNucleiHeightLabel.setText(_translate("MainWindow", "Nuclei Height (nm)"))
        self.InitialNucleiHeightLineEdit.setPlaceholderText(_translate("MainWindow", "0.00"))
        self.InitialSystemLabel.setText(_translate("MainWindow", "<b>Initial System:</b>"))

        self.InputSpecificationTextEdit.setHtml(_translate("MainWindow",
                                                           "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0/EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                           "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                           "p, li { white-space: pre-wrap; }\n"
                                                           "</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                                           "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Times New Roman,serif\'; font-size:11pt;\">User Guide</span><span style=\" font-size:11pt;\"> </span></p>\n"
                                                           "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
                                                           "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Times New Roman,serif,serif\'; font-size:11pt; color:#000000;\">1. Set COF Parameters: Please set the corresponding parameters according to experimental measurements and reaction pathway analysis.</span></p>\n"
                                                           "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
                                                           "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Times New Roman,serif,serif\'; font-size:11pt; color:#000000;\">2. Initial System: This section allows you to set the initial conditions of the system, such as initial volume, initial nuclei concentration, diameter, and height.</span></p>\n"
                                                           "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
                                                           "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Times New Roman,serif,serif\'; font-size:11pt; color:#000000;\">3. Conditions to Add Monomer: In this section, first enter the Monomer Concentration, and then input the monomer addition sequence.</span></p>\n"
                                                           "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
                                                           "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Times New Roman,serif,serif\'; font-size:11pt; color:#000000;\">4. After entering the monomer concentration and the addition sequence, click 'Check Input' to calculate the number of additions and the total added volume.</span></p>\n"
                                                           "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
                                                           "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Times New Roman,serif,serif\'; font-size:11pt; color:#000000;\">5. Run Computational Engine: After entering the basic parameters and monomer addition sequence, go to the `Run Computational Engine` to run the computation.</span></p>\n"
                                                           "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
                                                           "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Times New Roman,serif,serif\'; font-size:11pt; color:#000000;\">6. Post Processing: After the computation is complete, click on the 'Get Result Summary' button to obtain the final results and crystal distribution diagram.</span></p>\n"
                                                           "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
                                                           "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Times New Roman,serif,serif\'; font-size:11pt; color:#000000;\">**Before running the monomer next addition sequence computation with the same number of additions, please ensure that all addition sequence files with the same number of additions (e.g., nuc__1_0_x, where x is identical) in the MlCOFSyn\\negen1o directory are first backed up to another folder or deleted. Otherwise, the program will not run when you click Start.**</span></p></body></html>"))

        self.ParametersLayer.setTabText(self.ParametersLayer.indexOf(self.tab), _translate("MainWindow", " System and Parameters"))
        self.NEgen1OutputLabelTextEdit.setText(_translate("MainWindow", "OUTPUT:"))
        self.NEgen1OutputLabel.setText(_translate("MainWindow", "NEgen1o Model"))
        self.NEgen1StartPushButton.setText(_translate("MainWindow", "Run"))
        self.ParametersLayer.setTabText(self.ParametersLayer.indexOf(self.NEgenOutput), _translate("MainWindow", "Run Computational Engine"))
        self.QLabel_2.setText(_translate("MainWindow", "Q"))
        self.RSDLabel_2.setText(_translate("MainWindow", "RSD"))
        self.LargesDiameterLabel_2.setText(_translate("MainWindow", "Largest Diameter (nm)"))
        self.AverageDiameterLabel_2.setText(_translate("MainWindow", "Averge Diameter (nm)"))
        # self.TotalReactionTimesLabel.setText(_translate("MainWindow", "Total Reaction Time (s)"))
        # self.TotalVolumeLabel.setText(_translate("MainWindow", "Total Volume of Reaction"))
        self.DHRatioLabel.setText(_translate("MainWindow", "Diameter-to-Height Ratio"))
        self.DiameterDistributionLabel.setText(_translate("MainWindow", "Diameter Distribution"))
        self.DataoutputPushButton.setText(_translate("MainWindow", "Get Result Summary"))
        self.ParametersLayer.setTabText(self.ParametersLayer.indexOf(self.widget), _translate("MainWindow", "Post Processing"))
        self.sequenceInputLabel.setText("Monomer Addition Sequence Input:")