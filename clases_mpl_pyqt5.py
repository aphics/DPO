from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class MplCanvas11(FigureCanvas):
    def __init__(self):
        self.fig = Figure(tight_layout=True)
        self.ax = self.fig.add_subplot(111)        
        FigureCanvas.__init__(self, self.fig)

class MatplotlibWidget11(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.canvas = MplCanvas11()
        self.vbl = QVBoxLayout()
        # self.vbl.addWidget(self.canvas)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.vbl.addWidget(self.toolbar)
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)

class MatplotlibWidget11_sin(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.canvas = MplCanvas11()
        self.vbl = QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)

class MplCanvas22(FigureCanvas):
    def __init__(self):
        self.fig = Figure()
        # self.fig = Figure(tight_layout=True)
        # self.fig = Figure(constrained_layout=True)
        self.ax1 = self.fig.add_subplot(221)
        self.ax2 = self.fig.add_subplot(222)
        self.ax3 = self.fig.add_subplot(223)
        self.ax4 = self.fig.add_subplot(224)
        # Para unir las graficas y hacer una malla
        # self.fig.subplots_adjust(hspace=0, wspace=0)
        FigureCanvas.__init__(self, self.fig)

class MatplotlibWidget22_sin(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.canvas = MplCanvas22()
        self.vbl = QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)

class MplCanvas33(FigureCanvas):
    def __init__(self):
        self.fig = Figure()
        # Se inicia con el axes 5 ya que es el pixel central (en estudio)
        self.ax5 = self.fig.add_subplot(335)
        self.ax5.get_xaxis().set_visible(False)
        self.ax5.get_yaxis().set_visible(False)
        self.ax1 = self.fig.add_subplot(331, sharex = self.ax5, sharey = self.ax5)
        self.ax1.get_xaxis().set_visible(False)
        self.ax2 = self.fig.add_subplot(332, sharex = self.ax5, sharey = self.ax5)
        self.ax2.get_xaxis().set_visible(False)
        self.ax2.get_yaxis().set_visible(False)
        self.ax3 = self.fig.add_subplot(333, sharex = self.ax5, sharey = self.ax5)
        self.ax3.get_xaxis().set_visible(False)
        self.ax3.get_yaxis().set_visible(False)
        self.ax4 = self.fig.add_subplot(334, sharex = self.ax5, sharey = self.ax5)
        self.ax4.get_xaxis().set_visible(False)
        self.ax6 = self.fig.add_subplot(336, sharex = self.ax5, sharey = self.ax5)
        self.ax6.get_xaxis().set_visible(False)
        self.ax6.get_yaxis().set_visible(False)
        self.ax7 = self.fig.add_subplot(337, sharex = self.ax5, sharey = self.ax5)
        self.ax8 = self.fig.add_subplot(338, sharex = self.ax5, sharey = self.ax5)
        self.ax8.get_yaxis().set_visible(False)
        self.ax9 = self.fig.add_subplot(339, sharex = self.ax5, sharey = self.ax5)
        self.ax9.get_yaxis().set_visible(False)        
        self.fig.subplots_adjust(hspace=0, wspace=0, left=0.08, right=.92, top=.92, bottom=0.08)
        FigureCanvas.__init__(self, self.fig)

class MatplotlibWidget33_visual(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.canvas = MplCanvas33()
        self.vbl = QVBoxLayout()
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.vbl.addWidget(self.toolbar)
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)





