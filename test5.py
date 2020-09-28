import sys
import os
import random
import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QGridLayout, QFileDialog, QPushButton

from numpy import arange
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MyMplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig = fig ###
        self.axes = fig.add_subplot(111)

        self.plotted_line = None

        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class MyDynamicMplCanvas(MyMplCanvas):
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def compute_initial_figure(self):
        self.plotted_line, = self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'b')
        self.axes.autoscale(enable=False)

    def update_figure(self):
        l = [random.randint(0, 10) for i in range(4)]
        self.axes.cla()
        self.axes.plot([0, 1, 2, 3], l, 'b')
        self.draw()


class P1(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(P1, self).__init__(parent)
        layout = QGridLayout(self)

        self.plot_canvas = MyDynamicMplCanvas(self, width=5, height=4, dpi=100)
        self.navi_toolbar = NavigationToolbar(self.plot_canvas, self)


        layout.addWidget(self.plot_canvas, 1, 1, 1, 1)
        layout.addWidget(self.navi_toolbar, 2, 1, 1, 1)



class MainWindow(QtWidgets.QMainWindow):    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.stack = QtWidgets.QStackedWidget(self)
        P1f = P1(self)
        self.stack.addWidget(P1f)
        self.setCentralWidget(self.stack)


if __name__ == '__main__':
    qApp = QtWidgets.QApplication(sys.argv)
    aw = MainWindow()
    aw.show()
    sys.exit(qApp.exec_())