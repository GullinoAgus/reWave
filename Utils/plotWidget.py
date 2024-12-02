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
from matplotlib.widgets import Cursor
import mplcursors
rcParams['axes.formatter.useoffset'] = False


class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.hspan = None
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.dataCursor = None
        self.leftPatch = None
        self.rigthPatch = None
        self.middlePatch = None
        self.wpcirclePatch = None
        self.axes: Axes = self.fig.add_subplot()
        self.fig.set_tight_layout(True)
        super().__init__(self.fig)
        self.navToolBar = NavigationToolbar(self, parent)
        parent.layout().addWidget(self.navToolBar)
        parent.layout().addWidget(self)
        self.cursor = Cursor(self.axes, useblit=True,
                             color='gray', linestyle='--', linewidth=0.8)
        self.y_locator = AutoLocator()
        self.y_formater = StrMethodFormatter('{y:.3f}')
        self.axes.yaxis.set_major_locator(self.y_locator)
        self.axes.yaxis.set_major_formatter(self.y_formater)

    def plot_effeciency(self, x, y, ylims=None, xlims=None):
        self.axes.clear()
        line = self.axes.plot(x, y)
        self.axes.yaxis.set_major_locator(self.y_locator)
        self.axes.yaxis.set_major_formatter(self.y_formater)
        self.dataCursor = mplcursors.cursor(line)

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

    def plot_gammas(self, x, y1, y2, ylims=None, xlims=None):
        self.axes.clear()
        line1 = self.axes.plot(
            x*180/np.pi, y1, label="$|\\Gamma_{{\\parallel}}|$")
        line2 = self.axes.plot(x*180/np.pi, y2, label="$|\\Gamma_{{\\perp}}|$")
        self.axes.yaxis.set_major_locator(self.y_locator)
        self.axes.yaxis.set_major_formatter(self.y_formater)
        self.dataCursor = [mplcursors.cursor(line1), mplcursors.cursor(line2)]

        self.axes.set_xscale('linear')
        self.axes.set_yscale('linear')
        self.axes.grid(which='both')
        self.axes.legend()
        self.axes.set_xlabel('Angulo de incidencia [$\\degree$]')
        self.axes.set_ylabel('$|\\Gamma|$')
        if hasattr(ylims, '__iter__'):
            self.axes.set_ylim(ylims[0], ylims[1])
        if hasattr(xlims, '__iter__'):
            self.axes.set_xlim(xlims[0], xlims[1])
        else:
            xlims = self.axes.get_xlim()
            self.axes.set_xlim(xlims[0], xlims[1])

        self.fig.canvas.draw()


def make_format(current, other):
    # current and other are axes
    def format_coord(x, y):
        # x, y are data coordinates
        # convert to display coords
        display_coord = current.transData.transform((x, y))
        inv = other.transData.inverted()
        # convert back to data coords with respect to ax
        ax_coord = inv.transform(display_coord)
        coords = [ax_coord, (x, y)]
        return ('Left: {:<}   Right: {:}'
                .format(*['({:.3E}, {:.3E})'.format(x, y) for x, y in coords]))

    return format_coord


def format_coord_complex(x, y):
    return "{:.2E} + j*({:.2E})".format(x, y)


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
