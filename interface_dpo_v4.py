"""
Creado el 2 de diciembre del 2020

Autor: Edgar Sandoval Trejo

Archivo principal que instancia las demas clases
"""

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QVBoxLayout, QSpinBox
from PyQt5 import uic

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import matplotlib.pyplot as plt 
import matplotlib

import numpy as np 

from scipy.optimize import minimize

from AbrirFITS import AbrirArchivoFITS
from pestana_1 import visualizacion


print('version matplotlib: ', matplotlib.__version__)



class VentanaPrincipal(QMainWindow, visualizacion):

    # Metodo constructor
    def __init__(self):

        QMainWindow.__init__(self)
        # Se carga la plantilla. Archivo ui
        self.interface = uic.loadUi('interface_dpo_v3.ui', self)
        
        # Se fija el tamano maximo y minimo de la venta
        self.setMinimumSize(1200, 770)
        self.setMaximumSize(1200, 770)

        # Se pide al usuario seleccionar el archivo fits desde el inicio
        # Se instancia la clase AbrirArchivoFits
        abrir_archivo = AbrirArchivoFITS()
        # Se ocupa el metodo Archivo para abrir el archivo fits
        # Este regresa las simensiones del cubo, el cubo y el nombre del cubo
        info_FITS = abrir_archivo.Archivo()
        self.dims = info_FITS[0][::-1]
        self.name = info_FITS[2][::-1].split('/')[0][::-1]
        self.cubo = info_FITS[1]

        # Se usa el metodo mostrar_info_cubo para mostrar la info 
        # del cubo en la interface
        self.mostrar_info_cubo()
        # mostrar_info_cubo(self.interface, self.name)

        # ---------------------------------------------------

        # Inicializa la primera pestana
        # visualizacion(self.interface, self.cubo, self.dims)

        self.visual = visualizacion(self.interface, self.cubo, self.dims)

    #     self.interface.vis_canal.valueChanged.connect(self.cambio)

    # def cambio():
    #     self.visual.cambiar_canal()

        # ----------------------------------------------------



# class mostrar_info_cubo():
#     def __init__(self, interface, nombre):
#         interface.labelNombreArchivo.setText(nombre)
#         print('notino')

    # Metodo que muestra la informacion del cubo en las etiquetas de la interface
    def mostrar_info_cubo(self):
        # Muestra el nombre del archivo
        self.labelNombreArchivo.setText(self.name)
        # Muestra las dimensiones del archivo
        self.labelDimensionesArchivo.setText(str("x: {}, y: {}, z: {}".format(
            self.dims[0], self.dims[1], self.dims[2])))
        # Muestra la lambda en Angstroms del primer canal. Por default 1
        # Posteriormente se le solicita al usuario modificar este valor
        self.PrimerCanal.setText('1')
        # Muestra la resolucion de cada canal. Por default 0.43 Angstroms
        # Posteriormente se le solicita al usiario modificar este valor
        self.Resolucion.setText('0.43')

app = QApplication(sys.argv)
programa = VentanaPrincipal()
programa.show()
app.exec()