# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 15:15:33 2020

@author: aphics
"""


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QVBoxLayout
from PyQt5 import uic

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import numpy as np

from AbrirFITS import AbrirArchivoFITS


class VentanaPrincipal(QMainWindow, object):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("interface_dpo.ui", self)
        self.setMinimumSize(1200,600)
        #Para cargar archivo con boton "Abrir archivo"
        #archivo = self.boton_abrir_archivo.clicked.connect(AbrirArchivoFITS)
        #Se pide al usuario seleccionar el archivo FITS desde el inicio
        #Se usa el modulo AbrirArchivoFits
        abrir_archivo = AbrirArchivoFITS()
        info_FITS = abrir_archivo.Archivo()
        self.dimensiones_cubo = info_FITS[0][::-1]
        print(self.dimensiones_cubo)
        nombre_cubo = info_FITS[2][::-1].split('/')[0][::-1]
        self.cubo = info_FITS[1]
        self.labelNombreArchivo.setText(nombre_cubo)
        self.labelDimensionesArchivo.setText("x: " + str(self.dimensiones_cubo[0]) + ", y: "+ str(self.dimensiones_cubo[1]) + ", z: " + str(self.dimensiones_cubo[2]))
        
        #Se hace click en el boton cargar pixel para obtener informacion
        #a traves del metodo cargarPixel
        self.boton_CargarPixel.clicked.connect(self.cargarPixel)
        mpl_canvas111()
        
     
        
    # Se carga informacion del pixel           
    def cargarPixel(self):
        # px_x = self.dimensiones_cubo[0] - int(self.pixel_x.text())
        px_x = int(self.pixel_x.text())
        # px_y = self.dimensiones_cubo[1] - int(self.pixel_y.text())
        px_y = int(self.pixel_y.text())
        pixel = self.cubo[:, px_y, px_x]
        self.label_6.setText(str(pixel))
        
    # Evento al momento de cerrar la ventana
    def closeEvent(self, evento):
        mensaje_cerrar = QMessageBox.question(self, "Salir ...", "Seguro que quieres salir de la aplicacion?", QMessageBox.Yes | QMessageBox.No)
        if mensaje_cerrar == QMessageBox.Yes: evento.accept()
        else: evento.ignore()

class mpl_canvas111(FigureCanvas):
    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)
        self.grafico()
        print("grafico")
        plt.show()
    
    def grafico(self):
        X = list(range(50))
        Y = [x**2 for x in X]
        self.ax.plot(X, Y)
        
app = QApplication(sys.argv)
interface_dpo = VentanaPrincipal()
interface_dpo.show()
app.exec_()