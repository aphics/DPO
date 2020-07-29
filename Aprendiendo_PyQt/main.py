# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 15:24:28 2020

@author: aphics
"""


import sys
from PyQt5 import QtWidgets


from PyQt5.QtWidgets import QApplication, QMainWindow
import design

class MyApp(QMainWindow, design.Ui_MainWindow):
    def __init(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.pushButton_plotData.clicked.connect(self.plot_data)
        
    def plot_data(self):
        x=ange(0, 10)
        y=range(0, 20, 2)
        self.plotWidget.canvas.ax.plot(x, y)
        self.plotWidget.canvas.draw()
        
app = QtWidgets.QApplication(sys.argv)
form = MyApp()
form.show()
app.exec_()