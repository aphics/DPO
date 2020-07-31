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
import matplotlib

import numpy as np

from AbrirFITS import AbrirArchivoFITS

# print(matplotlib.__version__)


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
        print(self.cubo.shape, 'shape cubo')
        self.labelNombreArchivo.setText(nombre_cubo)
        self.labelDimensionesArchivo.setText("x: " + str(self.dimensiones_cubo[0]) + ", y: "+ str(self.dimensiones_cubo[1]) + ", z: " + str(self.dimensiones_cubo[2]))
        self.PrimerCanal.setText('1')
        self.Resolucion.setText('0.43')
        
        #Se hace click en el boton cargar pixel para obtener informacion
        #a traves del metodo cargarPixel
        self.boton_CargarPixel.clicked.connect(self.cargarPixel)
        self.grafica.canvas.ax.set_xlabel('Longitud de onda (Amstrong)')
        self.grafica.canvas.ax.set_ylabel('Cuentas')

        #Se carga imagen fits en el widget imagen
        imagen = np.zeros((self.dimensiones_cubo[1], self.dimensiones_cubo[0]))
        print(imagen.shape, 'shape')
        for i in range(self.dimensiones_cubo[0]):
            for j in range(self.dimensiones_cubo[1]):
                imagen[j,i] = np.sum(self.cubo[:,j,i])
        self.imagen.canvas.ax.imshow(imagen, vmin=0, vmax = np.mean(imagen)*80, origin = 'lower')
        # self.imagen.canvas.ax.get_xaxis().set_visible(False)
        # self.imagen.canvas.ax.get_yaxis().set_visible(False)
        self.imagen.canvas.draw()
        self.imagen.canvas.mpl_connect('button_press_event', self.click_imagen)
    
    #Click en imagen
    #Sirve para cambiar y graficar al pixel seleccionado directo desde imagen
    #Esto ocurre si el radioButton_imagen esta seleccionado
    def click_imagen(self, event):
        if self.radioButton_imagen.isChecked() and event.button == 1:
            self.pixel_x.setText(str(int(event.xdata)))
            self.pixel_y.setText(str(int(event.ydata)))
            self.cargarPixel()
        else:
            pass



        
    # Se carga informacion del pixel           
    def cargarPixel(self):
        # px_x = self.dimensiones_cubo[0] - int(self.pixel_x.text())
        self.px_x = int(self.pixel_x.text())
        # px_y = self.dimensiones_cubo[1] - int(self.pixel_y.text())
        self.px_y = int(self.pixel_y.text())
        # Datos del pixel
        pixel = self.cubo[:, self.px_y, self.px_x]
        # Arreglo lambda para graficar el eje X
        lambda_x = [ float(self.PrimerCanal.text()) + n*float(self.Resolucion.text()) for n in range(len(pixel))]
        self.grafica.canvas.ax.clear()
        self.grafica.canvas.ax.set_xlabel('Longitud de onda (Amstrong)')
        self.grafica.canvas.ax.set_ylabel('Cuentas')
        self.grafica.canvas.ax.plot(lambda_x, pixel)
        self.grafica.canvas.ax.grid(True)
        self.grafica.canvas.draw()
    

    # Evento al momento de cerrar la ventana
    def closeEvent(self, evento):
        mensaje_cerrar = QMessageBox.question(self, "Salir ...", "Seguro que quieres salir de la aplicacion?", QMessageBox.Yes | QMessageBox.No)
        if mensaje_cerrar == QMessageBox.Yes: evento.accept()
        else: evento.ignore()

        
app = QApplication(sys.argv)
interface_dpo = VentanaPrincipal()
interface_dpo.show()
app.exec_()