import locale
import numpy as np
from PyQt6 import QtWidgets, QtGui, QtCore

from UI.Main_UI import Ui_MainWindow
from Utils.TLNetwork import TLineNetwork
from Utils.plotWidget import MplCanvas
from Utils.Medium import Medium

units_dict = {'GHz': 1e9, 'MHz': 1e6, 'KHz': 1e3, 'Hz': 1}


def sanitize_values(value, epsilon=1e-6, min_val=0):
    return value if value >= epsilon else min_val


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        locale.setlocale(locale.LC_ALL, '')
        self.setupUi(self)
        self.setWindowTitle("Calculador de apantallamiento")

        self.coef_1_plot = MplCanvas(self.gammas_1)
        self.coef_2_plot = MplCanvas(self.gammas_2)
        self.apant_plot = MplCanvas(self.se)

        self.scientific_validator = QtGui.QDoubleValidator()
        # Validadores en inputs globales de la UI
        self.mu_input.setValidator(self.scientific_validator)
        self.epsilon_input.setValidator(self.scientific_validator)
        self.sigma_input.setValidator(self.scientific_validator)
        self.width_input.setValidator(self.scientific_validator)

        self.layer_list: list['LayerWidget'] = []

        # Estilo general (cards, chip, campos)
        self.setStyleSheet("""
        QFrame#LayerCard {
          border: 1px solid #3f3f3f;
          border-radius: 12px;
          background: #2b2b2b;
        }
        QLabel#TypeChip {
          border-radius: 10px;
          padding: 2px 8px;
          color: white;
          background: #3a6ea5;
          font-weight: 600;
        }
        QLabel { color: #ddd; }
        QToolButton { border: none; }
        QToolButton:hover { background: rgba(255,255,255,0.08); border-radius: 6px; }
        QDoubleSpinBox, QLineEdit, QComboBox {
          background: #212121; color: #e6e6e6; border: 1px solid #444; border-radius: 6px; padding: 2px 6px;
        }
        QComboBox::drop-down { border: 0; }
        """)

    def next_plot(self):
        self.plots.setCurrentIndex((self.plots.currentIndex() + 1) % self.plots.count())

    def prev_plot(self):
        self.plots.setCurrentIndex((self.plots.currentIndex() - 1) % self.plots.count())

    def create_layers(self):
        layers = []
        for layer in self.layer_list:
            if layer.isConnected():
                layers.append(LayerWidget.to_medium(layer))
        return layers

    def calculate(self):
        """
        Calculo de la eficiencia de apantallamiento o de
        los coeficientes en funcion de si es barrido de angulo o frecuencia
        """
        trans, T, EA, ref, A, R = [], [], [], [], [], []

        # Se construye la lista de medios a partir de los widgets de capas
        layers = self.create_layers()

        if self.freq_sweep_check.isChecked():
            x = np.linspace(0, 89, 10000)
            unit = 'Angulo de incidencia [°]'
            xlim = [0, 89]
        else:
            x = np.logspace(np.log10(self.min_freq), np.log10(self.max_freq), 10000, base=10)
            unit = "Frecuencia [Hz]"
            xlim = [self.min_freq, self.max_freq]

        # Se verifica si es barrido de ángulo o de frecuencia
        if self.freq_sweep_check.isChecked():   # Barrido de ángulo
            freq = self.min_freq
            for theta in np.radians(x):
                net = TLineNetwork(layers, theta)
                if self.polarization_CB.currentText() == "TM":
                    refl = net.get_reflexion_TM(freq)
                    se = net.get_se_TM(freq)
                    eta_i = net._layer_list[0].Zo_TM(freq, self.theta_i)
                    eta_s = net._layer_list[-1].Zo_TM(freq, self.theta_i)
                else:
                    refl = net.get_reflexion_TE(freq)
                    se = net.get_se_TE(freq)  # Ei/Et
                    eta_i = net._layer_list[0].Zo_TE(freq, self.theta_i)
                    eta_s = net._layer_list[-1].Zo_TE(freq, self.theta_i)

                tau = 1 / se
                transmit = np.abs(tau) ** 2 * (eta_i / eta_s) * (np.cos(net.theta_t(freq)) / np.cos(self.theta_i))

                ref.append(sanitize_values(np.abs(refl)))
                trans.append(sanitize_values(np.abs(tau)))
                T.append(sanitize_values(np.abs(transmit)))
                R.append(sanitize_values(ref[-1] ** 2))
                A.append(sanitize_values(1 - R[-1] - T[-1]))
                EA.append(sanitize_values(20 * np.log10(np.abs(se))))
        else:  # Barrido de frecuencia
            net = TLineNetwork(layers, self.theta_i)
            for freq in x:
                if self.polarization_CB.currentText() == "TM":
                    refl = net.get_reflexion_TM(freq)
                    se = net.get_se_TM(freq)
                    eta_i = net._layer_list[0].Zo_TM(freq, self.theta_i)
                    eta_s = net._layer_list[-1].Zo_TM(freq, self.theta_i)
                else:
                    refl = net.get_reflexion_TE(freq)
                    se = net.get_se_TE(freq)  # Ei/Et
                    eta_i = net._layer_list[0].Zo_TE(freq, self.theta_i)
                    eta_s = net._layer_list[-1].Zo_TE(freq, self.theta_i)

                tau = 1 / se
                transmit = np.abs(tau) ** 2 * (eta_i / eta_s) * (np.cos(net.theta_t(freq)) / np.cos(self.theta_i))

                ref.append(sanitize_values(np.abs(refl)))
                trans.append(sanitize_values(np.abs(tau)))
                T.append(sanitize_values(np.abs(transmit)))
                R.append(sanitize_values(ref[-1] ** 2))
                A.append(sanitize_values(1 - R[-1] - T[-1]))
                EA.append(sanitize_values(20 * np.log10(np.abs(se))))

        self.coef_1_plot.plot_for_freq(
            x, [ref, trans],
            y_labels=['$|\\Gamma|$', '$|\\tau|$'],
            x_labels=["Coef. de Reflexión", "Coef. de Transmisión"],
            unit=unit, xlims=xlim
        )
        self.coef_2_plot.plot_for_freq(
            x, [R, T, A],
            y_labels=['$R$', '$T$', '$A$'],
            x_labels=["Frac. Potencia Reflejada", "Frac. Potencia Transmitida", "Frac. Potencia Absorbida"],
            unit=unit, xlims=xlim
        )
        self.apant_plot.plot_efficiency(x, EA, unit=unit)

        self.plots.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(1)

    def freq_sweep_clicked(self, state):
        if state:
            self.incidence_input.setDisabled(True)
            self.incidence_label.setDisabled(True)
            self.max_freq_input.setDisabled(True)
            self.max_freq_label.setDisabled(True)
            self.max_freq_unit_CB.setDisabled(True)
            self.min_freq_label.setText("Frec")
        else:
            self.incidence_input.setEnabled(True)
            self.incidence_label.setEnabled(True)
            self.max_freq_input.setEnabled(True)
            self.max_freq_label.setEnabled(True)
            self.max_freq_unit_CB.setEnabled(True)
            self.min_freq_label.setText("Frec Min")

    def add_layer(self):
        if len(self.layer_list) == 0:
            layer = LayerWidget(
                self.layer_view_content, self.mu_value, self.epsilon_value, self.sigma_value,
                self.width_value, self.width_unit, self.layer_name,
                "Incidencia", len(self.layer_list),
                self.layer_swap_handler, self.layer_delete_handler, self.layer_duplicate_handler
            )
            self.calculateButton.setEnabled(False)
        elif len(self.layer_list) == 1:
            layer = LayerWidget(
                self.layer_view_content, self.mu_value, self.epsilon_value, self.sigma_value,
                self.width_value, self.width_unit, self.layer_name,
                "Transmision", len(self.layer_list),
                self.layer_swap_handler, self.layer_delete_handler, self.layer_duplicate_handler
            )
            self.calculateButton.setEnabled(False)
        else:
            layer = LayerWidget(
                self.layer_view_content, self.mu_value, self.epsilon_value, self.sigma_value,
                self.width_value, self.width_unit, self.layer_name,
                "Transmision", len(self.layer_list),
                self.layer_swap_handler, self.layer_delete_handler, self.layer_duplicate_handler
            )
            self.layer_list[-1].set_type("Shield")

        self.layer_list.append(layer)

        if len(self.layer_list) >= 2:
            self.calculateButton.setEnabled(True)

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

    @property
    def min_freq(self):
        return locale.atof(self.min_freq_input.text()) * units_dict[self.min_freq_unit_CB.currentText()]

    @property
    def max_freq(self):
        return locale.atof(self.max_freq_input.text()) * units_dict[self.max_freq_unit_CB.currentText()]

    def layer_swap_handler(self, layer_num, direction):
        if (direction == -1 and layer_num == 0) or (direction == 1 and layer_num == len(self.layer_list) - 1):
            return
        if (layer_num == 0 and direction == 1) or (layer_num == 1 and direction == -1):
            self.layer_list[0].set_type("Shield")
            self.layer_list[1].set_type("Incidencia")
        elif (layer_num == len(self.layer_list) - 1 and direction == -1) or (layer_num == len(self.layer_list) - 2 and direction == 1):
            self.layer_list[-1].set_type("Shield")
            self.layer_list[-2].set_type("Transmision")

        self.layer_list[layer_num].layer_num = layer_num + direction
        self.layer_list[layer_num + direction].layer_num = layer_num
        self.layer_list[layer_num], self.layer_list[layer_num + direction] = \
            self.layer_list[layer_num + direction], self.layer_list[layer_num]

        # Reordenar en layout visual
        auxlay = self.layer_view_content.layout()
        while auxlay.count():
            auxlay.takeAt(0)
        for i in self.layer_list:
            auxlay.addWidget(i)

    def layer_delete_handler(self, layer_num):
        auxlay = self.layer_view_content.layout()
        layer = self.layer_list.pop(layer_num)
        layer_index = layer.layer_num
        auxlay.removeWidget(layer)
        layer.destroy(True, True)
        layer.deleteLater()

        if len(self.layer_list) < 2:
            self.calculateButton.setEnabled(False)

        if self.layer_list:
            self.layer_list[0].set_type("Incidencia")
        if len(self.layer_list) >= 2:
            for lw in self.layer_list[1:-1]:
                lw.set_type("Shield")
            self.layer_list[-1].set_type("Transmision")

        for i in range(len(self.layer_list)):
            if i >= layer_index:
                self.layer_list[i].layer_num = i

        # Reagregar al layout
        while auxlay.count():
            auxlay.takeAt(0)
        for i in self.layer_list:
            auxlay.addWidget(i)

    def layer_duplicate_handler(self, layer_num: int):
        """Duplica la capa en layer_num e inserta la copia inmediatamente a su derecha."""
        if layer_num < 0 or layer_num >= len(self.layer_list):
            return

        src = self.layer_list[layer_num]

        # 1) Leer valores actuales
        mur = src.mu_value
        er = src.epsilon_value
        sigma = src.sigma_value
        width = src.width_value
        width_unit = src.width_unit
        name = src.layer_name_input.text()

        # 2) Crear nueva capa (tipo provisional; normalizamos después)
        insert_pos = layer_num + 1
        new_layer = LayerWidget(
            self.layer_view_content, mur, er, sigma, width, width_unit, name,
            "Shield", insert_pos,
            self.layer_swap_handler, self.layer_delete_handler, self.layer_duplicate_handler
        )

        # 3) Respetar modelo de pérdidas
        if src.loss_kind == "eps_i":
            new_layer.loss_kind_CB.setCurrentIndex(1)
            new_layer.loss_spin.setValue(src.eps_i_value)
        else:
            new_layer.loss_kind_CB.setCurrentIndex(0)
            new_layer.loss_spin.setValue(sigma)

        # 4) Insertar inmediatamente a la derecha
        self.layer_list.insert(insert_pos, new_layer)

        # 5) Renumerar y normalizar tipos
        for i, lw in enumerate(self.layer_list):
            lw.layer_num = i
        if self.layer_list:
            self.layer_list[0].set_type("Incidencia")
        if len(self.layer_list) > 1:
            for lw in self.layer_list[1:-1]:
                lw.set_type("Shield")
            self.layer_list[-1].set_type("Transmision")

        # 6) Re-armar layout visual
        lay = self.layer_view_content.layout()
        while lay.count():
            lay.takeAt(0)
        for lw in self.layer_list:
            lay.addWidget(lw)

        if len(self.layer_list) >= 2:
            self.calculateButton.setEnabled(True)


class LayerWidget(QtWidgets.QWidget):
    def __init__(self, parent, mur, er, sigma, width, width_unit, name,
                 layer_type, layer_num, swap_handler, delete_handler, duplicate_handler=None):
        super().__init__(parent)
        parent.layout().addWidget(self)

        rootLay = QtWidgets.QVBoxLayout(self)
        rootLay.setContentsMargins(4, 4, 4, 4)

        # === Card base ===
        card = QtWidgets.QFrame(parent)
        card.setObjectName("LayerCard")
        card.setContentsMargins(0, 0, 0, 0)
        self.card = card 
        rootLay.addWidget(card)
        cardLay = QtWidgets.QVBoxLayout(card)
        cardLay.setContentsMargins(12, 12, 12, 12)
        cardLay.setSpacing(10)

        self._normal_card_css = """
            QFrame#LayerCard {
                border: 1px solid #3f3f3f;
                border-radius: 12px;
                background: #2b2b2b;
            }
            """
        self.card.setStyleSheet(self._normal_card_css)

        # Sombra
        shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(16)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QtGui.QColor(0, 0, 0, 80))
        card.setGraphicsEffect(shadow)

        # === HEADER (← tacho duplicar →   |   [Hab.]  [Chip]) ===
        hdr = QtWidgets.QHBoxLayout()
        hdr.setSpacing(8)
        cardLay.addLayout(hdr)

        def tb(icon_name: str, tip: str, fallback=QtWidgets.QStyle.StandardPixmap.SP_DirIcon):
            b = QtWidgets.QToolButton(card)
            ic = QtGui.QIcon.fromTheme(icon_name)
            if ic.isNull():
                ic = QtWidgets.QApplication.style().standardIcon(fallback)
            b.setIcon(ic)
            b.setAutoRaise(True)
            b.setIconSize(QtCore.QSize(18, 18))
            b.setFixedSize(26, 26)
            b.setToolTip(tip)
            return b

        self.leftArrowButt = tb('go-previous', 'Mover a la izquierda', QtWidgets.QStyle.StandardPixmap.SP_ArrowLeft)
        self.deleteButt = tb('user-trash', 'Eliminar capa', QtWidgets.QStyle.StandardPixmap.SP_TrashIcon)
        self.duplicateButt = tb('edit-copy', 'Duplicar a la derecha', QtWidgets.QStyle.StandardPixmap.SP_FileDialogNewFolder)
        self.rightArrowButt = tb('go-next', 'Mover a la derecha', QtWidgets.QStyle.StandardPixmap.SP_ArrowRight)

        # Orden pedido: flecha, tacho, duplicar, flecha
        hdr.addWidget(self.leftArrowButt)
        hdr.addWidget(self.deleteButt)
        hdr.addWidget(self.duplicateButt)
        hdr.addWidget(self.rightArrowButt)
        hdr.addStretch()

        # Habilitado + chip de tipo
        self.enabledCheck = QtWidgets.QCheckBox(card)
        self.enabledCheck.setChecked(True)
        self.enabledCheck.setToolTip("Habilitar/deshabilitar capa")
        hdr.addWidget(self.enabledCheck)

        self.typeChip = QtWidgets.QLabel("Incidencia", card)
        self.typeChip.setObjectName("TypeChip")
        self.typeChip.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.typeChip.setMinimumWidth(92)
        hdr.addWidget(self.typeChip)

        # Chip rojo de "deshabilitada" (oculto por defecto)
        self.disabledChip = QtWidgets.QLabel("DESH.", card)
        self.disabledChip.setObjectName("DisabledChip")
        self.disabledChip.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.disabledChip.setMinimumWidth(64)
        self.disabledChip.setStyleSheet(
            "border-radius:10px; padding:2px 8px; color:white; font-weight:600; background:#e74c3c;"
        )
        self.disabledChip.hide()
        hdr.addWidget(self.disabledChip)

        # Conexiones
        self.leftArrowButt.clicked.connect(lambda: swap_handler(self.layer_num, -1))
        self.rightArrowButt.clicked.connect(lambda: swap_handler(self.layer_num, 1))
        self.deleteButt.clicked.connect(lambda: delete_handler(self.layer_num))
        if duplicate_handler:
            self.duplicateButt.clicked.connect(lambda: duplicate_handler(self.layer_num))
        else:
            self.duplicateButt.setEnabled(False)

        # === FORM ===
        form = QtWidgets.QFormLayout()
        form.setLabelAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        form.setFormAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        form.setHorizontalSpacing(10)
        form.setVerticalSpacing(8)
        cardLay.addLayout(form)

        def dspin(minv, maxv, step, decimals=6, suffix=""):
            sp = QtWidgets.QDoubleSpinBox(card)
            sp.setRange(minv, maxv)
            sp.setDecimals(decimals)
            sp.setSingleStep(step)
            if suffix:
                sp.setSuffix(" " + suffix)
            sp.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons)
            sp.setMaximumWidth(130)
            return sp

        # Valores iniciales
        self.mur = mur
        self.er = er
        self.sigma = sigma
        self.layer_width = width
        self.layer_num = layer_num
        self.name = name
        self.connected = True

        # Campos
        self.mu_spin = dspin(0, 1e6, 0.1, 2)         # μr
        self.er_spin = dspin(0, 1e6, 0.1, 2)         # εr
        self.loss_spin = dspin(0, 1e12, 0.1, 2)      # σ (S/m) o εi (rel)
        self.width_spin = dspin(0, 1e9, 0.01, 2)     # d

        self.loss_kind_CB = QtWidgets.QComboBox(card)
        self.loss_kind_CB.addItems(["σ (S/m)", "εi (rel.)"])

        # d + unidad
        d_box = QtWidgets.QHBoxLayout()
        d_box.setSpacing(2)
        d_box.addWidget(self.width_spin)
        self.width_unit_CB = QtWidgets.QComboBox(card)
        self.width_unit_CB.addItems(["λs", "mm"])
        self.width_unit_CB.setMinimumWidth(60)
        d_box.addWidget(self.width_unit_CB)
        d_box.addStretch()

        # Nombre
        self.layer_name_input = QtWidgets.QLineEdit(card)
        self.layer_name_input.setPlaceholderText("Nombre de la capa")

        # Poner filas
        form.addRow("μr", self.mu_spin)
        form.addRow("εr", self.er_spin)
        row_loss = QtWidgets.QHBoxLayout()
        row_loss.addWidget(self.loss_spin)
        row_loss.addWidget(self.loss_kind_CB)
        row_loss.addStretch()
        form.addRow("loss", row_loss)
        self.width_label = QtWidgets.QLabel("d", card)
        form.addRow(self.width_label, d_box)
        form.addRow("name", self.layer_name_input)

        # Inicialización de valores
        self.mu_spin.setValue(float(mur))
        self.er_spin.setValue(float(er))
        self.width_spin.setValue(float(width))
        self.width_unit_CB.setCurrentIndex(1 if width_unit == 'mm' else 0)
        self.layer_name_input.setText(name)

        # Por compatibilidad: arrancar con σ
        self.loss_kind_CB.setCurrentIndex(0)
        self.loss_spin.setValue(float(sigma))
        self.set_type(layer_type)

        # Eventos
        self.enabledCheck.toggled.connect(self.setConnected)

        self._editables = [
            self.mu_spin,
            self.er_spin,
            self.loss_spin,
            self.loss_kind_CB,
            self.width_spin,
            self.width_unit_CB,
            self.layer_name_input,
        ]

    # ---- Lógica de estado / datos ----
    def setConnected(self, en: bool):
        """Habilita/inhabilita SOLO los campos editables de esta capa y cambia el look del card."""
        self.connected = en

        # Solo campos editables (flechas/tacho/duplicar/checkbox quedan activos siempre)
        for w in getattr(self, "_editables", []):
            w.setEnabled(en)

        if not en:
            # Estilo notorio al deshabilitar
            self.card.setStyleSheet("""
            QFrame#LayerCard {
                border: 2px dashed #e74c3c;
                border-radius: 12px;
                background: #1f1b1b;
            }
            """)
            if hasattr(self, "disabledChip"):
                self.disabledChip.show()
            # Apagar chip de tipo
            self.typeChip.setStyleSheet(
                "border-radius:10px; padding:2px 8px; color:white; font-weight:600; background:#555;"
            )
        else:
            # Restaurar estilo normal y color por tipo
            self.card.setStyleSheet(self._normal_card_css)
            if hasattr(self, "disabledChip"):
                self.disabledChip.hide()
            # Reaplicar color del chip según el tipo actual
            self.set_type(self.typeChip.text())

    def isConnected(self):
        return self.connected

    def set_type(self, layer_type):
        self.typeChip.setText(layer_type)
        color = {"Incidencia": "#3a6ea5", "Shield": "#6c6c6c", "Transmision": "#2b9a66"}.get(layer_type, "#6c6c6c")
        self.typeChip.setStyleSheet(
            f"border-radius:10px; padding:2px 8px; color:white; font-weight:600; background:{color};"
        )

        is_edge = layer_type in ("Incidencia", "Transmision")
        for w in (self.width_label, self.width_spin, self.width_unit_CB):
            w.setVisible(not is_edge)

    # ---- Exportar a Medium ----
    def to_medium(self):
        """
        Construye Medium respetando el selector de pérdidas:
          - Si 'σ': usa sigma_value y eps_i=0
          - Si 'εi': fuerza sigma=0 y anota eps_i en el Medium
        """
        sigma = self.sigma_value  # 0.0 si está en modo εi

        if self.width_unit_CB.currentText() == "mm":
            med = Medium(ur=self.mu_value, sigma=sigma, er=self.epsilon_value,
                         width=self.width_value * 1e-3)
        else:
            med = Medium(ur=self.mu_value, sigma=sigma, er=self.epsilon_value,
                         width_lambdas=self.width_value)

        med.loss_model = self.loss_kind
        med.eps_i = self.eps_i_value
        return med

    # --- getters usados por MainWindow ---
    @property
    def loss_kind(self) -> str:
        return 'sigma' if self.loss_kind_CB.currentIndex() == 0 else 'eps_i'

    @property
    def mu_value(self):
        return float(self.mu_spin.value())

    @property
    def epsilon_value(self):
        return float(self.er_spin.value())

    @property
    def sigma_value(self):
        if self.loss_kind == 'sigma':
            return float(self.loss_spin.value())
        return 0.0

    @property
    def eps_i_value(self):
        if self.loss_kind == 'eps_i':
            return float(self.loss_spin.value())
        return 0.0

    @property
    def width_value(self):
        return float(self.width_spin.value())

    @property
    def width_unit(self):
        return self.width_unit_CB.currentText()
