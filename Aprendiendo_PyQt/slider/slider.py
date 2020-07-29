# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 20:37:26 2020

@author: aphics
"""


import sys
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5 import uic

class Dialogo(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("slider.ui", self)
        
        #Horizontal slider
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setSingleStep(1)
        self.horizontalSlider.setValue(50)
        #detectando cambios en la señal
        self.horizontalSlider.valueChanged.connect(self.getValueHorizontal)
        self.labelHorizontal.setText("50")
        
        #Vertical slider
        self.verticalSlider.setMinimum(0)
        self.verticalSlider.setMaximum(100)
        self.verticalSlider.setSingleStep(1)
        self.verticalSlider.setValue(50)
        #Detectando cambios en la señal
        self.verticalSlider.valueChanged.connect(self.getValueVertical)
        self.labelVertical.setText("50")
                
    
    def getValueHorizontal(self):
        value = self.horizontalSlider.value()
        self.labelHorizontal.setText(str(value))
        
    def getValueVertical(self):
        value = self.verticalSlider.value()
        self.labelVertical.setText(str(value))

app = QApplication(sys.argv)
dialogo = Dialogo()
dialogo.show()
app.exec_()
