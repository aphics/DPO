# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 22:19:26 2020

@author: aphics
"""


import sys
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5 import uic

class Dialogo(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("radio-checkbox.ui", self)
        
        self.radio_value()
        self.boton.clicked.connect(self.radio_value)
        
        self.checkbox_state()
        self.boton.clicked.connect(self.checkbox_state)
        
    def radio_value(self):
        if self.python.isChecked():
            self.labelLenguaje.setText("Python ha sido seleccionado")
        elif self.php.isChecked():
            self.labelLenguaje.setText("PHP ha sido seleccionada")
        elif self.perl.isChecked():
            self.labelLenguaje.setText("Perl ha sido seleccionado")
        elif self.ruby.isChecked():
            self.labelLenguaje.setText("Ruby ha sido seleccionado")
        else:
            self.labelLenguaje.setText("No ha seleccionado ningun lenguaje")
    
    def checkbox_state(self):
        self.labelTerminos.setStyleSheet("color: black")
        if self.checkBox.isChecked():
            self.labelTerminos.setText("Has aceptado los terminos")
            self.labelTerminos.setStyleSheet("color: green")
        else:
            self.labelTerminos.setText("No has aceptado los terminos")
            self.labelTerminos.setStyleSheet("color: red")

app = QApplication(sys.argv)
dialogo = Dialogo()
dialogo.show()
app.exec_()