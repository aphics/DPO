# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 16:33:40 2020

@author: aphics
"""


import sys
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5 import uic

class Dialogo(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("combobox.ui", self)
        self.boton.clicked.connect(self.getItem)
        # Para inicializarlo desde un principio
        self.getItem()
    
        # Para agregar un nuevo item
        self.lenguajes.addItem("C++")
        
        # Para eliminar un determinado elemento a traves del indice
        self.lenguajes.removeItem(0)
        
    # Para obtener el item seleccionado
    def getItem(self):
        item = self.lenguajes.currentText()
        self.labelLenguajes.setText("Has seleccionado: "+item)

app = QApplication(sys.argv)
dialogo = Dialogo()
dialogo.show()
app.exec_()
