import locale
import numpy as np
from PyQt6 import QtWidgets, QtGui, QtCore

from UI.Main_UI import Ui_MainWindow
from Utils.TLineNetworkClass import TLineNetwork
from Utils.plotWidget import MplCanvas
from Utils.MediumClass import Medium


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        locale.setlocale(locale.LC_ALL, '')
        self.setupUi(self)
        self.setWindowTitle("Calculador de apantallamiento")
        self.apant_plot = MplCanvas(self.result_tab)
        self.coefs_plot = MplCanvas(self.result_tab)
        self.scientific_validator = QtGui.QDoubleValidator()
        # Set scientific notation for all input fields
        self.mu_input.setValidator(self.scientific_validator)
        self.epsilon_input.setValidator(self.scientific_validator)
        self.sigma_input.setValidator(self.scientific_validator)
        self.width_input.setValidator(self.scientific_validator)

        self.layer_list: list[LayerWidget] = []

    def calculate(self):
        '''
        Calculo de la eficiencia de apantallamiento o de 
        los coeficientes en funcion de si es barrido de angulo o frecuencia
        '''

        # Se construye la lista de medios a partir de los widgets de capas
        layers = []
        for layer in self.layer_list:
            if layer.isConnected():
                layers.append(LayerWidget.to_medium(layer))
        if self.period_input.value() > 1:
            last_layer = layers.pop()
            length = len(layers)
            for i in range(self.period_input.value()):
                layers.append(layers[1:length])
            layers.append(last_layer)

        # Se verifica si se esta en modo barrido de angulo o frecuencia
        if self.freq_sweep_check.isChecked():   # Barrido de angulo
            self.coefs_plot.hide()
            self.coefs_plot.navToolBar.hide()
            # Valores de angulos a evaluar y freq
            theta_i = np.linspace(0, np.pi/2, 1000)
            freq = float(self.min_freq_input.value()*1e9)
            gamma_par = []
            gamma_per = []
            for theta in theta_i:
                # Para cada angulo calculamos nuevamente las lineas equivalente
                # y presentamos el modulo de los coeficientes de reflexion para incidencia TM y TE
                net = TLineNetwork(layers, theta)
                gamma_par.append(
                    np.abs(net.calc_total_reflection_coef_and_losses_par(freq))[0])
                gamma_per.append(
                    np.abs(net.calc_total_reflection_coef_and_losses_par(freq))[0])
            self.apant_plot.plot_gammas(theta_i, gamma_par, gamma_per)

        else:  # Barrido de freq
            self.coefs_plot.show()
            self.coefs_plot.navToolBar.show()
            # Armo la cadena de lineas de transmision equivalente
            net = TLineNetwork(layers, self.theta_i)
            # Lista de frecuencias a evaluar
            freqs = np.logspace(np.log10(float(self.min_freq_input.value()*1e9)), np.log10(float(
                self.max_freq_input.value()*1e9)), 1000, base=10)
            trans = []
            EA = []
            ref = []
            # Verifico el tipo de polarizacion incidente
            if self.polarization_CB.currentText() == "TM":

                for freq in freqs:
                    # Calculo del coef de reflexion total y las perdidas
                    refl, losses = net.calc_total_reflection_coef_and_losses_par(
                        freq)

                    # Apendeo los resultados para el vector de poynting
                    # para la reflexion es modulo cuadrado y para la transmision
                    # 1-|gamma|**2 agregando las perdidas
                    ref.append(np.abs(refl)**2)
                    trans.append((1 - np.abs(refl)**2) * 10**(-(losses/10)))
                    EA.append(-10*np.log10(1 - np.abs(refl)**2) + losses)
            else:
                for freq in freqs:
                    refl, losses = net.calc_total_reflection_coef_and_losses_per(
                        freq)
                    ref.append(np.abs(refl)**2)
                    trans.append((1 - np.abs(refl)**2) * 10**(-(losses/10)))
                    EA.append(-10*np.log10(1 - np.abs(refl)**2) + losses)

            self.apant_plot.plot_effeciency(
                freqs, EA)
            self.coefs_plot.plot_coefs(
                freqs, ref, trans)

        self.tabWidget.setCurrentIndex(1)

    def freq_sweep_clicked(self, state):
        if state:
            self.polarization_CB.setDisabled(True)
            self.polarization_label.setDisabled(True)
            self.incidence_input.setDisabled(True)
            self.incidence_label.setDisabled(True)
            self.max_freq_input.setDisabled(True)
            self.max_freq_label.setDisabled(True)
            self.min_freq_label.setText("Frec [GHz]")
        else:
            self.polarization_CB.setEnabled(True)
            self.polarization_label.setEnabled(True)
            self.incidence_input.setEnabled(True)
            self.incidence_label.setEnabled(True)
            self.max_freq_input.setEnabled(True)
            self.max_freq_label.setEnabled(True)
            self.min_freq_label.setText("Frec Min [GHz]")

    def add_layer(self):
        if len(self.layer_list) == 0:
            layer = LayerWidget(self.layer_view_content, self.mu_value, self.epsilon_value,
                                self.sigma_value, self.width_value, self.width_unit, self.layer_name,
                                "Incidencia", len(
                                    self.layer_list), self.layer_swap_handler,
                                self.layer_delete_handler)
        elif len(self.layer_list) == 1:
            layer = LayerWidget(self.layer_view_content, self.mu_value, self.epsilon_value,
                                self.sigma_value, self.width_value, self.width_unit, self.layer_name,
                                "Transmision", len(
                                    self.layer_list), self.layer_swap_handler,
                                self.layer_delete_handler)
        else:
            layer = LayerWidget(self.layer_view_content, self.mu_value, self.epsilon_value,
                                self.sigma_value, self.width_value, self.width_unit, self.layer_name,
                                "Transmision", len(
                                    self.layer_list), self.layer_swap_handler,
                                self.layer_delete_handler)
            self.layer_list[-1].set_type("Intermedio")
        self.layer_list.append(layer)
        pass

    @property
    def mu_value(self):
        return locale.atof(self.mu_input.text())

    @property
    def epsilon_value(self):
        return locale.atof(self.epsilon_input.text())

    @property
    def sigma_value(self):
        return locale.atof(self.sigma_input.text())

    @property
    def width_value(self):
        return locale.atof(self.width_input.text())

    @property
    def width_unit(self):
        return self.width_unit_CB.currentText()

    @property
    def layer_name(self):
        return self.layer_name_input.text()

    @property
    def theta_i(self):
        return locale.atof(self.incidence_input.text()) * np.pi / 180

    def layer_swap_handler(self, layer_num, direction):
        if (direction == -1 and layer_num == 0) or (direction == 1 and layer_num == len(self.layer_list) - 1):
            return
        if (layer_num == 0 and direction == 1) or (layer_num == 1 and direction == -1):
            self.layer_list[0].set_type("Intermedio")
            self.layer_list[1].set_type("Incidencia")
        elif (layer_num == len(self.layer_list) - 1 and direction == -1) or (layer_num == len(self.layer_list) - 2 and direction == 1):
            self.layer_list[-1].set_type("Intermedio")
            self.layer_list[-2].set_type("Transmision")
        self.layer_list[layer_num].layer_num = layer_num + direction
        self.layer_list[layer_num + direction].layer_num = layer_num
        self.layer_list[layer_num], self.layer_list[layer_num + direction] = \
            self.layer_list[layer_num + direction], self.layer_list[layer_num]
        auxlay = self.layer_view_content.layout()
        for i in range(len(self.layer_list)):
            auxlay.takeAt(i)
        for i in self.layer_list:
            auxlay.addWidget(i)

    def layer_delete_handler(self, layer_num):

        auxlay = self.layer_view_content.layout()
        layer = self.layer_list.pop(layer_num)
        layer_index = layer.layer_num
        auxlay.removeWidget(layer)
        layer.destroy(True, True)
        layer.deleteLater()
        if layer_num == 0 and len(self.layer_list):
            self.layer_list[0].set_type("Incidencia")
        elif layer_num == len(self.layer_list) and len(self.layer_list):
            self.layer_list[-1].set_type("Transmision")
        for i in range(len(self.layer_list)):
            if i >= layer_index:
                self.layer_list[i].layer_num -= 1
        del layer


class LayerWidget(QtWidgets.QWidget):
    def __init__(self, parent, mur, er, sigma, width, width_unit, name, layer_type, layer_num, swap_handler, delete_handler):
        super().__init__(parent)
        parent.layout().addWidget(self)
        self.layout = QtWidgets.QGridLayout(self)
        self.mur = mur
        self.er = er
        self.sigma = sigma
        self.layer_width = width
        self.layer_num = layer_num
        self.name = name
        self.connected = True
        self.infoViewBox = QtWidgets.QGroupBox('', parent)
        self.layout.addWidget(self.infoViewBox)
        self.boxlayout = QtWidgets.QGridLayout(self.infoViewBox)
        self.infoViewBox.setMaximumWidth(200)
        self.rightArrowButt = QtWidgets.QPushButton('>', self.infoViewBox)
        self.boxlayout.addWidget(self.rightArrowButt, 0, 2)
        self.rightArrowButt.clicked.connect(
            lambda: swap_handler(self.layer_num, 1))
        self.leftArrowButt = QtWidgets.QPushButton('<', self.infoViewBox)
        self.boxlayout.addWidget(self.leftArrowButt, 0, 0)
        self.leftArrowButt.clicked.connect(
            lambda: swap_handler(self.layer_num, -1))
        self.deleteButt = QtWidgets.QPushButton(self.infoViewBox)
        self.deleteButt.setIcon(QtGui.QIcon.fromTheme('user-trash'))
        self.boxlayout.addWidget(self.deleteButt, 0, 1)
        self.deleteButt.clicked.connect(
            lambda: delete_handler(self.layer_num))
        self.ConnectedCheck = QtWidgets.QCheckBox(
            'Habilitada', self.infoViewBox)
        self.ConnectedCheck.setChecked(True)
        self.boxlayout.addWidget(self.ConnectedCheck, 1, 0)
        self.ConnectedCheck.toggled['bool'].connect(self.setConnected)
        self.scientific_validator = QtGui.QDoubleValidator()

        # Set scientific notation for all input fields
        self.mu_input = QtWidgets.QLineEdit(self.infoViewBox)
        self.mu_input.setObjectName("mu_input")
        self.mu_input.setValidator(self.scientific_validator)
        self.boxlayout.addWidget(self.mu_input, 2, 1, 1, 1)
        self.sigma_label = QtWidgets.QLabel(self.infoViewBox)
        self.sigma_label.setMaximumSize(QtCore.QSize(16777215, 30))
        self.sigma_label.setObjectName("sigma_label")
        self.boxlayout.addWidget(self.sigma_label, 4, 0, 1, 1)
        self.mu_label = QtWidgets.QLabel(self.infoViewBox)
        self.mu_label.setObjectName("mu_label")
        self.boxlayout.addWidget(self.mu_label, 2, 0, 1, 1)
        self.width_label = QtWidgets.QLabel(self.infoViewBox)
        self.width_label.setObjectName("width_label")
        self.boxlayout.addWidget(self.width_label, 5, 0, 1, 1)
        self.epsilon_label = QtWidgets.QLabel(self.infoViewBox)
        self.epsilon_label.setObjectName("epsilon_label")
        self.boxlayout.addWidget(self.epsilon_label, 3, 0, 1, 1)
        self.width_input = QtWidgets.QLineEdit(self.infoViewBox)
        self.width_input.setObjectName("width_input")
        self.width_input.setValidator(self.scientific_validator)
        self.boxlayout.addWidget(self.width_input, 5, 1, 1, 1)
        self.width_unit_CB = QtWidgets.QComboBox(self.infoViewBox)
        self.width_unit_CB.setObjectName("width_unit_CB")
        self.width_unit_CB.addItem("")
        self.width_unit_CB.addItem("")
        self.boxlayout.addWidget(self.width_unit_CB, 5, 2, 1, 1)
        self.sigma_input = QtWidgets.QLineEdit(self.infoViewBox)
        self.sigma_input.setMaxLength(100)
        self.sigma_input.setObjectName("sigma_input")
        self.sigma_input.setValidator(self.scientific_validator)
        self.boxlayout.addWidget(self.sigma_input, 4, 1, 1, 1)
        self.epsilon_input = QtWidgets.QLineEdit(self.infoViewBox)
        self.epsilon_input.setObjectName("epsilon_input")
        self.epsilon_input.setValidator(self.scientific_validator)
        self.boxlayout.addWidget(self.epsilon_input, 3, 1, 1, 1)
        self.layer_name_input = QtWidgets.QLineEdit(self.infoViewBox)
        self.layer_name_input.setObjectName("layer_name_input")
        self.boxlayout.addWidget(self.layer_name_input, 6, 1, 1, 1)
        self.layer_name_label = QtWidgets.QLabel(self.infoViewBox)
        self.layer_name_label.setObjectName("layer_name_label")
        self.boxlayout.addWidget(self.layer_name_label, 6, 0, 1, 1)
        self.layer_type = QtWidgets.QLabel(self.infoViewBox)
        self.layer_type.setObjectName("layer_name_label")
        myFont = QtGui.QFont()
        myFont.setBold(True)
        self.layer_type.setFont(myFont)
        self.layer_type.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.boxlayout.addWidget(self.layer_type, 7, 0, 1, 3)

        self.mu_input.setText(locale.str(self.mur))
        self.sigma_label.setText("σ")
        self.mu_label.setText("μr")
        self.width_label.setText("Espesor")
        self.epsilon_label.setText("εr")
        self.width_input.setText(locale.str(self.layer_width))
        self.width_unit_CB.setItemText(0, "λs")
        self.width_unit_CB.setItemText(1, "mm")
        self.width_unit_CB.setCurrentIndex(1 if width_unit == 'mm' else 0)
        self.sigma_input.setText((locale.str(self.sigma)))
        self.epsilon_input.setText(locale.str(self.er))
        self.layer_name_label.setText("Nombre")
        self.layer_name_input.setText(self.name)
        self.layer_type.setText(layer_type)
        self.set_type(layer_type)

    def setConnected(self, en):
        self.connected = en

    def isConnected(self):
        return self.connected

    def set_type(self, layer_type):
        if layer_type == "Incidencia":
            self.layer_type.setText("Incidencia")
            self.width_label.setVisible(False)
            self.width_input.setVisible(False)
            self.width_unit_CB.setVisible(False)
        elif layer_type == "Transmision":
            self.layer_type.setText("Transmision")
            self.width_label.setVisible(False)
            self.width_input.setVisible(False)
            self.width_unit_CB.setVisible(False)

        else:
            self.layer_type.setText("Intermedio")
            self.width_label.setVisible(True)
            self.width_input.setVisible(True)
            self.width_unit_CB.setVisible(True)

    def to_medium(self):
        if self.width_unit_CB.currentText() == "mm":
            med = Medium(ur=self.mu_value,
                         sigma=self.sigma_value,
                         er=self.epsilon_value,
                         width=self.width_value * 1e-3)
        else:
            med = Medium(ur=self.mu_value,
                         sigma=self.sigma_value,
                         er=self.epsilon_value,
                         width_lambdas=self.width_value)
        return med

    @property
    def mu_value(self):
        return locale.atof(self.mu_input.text())

    @property
    def epsilon_value(self):
        return locale.atof(self.epsilon_input.text())

    @property
    def sigma_value(self):
        return locale.atof(self.sigma_input.text())

    @property
    def width_value(self):
        return locale.atof(self.width_input.text())

    @property
    def width_unit(self):
        return self.width_unit_CB.currentText()
