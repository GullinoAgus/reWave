import os.path
from PyQt6 import QtWidgets
from PyQt6.QtCore import QEvent
from matplotlib.ticker import AutoLocator, FuncFormatter, LinearLocator, StrMethodFormatter
import numpy as np
from matplotlib import scale, rcParams
from matplotlib.axes import Axes
from matplotlib.backends.backend_qt import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle, PathPatch, Arc
from matplotlib.path import Path
from matplotlib.widgets import Cursor, MultiCursor
import mplcursors


class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        rcParams['axes.formatter.useoffset'] = False
        self.hspan = None
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig.set_constrained_layout(True)
        self.dataCursor = None
        self.leftPatch = None
        self.rigthPatch = None
        self.middlePatch = None
        self.wpcirclePatch = None

        # Eje inicial (se reemplaza al crear layouts 2 ó 3 paneles)
        self.axes: Axes = self.fig.add_subplot(111)
        self.axes2 = None
        self.axes3 = None

        super().__init__(self.fig)
        self.navToolBar = NavigationToolbar(self, parent)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.navToolBar)
        self.layout.addWidget(self)
        parent.layout().addLayout(self.layout)

        # Cursor inicial (se reemplaza por MultiCursor cuando se arma el layout múltiple)
        self.cursor = Cursor(self.axes, useblit=True,
                             color='gray', linestyle='--', linewidth=0.8)

        # Formato de ticks en Y
        self.y_locator = AutoLocator()
        self.y_formater = StrMethodFormatter('{x:.3f}')
        self.axes.yaxis.set_major_locator(self.y_locator)
        self.axes.yaxis.set_major_formatter(self.y_formater)
        self.axes.format_coord = format_coord_piola
        self.title_size = 10

    def resizeEvent(self, event):
        self.fig.set_constrained_layout(True)
        self.fig.canvas.draw()
        super().resizeEvent(event)

    def plot_efficiency(self, x, EA, unit: str, ylims=None, xlims=None):
        self.axes.clear()
        self.axes.format_coord = format_coord_piola

        line1 = self.axes.plot(x, EA, label="Eficiencia de apantallamiento")
        self.axes.yaxis.set_major_locator(self.y_locator)
        self.axes.yaxis.set_major_formatter(self.y_formater)
        #self.axes.legend()
        self.fig.set_constrained_layout(True)

        self.dataCursor = mplcursors.cursor(line1, hover='Transient')
        self.axes.set_xscale('linear')
        self.axes.set_yscale('linear')
        self.axes.grid(which='both')
        self.axes.set_xlabel(f'{unit}')
        self.axes.set_ylabel('Eficiencia [dB]')

        if hasattr(ylims, '__iter__'):
            self.axes.set_ylim(ylims[0], ylims[1])

        if hasattr(xlims, '__iter__'):
            self.axes.set_xlim(xlims[0], xlims[1])
        else:
            xlims = self.axes.get_xlim()
            self.axes.set_xlim(xlims[0], xlims[1])

        self.fig.canvas.draw()

    def plot_efficiency_with_components(self, x, SE_total, R, A, M, unit='Frecuencia [Hz]', ylims=None, xlims=None):
        """Plotea SE total y sus componentes R, A, M"""
        self.axes.clear()
        self.axes.format_coord = format_coord_piola
        
        # Plotear SE total y componentes con plot normal (no semilogx)
        line1 = self.axes.plot(x, SE_total, 'b-', linewidth=2, label='SE Total')
        line2 = self.axes.plot(x, R, 'r--', linewidth=1.5, label='R (Reflexion)')
        line3 = self.axes.plot(x, A, 'g--', linewidth=1.5, label='A (Absorcion)')
        line4 = self.axes.plot(x, M, 'm--', linewidth=1.5, label='M (Refl. Multiple)')
        
        # Configuración igual que plot_efficiency
        self.axes.yaxis.set_major_locator(self.y_locator)
        self.axes.yaxis.set_major_formatter(self.y_formater)
        self.axes.legend()
        self.fig.set_constrained_layout(True)

        # Data cursor para todas las líneas
        all_lines = line1 + line2 + line3 + line4
        self.dataCursor = mplcursors.cursor(all_lines, hover='Transient')
        
        # Escalas lineales (igual que plot_efficiency)
        self.axes.set_xscale('linear')
        self.axes.set_yscale('linear')
        self.axes.grid(which='both')
        self.axes.set_xlabel(f'{unit}')
        self.axes.set_ylabel('Eficiencia [dB]')

        # Límites (igual que plot_efficiency)
        if hasattr(ylims, '__iter__'):
            self.axes.set_ylim(ylims[0], ylims[1])

        if hasattr(xlims, '__iter__'):
            self.axes.set_xlim(xlims[0], xlims[1])
        else:
            xlims = self.axes.get_xlim()
            self.axes.set_xlim(xlims[0], xlims[1])

        self.fig.canvas.draw()

    def init_plot_layout(self, n_plots: int):
        """
        Crea la disposición de ejes según n_plots:
          - 3: izquierda (2 filas: R y T) + derecha (A) ocupando toda la altura
          - 2: 1 columna, 2 filas (arriba y abajo, mitad y mitad)
        """
        if n_plots not in (2, 3):
            raise ValueError("n_plots debe ser 2 o 3.")

        # Limpiar figura y armar grilla
        self.fig.clear()

        if n_plots == 3:
            gs = self.fig.add_gridspec(
                nrows=2, ncols=2,
                width_ratios=[1.0, 1.15],   # un poco más ancho el panel derecho
                height_ratios=[1, 1],
                wspace=0.04, hspace=0.04
            )
            self.axes  = self.fig.add_subplot(gs[0, 0])                 # panel 1 (arriba-izq)
            self.axes2 = self.fig.add_subplot(gs[1, 0], sharex=self.axes)  # panel 2 (abajo-izq)
            self.axes3 = self.fig.add_subplot(gs[:, 1], sharex=self.axes)  # panel 3 (derecha)
            axes_list = [self.axes, self.axes2, self.axes3]
        else:  # n_plots == 2
            gs = self.fig.add_gridspec(
                nrows=2, ncols=1,
                height_ratios=[1, 1],
                hspace=0.04
            )
            self.axes  = self.fig.add_subplot(gs[0, 0])  # arriba
            self.axes2 = self.fig.add_subplot(gs[1, 0], sharex=self.axes)  # abajo
            self.axes3 = None
            axes_list = [self.axes, self.axes2]

        # Formateadores base y coord formatter
        for ax in axes_list:
            ax.yaxis.set_major_locator(self.y_locator)
            ax.yaxis.set_major_formatter(self.y_formater)
            ax.format_coord = format_coord_piola

        # MultiCursor en los ejes activos
        try:
            self.cursor = MultiCursor(
                canvas=self.fig.canvas,
                axes=axes_list,
                useblit=True,
                color='gray', linestyle='--', linewidth=0.8,
                horizOn=True, vertOn=True
            )
        except Exception:
            pass

    def plot_for_freq(self, x, y, y_labels, x_labels, unit: str, ylims=None, xlims=None):
        """
        x: array de X
        y: lista con 2 o 3 arrays [y1, y2, (y3)]
        y_labels: lista de etiquetas de eje Y por panel (len = len(y))
        x_labels: lista de títulos/labels por panel (len = len(y))
        unit: etiqueta del eje X
        """
        n = len(y)
        if n not in (2, 3):
            raise ValueError("El parámetro 'y' debe contener 2 o 3 series.")

        # Crear/asegurar layout adecuado
        self.init_plot_layout(n)
        axes_list = [self.axes, self.axes2] if n == 2 else [self.axes, self.axes2, self.axes3]

        # Limpiar ejes y setear formateadores
        for ax in axes_list:
            ax.clear()
            ax.format_coord = format_coord_piola

        # Graficar cada serie en su panel
        line_handles = []
        for i, ax in enumerate(axes_list):
            serie = y[i]
            label_panel = x_labels[i] if i < len(x_labels) else f"Serie {i+1}"
            lh = ax.plot(x, serie, label=label_panel)
            line_handles.append(lh)

            # Leyenda y estilos base
            #ax.legend(loc="best")
            ax.yaxis.set_major_locator(self.y_locator)
            ax.yaxis.set_major_formatter(self.y_formater)
            ax.set_xscale('linear')
            ax.set_yscale('linear')
            ax.grid(which='both')

            # Etiqueta de Y y título del panel
            if i < len(y_labels):
                ax.set_ylabel(y_labels[i])
            ax.set_title(label_panel, fontsize=self.title_size)

        # Etiquetas de X (solo en los ejes inferiores/derecha para evitar ruido)
        if n == 2:
            self.axes2.set_xlabel(f"{unit}")     # abajo
        else:
            self.axes2.set_xlabel(f"{unit}")     # abajo-izq
            self.axes3.set_xlabel(f"{unit}")     # derecha

        # Límites Y (mismos para todos si se pasa un par (ymin,ymax))
        if hasattr(ylims, '__iter__') and len(ylims) == 2:
            for ax in axes_list:
                ax.set_ylim(ylims[0], ylims[1])

        # Límites X (compartido por sharex)
        if hasattr(xlims, '__iter__') and len(xlims) == 2:
            for ax in axes_list:
                ax.set_xlim(xlims[0], xlims[1])
        else:
            xlims_auto = self.axes.get_xlim()
            for ax in axes_list:
                ax.set_xlim(xlims_auto[0], xlims_auto[1])

        # Data cursors (hover) para cada línea
        try:
            self.dataCursor = [mplcursors.cursor(lh, hover='Transient') for lh in line_handles]
        except Exception:
            self.dataCursor = None

        # Ajustes finales
        self.fig.set_constrained_layout(True)
        yticks = self.axes.get_yticklabels()
        if len(yticks):
            yticks[-1].set_visible(False)

        self.fig.canvas.draw_idle()

    def init_plot_coefs(self):
        """
        Disposición 2+1 clásica (compatibilidad):
          - Izquierda: 2 filas (arriba R, abajo T)
          - Derecha: A ocupa ambas filas
        """
        self.init_plot_layout(3)


def format_coord_piola(x, y):
    return '({:.3E}, {:.3E})'.format(x, y)


def calculate_ticks(ax, ticks, round_to=0.1, center=False):
    upperbound = np.ceil(ax.get_ybound()[1] / round_to)
    lowerbound = np.floor(ax.get_ybound()[0] / round_to)
    dy = upperbound - lowerbound
    fit = np.floor(dy / (ticks - 1)) + 1
    dy_new = (ticks - 1) * fit
    if center:
        offset = np.floor((dy_new - dy) / 2)
        lowerbound = lowerbound - offset
    values = np.linspace(lowerbound, lowerbound + dy_new, ticks)
    return values * round_to
