import os.path
from PyQt6 import QtWidgets
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
        self.fig.tight_layout()
        self.dataCursor = None
        self.leftPatch = None
        self.rigthPatch = None
        self.middlePatch = None
        self.wpcirclePatch = None
        self.axes: Axes = self.fig.add_subplot(111)
        self.axes2 = None
        super().__init__(self.fig)
        self.navToolBar = NavigationToolbar(self, parent)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.navToolBar)
        self.layout.addWidget(self)
        parent.layout().addLayout(self.layout)
        self.cursor = Cursor(self.axes, useblit=True,
                             color='gray', linestyle='--', linewidth=0.8)
        self.y_locator = AutoLocator()
        self.y_formater = StrMethodFormatter('{x:.3f}')
        self.axes.yaxis.set_major_locator(self.y_locator)
        self.axes.yaxis.set_major_formatter(self.y_formater)
        self.axes.format_coord = format_coord_piola

    def plot_effeciency(self, x, EA, ylims=None, xlims=None):
        self.axes.clear()
        self.axes.format_coord = format_coord_piola

        line1 = self.axes.plot(x, EA)
        self.axes.yaxis.set_major_locator(self.y_locator)
        self.axes.yaxis.set_major_formatter(self.y_formater)
        self.fig.tight_layout()

        self.dataCursor = mplcursors.cursor(line1, hover='Transient')
        self.axes.set_xscale('log')
        self.axes.set_yscale('linear')
        self.axes.grid(which='both')
        self.axes.set_xlabel('Frecuencia [GHz]')
        self.axes.set_ylabel('Eficiencia de apantallamiento [dB]')
        if hasattr(ylims, '__iter__'):
            self.axes.set_ylim(ylims[0], ylims[1])
        if hasattr(xlims, '__iter__'):
            self.axes.set_xlim(xlims[0], xlims[1])
        else:
            xlims = self.axes.get_xlim()
            self.axes.set_xlim(xlims[0], xlims[1])

        self.fig.canvas.draw()

    def plot_coefs(self, x, ref, trans, ylims=None, xlims=None):
        if self.axes2 == None:
            self.init_plot_coefs()
        self.axes.clear()
        self.axes2.clear()
        self.axes.format_coord = format_coord_piola
        self.axes2.format_coord = format_coord_piola
        self.fig.subplots_adjust(hspace=0.)

        line1 = self.axes.plot(
            x, ref, label="Coef. de Reflexion $\\vec{{S}}$")

        line2 = self.axes2.plot(
            x, trans, label="Coef. de Transmision de $\\vec{{S}}$")
        yticks = self.axes.get_yticklabels()
        self.fig.tight_layout()
        yticks[-1].set_visible(False)
        self.dataCursor = [mplcursors.cursor(
            line1, hover='Transient'), mplcursors.cursor(line2, hover='Transient')]
        self.axes.set_xscale('log')
        self.axes.set_yscale('linear')
        self.axes2.set_yscale('linear')
        self.axes.grid(which='both')
        self.axes2.grid(which='both')
        self.axes2.set_xlabel('Frecuencia [GHz]')
        self.axes.set_ylabel('Coeficientes de Reflexión [UA]')
        self.axes2.set_ylabel('Coeficientes de Transmisión [UA]')
        if hasattr(ylims, '__iter__'):
            self.axes.set_ylim(ylims[0], ylims[1])
        if hasattr(xlims, '__iter__'):
            self.axes.set_xlim(xlims[0], xlims[1])
        else:
            xlims = self.axes.get_xlim()
            self.axes.set_xlim(xlims[0], xlims[1])

        self.fig.canvas.draw()

    def plot_gammas(self, x, y1, y2, ylims=None, xlims=None):
        self.axes.clear()
        self.axes.format_coord = format_coord_piola

        line1 = self.axes.plot(
            x*180/np.pi, y1, label="$|\\Gamma_{{\\parallel}}|$")
        line2 = self.axes.plot(
            x*180/np.pi, y2, label="$|\\Gamma_{{\\perp}}|$")
        self.axes.yaxis.set_major_locator(self.y_locator)
        self.axes.yaxis.set_major_formatter(self.y_formater)
        self.dataCursor = [mplcursors.cursor(
            line1, hover='Transient'), mplcursors.cursor(line2, hover='Transient')]
        self.axes.grid(which='both')
        self.axes.legend()
        self.axes.set_xlabel('Angulo de incidencia [$\\degree$]')
        self.axes.set_ylabel('$|\\Gamma|$')
        self.fig.tight_layout()
        if hasattr(ylims, '__iter__'):
            self.axes.set_ylim(ylims[0], ylims[1])
        if hasattr(xlims, '__iter__'):
            self.axes.set_xlim(xlims[0], xlims[1])
        else:
            xlims = self.axes.get_xlim()
            self.axes.set_xlim(xlims[0], xlims[1])

        self.fig.canvas.draw()

    def init_plot_coefs(self):
        self.fig.clear()
        self.axes, self.axes2 = self.fig.subplots(
            2, 1, sharex=True, gridspec_kw={'hspace': 0})
        self.axes.get_yaxis().get_major_formatter()
        self.cursor = MultiCursor(canvas=self.fig.canvas, axes=[self.axes, self.axes2], useblit=True,
                                  color='gray', linestyle='--', linewidth=0.8, horizOn=True)


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
