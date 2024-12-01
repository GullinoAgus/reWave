# Form implementation generated from reading ui file 'UI/Main.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(805, 718)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.config_tab = QtWidgets.QWidget()
        self.config_tab.setObjectName("config_tab")
        self.gridLayout = QtWidgets.QGridLayout(self.config_tab)
        self.gridLayout.setObjectName("gridLayout")
        self.sim_conf_box = QtWidgets.QGroupBox(self.config_tab)
        self.sim_conf_box.setObjectName("sim_conf_box")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.sim_conf_box)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.incidence_input = QtWidgets.QDoubleSpinBox(self.sim_conf_box)
        font = QtGui.QFont()
        font.setKerning(True)
        self.incidence_input.setFont(font)
        self.incidence_input.setFrame(True)
        self.incidence_input.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.incidence_input.setMaximum(90.0)
        self.incidence_input.setObjectName("incidence_input")
        self.gridLayout_3.addWidget(self.incidence_input, 2, 2, 1, 1)
        self.max_freq_input = QtWidgets.QDoubleSpinBox(self.sim_conf_box)
        self.max_freq_input.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.max_freq_input.setDecimals(3)
        self.max_freq_input.setMinimum(0.1)
        self.max_freq_input.setMaximum(10.0)
        self.max_freq_input.setSingleStep(0.5)
        self.max_freq_input.setProperty("value", 10.0)
        self.max_freq_input.setObjectName("max_freq_input")
        self.gridLayout_3.addWidget(self.max_freq_input, 1, 4, 1, 1)
        self.incidence_label = QtWidgets.QLabel(self.sim_conf_box)
        self.incidence_label.setObjectName("incidence_label")
        self.gridLayout_3.addWidget(self.incidence_label, 2, 1, 1, 1)
        self.min_freq_label = QtWidgets.QLabel(self.sim_conf_box)
        self.min_freq_label.setObjectName("min_freq_label")
        self.gridLayout_3.addWidget(self.min_freq_label, 1, 1, 1, 1)
        self.min_freq_input = QtWidgets.QDoubleSpinBox(self.sim_conf_box)
        self.min_freq_input.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.min_freq_input.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectionMode.CorrectToPreviousValue)
        self.min_freq_input.setDecimals(3)
        self.min_freq_input.setMinimum(0.001)
        self.min_freq_input.setMaximum(10.0)
        self.min_freq_input.setSingleStep(0.05)
        self.min_freq_input.setObjectName("min_freq_input")
        self.gridLayout_3.addWidget(self.min_freq_input, 1, 2, 1, 1)
        self.max_freq_label = QtWidgets.QLabel(self.sim_conf_box)
        self.max_freq_label.setObjectName("max_freq_label")
        self.gridLayout_3.addWidget(self.max_freq_label, 1, 3, 1, 1)
        self.period_label = QtWidgets.QLabel(self.sim_conf_box)
        self.period_label.setObjectName("period_label")
        self.gridLayout_3.addWidget(self.period_label, 3, 1, 1, 1)
        self.period_input = QtWidgets.QSpinBox(self.sim_conf_box)
        self.period_input.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.period_input.setMinimum(1)
        self.period_input.setObjectName("period_input")
        self.gridLayout_3.addWidget(self.period_input, 3, 2, 1, 1)
        self.polarization_CB = QtWidgets.QComboBox(self.sim_conf_box)
        self.polarization_CB.setObjectName("polarization_CB")
        self.polarization_CB.addItem("")
        self.polarization_CB.addItem("")
        self.gridLayout_3.addWidget(self.polarization_CB, 3, 4, 1, 1)
        self.polarization_label = QtWidgets.QLabel(self.sim_conf_box)
        self.polarization_label.setObjectName("polarization_label")
        self.gridLayout_3.addWidget(self.polarization_label, 3, 3, 1, 1)
        self.freq_sweep_check = QtWidgets.QCheckBox(self.sim_conf_box)
        self.freq_sweep_check.setEnabled(True)
        self.freq_sweep_check.setChecked(False)
        self.freq_sweep_check.setTristate(False)
        self.freq_sweep_check.setObjectName("freq_sweep_check")
        self.gridLayout_3.addWidget(self.freq_sweep_check, 0, 1, 1, 2)
        self.gridLayout.addWidget(self.sim_conf_box, 2, 1, 1, 1)
        self.layer_box = QtWidgets.QGroupBox(self.config_tab)
        self.layer_box.setMaximumSize(QtCore.QSize(16777215, 250))
        self.layer_box.setObjectName("layer_box")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.layer_box)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.mu_input = QtWidgets.QLineEdit(self.layer_box)
        self.mu_input.setObjectName("mu_input")
        self.gridLayout_4.addWidget(self.mu_input, 0, 1, 1, 1)
        self.add_layer_button = QtWidgets.QPushButton(self.layer_box)
        self.add_layer_button.setObjectName("add_layer_button")
        self.gridLayout_4.addWidget(self.add_layer_button, 5, 0, 1, 3)
        self.sigma_label = QtWidgets.QLabel(self.layer_box)
        self.sigma_label.setMaximumSize(QtCore.QSize(16777215, 30))
        self.sigma_label.setObjectName("sigma_label")
        self.gridLayout_4.addWidget(self.sigma_label, 2, 0, 1, 1)
        self.mu_label = QtWidgets.QLabel(self.layer_box)
        self.mu_label.setObjectName("mu_label")
        self.gridLayout_4.addWidget(self.mu_label, 0, 0, 1, 1)
        self.width_label = QtWidgets.QLabel(self.layer_box)
        self.width_label.setObjectName("width_label")
        self.gridLayout_4.addWidget(self.width_label, 3, 0, 1, 1)
        self.epsilon_label = QtWidgets.QLabel(self.layer_box)
        self.epsilon_label.setObjectName("epsilon_label")
        self.gridLayout_4.addWidget(self.epsilon_label, 1, 0, 1, 1)
        self.width_input = QtWidgets.QLineEdit(self.layer_box)
        self.width_input.setObjectName("width_input")
        self.gridLayout_4.addWidget(self.width_input, 3, 1, 1, 1)
        self.width_unit_CB = QtWidgets.QComboBox(self.layer_box)
        self.width_unit_CB.setObjectName("width_unit_CB")
        self.width_unit_CB.addItem("")
        self.width_unit_CB.addItem("")
        self.gridLayout_4.addWidget(self.width_unit_CB, 3, 2, 1, 1)
        self.sigma_input = QtWidgets.QLineEdit(self.layer_box)
        self.sigma_input.setMaxLength(100)
        self.sigma_input.setObjectName("sigma_input")
        self.gridLayout_4.addWidget(self.sigma_input, 2, 1, 1, 1)
        self.epsilon_input = QtWidgets.QLineEdit(self.layer_box)
        self.epsilon_input.setObjectName("epsilon_input")
        self.gridLayout_4.addWidget(self.epsilon_input, 1, 1, 1, 1)
        self.layer_name_input = QtWidgets.QLineEdit(self.layer_box)
        self.layer_name_input.setObjectName("layer_name_input")
        self.gridLayout_4.addWidget(self.layer_name_input, 4, 1, 1, 1)
        self.layer_name_label = QtWidgets.QLabel(self.layer_box)
        self.layer_name_label.setObjectName("layer_name_label")
        self.gridLayout_4.addWidget(self.layer_name_label, 4, 0, 1, 1)
        self.gridLayout.addWidget(self.layer_box, 2, 0, 1, 1)
        self.layer_view_box = QtWidgets.QGroupBox(self.config_tab)
        self.layer_view_box.setObjectName("layer_view_box")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layer_view_box)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.scrollArea = QtWidgets.QScrollArea(self.layer_view_box)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.layer_view_content = QtWidgets.QWidget()
        self.layer_view_content.setGeometry(QtCore.QRect(0, 0, 759, 321))
        self.layer_view_content.setObjectName("layer_view_content")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layer_view_content)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.scrollArea.setWidget(self.layer_view_content)
        self.horizontalLayout.addWidget(self.scrollArea)
        self.gridLayout.addWidget(self.layer_view_box, 0, 0, 1, 2)
        self.pushButton = QtWidgets.QPushButton(self.config_tab)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 3, 0, 1, 2)
        self.tabWidget.addTab(self.config_tab, "")
        self.result_tab = QtWidgets.QWidget()
        self.result_tab.setObjectName("result_tab")
        self.result_layout = QtWidgets.QVBoxLayout(self.result_tab)
        self.result_layout.setObjectName("result_layout")
        self.results_box = QtWidgets.QGroupBox(self.result_tab)
        self.results_box.setMaximumSize(QtCore.QSize(16777215, 100))
        self.results_box.setObjectName("results_box")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.results_box)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.reflex_coef_output = QtWidgets.QLineEdit(self.results_box)
        self.reflex_coef_output.setReadOnly(True)
        self.reflex_coef_output.setObjectName("reflex_coef_output")
        self.gridLayout_5.addWidget(self.reflex_coef_output, 2, 1, 1, 1)
        self.reflex_coef_label = QtWidgets.QLabel(self.results_box)
        self.reflex_coef_label.setObjectName("reflex_coef_label")
        self.gridLayout_5.addWidget(self.reflex_coef_label, 2, 0, 1, 1)
        self.trans_coef_output = QtWidgets.QLineEdit(self.results_box)
        self.trans_coef_output.setReadOnly(True)
        self.trans_coef_output.setObjectName("trans_coef_output")
        self.gridLayout_5.addWidget(self.trans_coef_output, 2, 3, 1, 1)
        self.trans_coef_label = QtWidgets.QLabel(self.results_box)
        self.trans_coef_label.setObjectName("trans_coef_label")
        self.gridLayout_5.addWidget(self.trans_coef_label, 2, 2, 1, 1)
        self.eval_freq_label = QtWidgets.QLabel(self.results_box)
        self.eval_freq_label.setObjectName("eval_freq_label")
        self.gridLayout_5.addWidget(self.eval_freq_label, 0, 1, 1, 1)
        self.eval_freq_output = QtWidgets.QLineEdit(self.results_box)
        self.eval_freq_output.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.eval_freq_output.setReadOnly(True)
        self.eval_freq_output.setObjectName("eval_freq_output")
        self.gridLayout_5.addWidget(self.eval_freq_output, 0, 2, 1, 1)
        self.result_layout.addWidget(self.results_box)
        self.tabWidget.addTab(self.result_tab, "")
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.freq_sweep_check.clicked['bool'].connect(MainWindow.freq_sweep_clicked) # type: ignore
        self.pushButton.clicked.connect(MainWindow.calculate) # type: ignore
        self.add_layer_button.clicked.connect(MainWindow.add_layer) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.sim_conf_box.setTitle(_translate("MainWindow", "Sim Config"))
        self.incidence_label.setText(_translate("MainWindow", "Incidencia [º]"))
        self.min_freq_label.setText(_translate("MainWindow", "Frec Min [GHz]"))
        self.max_freq_label.setText(_translate("MainWindow", "Frec Max [GHz]"))
        self.period_label.setText(_translate("MainWindow", "Periodos de capas"))
        self.polarization_CB.setItemText(0, _translate("MainWindow", "TM"))
        self.polarization_CB.setItemText(1, _translate("MainWindow", "TE"))
        self.polarization_label.setText(_translate("MainWindow", "Polarizacion"))
        self.freq_sweep_check.setText(_translate("MainWindow", "Barrido de angulo"))
        self.layer_box.setTitle(_translate("MainWindow", "Añadir capa"))
        self.mu_input.setText(_translate("MainWindow", "1e0"))
        self.add_layer_button.setText(_translate("MainWindow", "Añadir"))
        self.sigma_label.setText(_translate("MainWindow", "σ"))
        self.mu_label.setText(_translate("MainWindow", "μr"))
        self.width_label.setText(_translate("MainWindow", "Espesor"))
        self.epsilon_label.setText(_translate("MainWindow", "εr"))
        self.width_input.setText(_translate("MainWindow", "250e-3"))
        self.width_unit_CB.setItemText(0, _translate("MainWindow", "λs"))
        self.width_unit_CB.setItemText(1, _translate("MainWindow", "mm"))
        self.sigma_input.setText(_translate("MainWindow", "0"))
        self.epsilon_input.setText(_translate("MainWindow", "1e0"))
        self.layer_name_input.setText(_translate("MainWindow", "Capa"))
        self.layer_name_label.setText(_translate("MainWindow", "Nombre"))
        self.layer_view_box.setTitle(_translate("MainWindow", "Visualizacion"))
        self.pushButton.setText(_translate("MainWindow", "Calcular"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.config_tab), _translate("MainWindow", "Configuracion"))
        self.results_box.setTitle(_translate("MainWindow", "Resultados"))
        self.reflex_coef_label.setText(_translate("MainWindow", "Coeficiente de reflexion"))
        self.trans_coef_label.setText(_translate("MainWindow", "Coeficiente de transmision"))
        self.eval_freq_label.setText(_translate("MainWindow", "Frecuencia de evaluacion [GHz]"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.result_tab), _translate("MainWindow", "Resultados"))
