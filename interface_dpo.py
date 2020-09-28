# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 15:15:33 2020

@author: aphics
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

from AbrirFITS import AbrirArchivoFITS

# print(matplotlib.__version__)


class VentanaPrincipal(QMainWindow, object):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("interface_dpo.ui", self)
        self.setMinimumSize(1325,790)
        #Para cargar archivo con boton "Abrir archivo"
        #archivo = self.boton_abrir_archivo.clicked.connect(AbrirArchivoFITS)
        #Se pide al usuario seleccionar el archivo FITS desde el inicio
        #Se usa el modulo AbrirArchivoFits
        abrir_archivo = AbrirArchivoFITS()
        info_FITS = abrir_archivo.Archivo()
        self.dimensiones_cubo = info_FITS[0][::-1]
        nombre_cubo = info_FITS[2][::-1].split('/')[0][::-1]
        self.cubo = info_FITS[1]
        self.labelNombreArchivo.setText(nombre_cubo)
        self.labelDimensionesArchivo.setText("x: " + str(self.dimensiones_cubo[0]) + ", y: "+ 
                                                str(self.dimensiones_cubo[1]) + ", z: " + 
                                                str(self.dimensiones_cubo[2]))
        self.PrimerCanal.setText('1')
        self.Resolucion.setText('0.43')
        #Se calcula la imagen del cubo con canales sumados
        self.imagen_2d = np.zeros((self.dimensiones_cubo[1], self.dimensiones_cubo[0]))
        for i in range(self.dimensiones_cubo[0]):
            for j in range(self.dimensiones_cubo[1]):
                self.imagen_2d[j,i] = np.sum(self.cubo[:,j,i])

        #Se carga el primer canal del cubo en el pestana visualizador del cubo
        self.vis_canal.setMaximum(self.dimensiones_cubo[2])
        self.visualizacion_cubo.canvas.ax.imshow(self.cubo[1,:,:], 
                                    vmin=0, vmax = np.mean(self.cubo[1,:,:])*80, origin = 'lower')
        # self.visualizacion_cubo.canvas.draw()
        self.vis_canal.valueChanged.connect(self.cambiar_canal)
        self.colormap_cubo.activated.connect(self.cambiar_canal)
        self.label_val_min_cubo.setText('Val. min: ' + str(format(np.min(self.cubo[1,:,:]), '0.2f')))
        self.label_val_max_cubo.setText('Val. min: ' + str(format(np.max(self.cubo[1,:,:]), '0.2f')))
        self.umbral_cubo.setText('0')
        self.maximo_cubo.setText(str(format(np.mean(self.cubo[1,:,:])*80,'0.0f')))
        self.umbral_cubo.returnPressed.connect(self.cambiar_canal)
        self.maximo_cubo.returnPressed.connect(self.cambiar_canal)
        self.pushButton_actualizar_vis_cubo.clicked.connect(self.cambiar_canal)
        
        #Desactiva el grupo de parametros para visualizar el cubo en modo suma
        self.groupBox_vis_suma.setEnabled(False)
        #Fija valores minimo y maximo en las etiquetas del grupo de parametros del modo suma
        self.label_val_min_cubo_suma.setText('Val. min: ' + str(format(np.min(self.imagen_2d), '0.2f')))
        self.label_val_max_cubo_suma.setText('Val. max: ' + str(format(np.max(self.imagen_2d), '0.2f')))
        #Fija valores umbral y maximo en las etiquetas del grupo de parametros del modo suma
        self.umbral_cubo_suma.setText('0')
        self.maximo_cubo_suma.setText(str(format(np.mean(self.imagen_2d)*80, '0.0f')))
        #Activa la funcion cambiar_canal cada que se selecciona el modo canal o suma
        self.vista_modo_canal.toggled.connect(self.cambiar_canal)
        self.vista_modo_suma.toggled.connect(self.cambiar_canal)
        #Activa la funcion cambiar_canal cada que se da enter en el umbral, maximo, colormap o boton actualizar
        self.umbral_cubo_suma.returnPressed.connect(self.cambiar_canal)
        self.maximo_cubo_suma.returnPressed.connect(self.cambiar_canal)
        self.pushButton_actualizar_vis_cubo_suma.clicked.connect(self.cambiar_canal)
        self.colormap_cubo_suma.activated.connect(self.cambiar_canal)

        #Para visualizar perfil del pixel en el modo visualizador del cubo
        self.visualizacion_cubo.canvas.mpl_connect('motion_notify_event', self.vis_perfil_grafica)
        








        
        #Se hace click en el boton cargar pixel para obtener informacion
        #a traves del metodo cargarPixel
        self.boton_CargarPixel.clicked.connect(self.cargarPixel)
        #Tambien se puede cargar el pixel al oprimir la tecla 'enter'
        self.pixel_x.returnPressed.connect(self.cargarPixel)        
        self.pixel_y.returnPressed.connect(self.cargarPixel)
        self.grafica.canvas.ax.set_xlabel('Longitud de onda (Angstrom)')
        self.grafica.canvas.ax.set_ylabel('Cuentas')
        #Tambien se puede cargar el pixel al oprimir la tecla 'enter'
        #de las entradas PrimerCanal y Resolucion
        self.PrimerCanal.returnPressed.connect(self.cargarPixel)
        self.Resolucion.returnPressed.connect(self.cargarPixel)

        #Se carga imagen fits en el widget imagen
        self.imagen.canvas.ax.imshow(self.imagen_2d, vmin=0, vmax = np.mean(self.imagen_2d)*80, origin = 'lower')
        # self.imagen.canvas.ax.get_xaxis().set_visible(False)
        # self.imagen.canvas.ax.get_yaxis().set_visible(False)
        self.imagen.canvas.draw()
        self.imagen.canvas.mpl_connect('button_press_event', self.click_imagen)
        self.imagen.canvas.mpl_connect('motion_notify_event', self.mouse_event_imagen)
        self.label_val_min_imagen.setText('Val. min: ' + str(format(np.min(self.imagen_2d), '0.2f')))
        self.label_val_max_imagen.setText('Val. max: ' + str(format(np.max(self.imagen_2d), '0.2f')))
        self.umbral.setText('0')
        self.maximo.setText(str(format(np.mean(self.imagen_2d)*80, '0.0f')))
        #Se actualiza la imagen con los valores de umbral y maximo ingresados
        self.pushButton_actualizar_umbral_imagen.clicked.connect(self.umbral_imagen)
        self.umbral.returnPressed.connect(self.umbral_imagen)
        self.maximo.returnPressed.connect(self.umbral_imagen)
        self.colormap_imagen.activated.connect(self.umbral_imagen)

    #Funcion para visualizar el perfil del pixel
    def vis_perfil_grafica(self, event):
        self.vis_x_coord = int(round(event.xdata, 0))
        self.vis_y_coord = int(round(event.ydata, 0))
        self.pixel_seleccionado = self.cubo[:, self.vis_y_coord, self.vis_x_coord]
        self.lambda_x = [float(self.PrimerCanal.text()) + n*float(self.Resolucion.text()) for n in range(len(self.pixel_seleccionado))]

        # if event.xdata == True:
        self.vis_perfil.canvas.ax.clear()
        self.vis_perfil.canvas.ax.plot(self.lambda_x, self.pixel_seleccionado)
        self.vis_perfil.canvas.ax.grid(True)
        self.vis_perfil.canvas.draw()
        
        # else:
        #     pass
        

    #Para cambiar los canales en la pestana de visualizacion del cubo
    def cambiar_canal(self):
        self.colormap_dic_vis = {'Viridis': 'viridis', 'Grices': 'Greys', 'Grices R': 'Greys_r', '12C - 1': 'Paired', '12C - 2': 'Set3',
                                '20C': 'tab20c', 'Cividis': 'cividis', 'Plasma': 'plasma'}
        
        #Si esta activado en modo visualizacion por canal
        if self.vista_modo_canal.isChecked():
            self.colormap_vis_cubo = self.colormap_dic_vis[self.colormap_cubo.currentText()]
            self.canal = int(self.vis_canal.value()) - 1
            try:
                self.cuentas_min_canal = int(self.umbral_cubo.text())
                self.cuentas_max_canal = int(self.maximo_cubo.text())
                self.label_val_min_cubo.setText('Val. min: ' + str(format(np.min(self.cubo[self.canal,:,:]), '0.2f')))
                self.label_val_max_cubo.setText('Val. max: ' + str(format(np.max(self.cubo[self.canal,:,:]), '0.2f')))
                self.visualizacion_cubo.canvas.ax.imshow(self.cubo[self.canal, :, :], cmap = self.colormap_vis_cubo,
                                        vmin=self.cuentas_min_canal, vmax = self.cuentas_max_canal, origin = 'lower')
                self.visualizacion_cubo.canvas.draw()
            except :
                pass
        
        #Si esta activado en modo visualiacion por suma
        if self.vista_modo_suma.isChecked():
            self.colormap_vis_cubo_suma = self.colormap_dic_vis[self.colormap_cubo_suma.currentText()]
            try:
                self.cuentas_min_vis_suma = int(self.umbral_cubo_suma.text())
                self.cuentas_max_vis_suma = int(self.maximo_cubo_suma.text())
                self.visualizacion_cubo.canvas.ax.imshow(self.imagen_2d, cmap = self.colormap_vis_cubo_suma,
                                        vmin = self.cuentas_min_vis_suma, vmax = self.cuentas_max_vis_suma, origin = 'lower')
                self.visualizacion_cubo.canvas.draw()
            except :
                pass

    #Para mostrar las coordenadas del pixel cuando el mouse
    #se posicionea en la imagen
    def mouse_event_imagen(self, event):
        if event.xdata == None:
            self.label_coord_x_imagen.setText('  X: ')
            self.label_coord_y_imagen.setText('  Y: ')
            self.label_coord_valor.setText('Valor: None')
        else:
            self.label_coord_x_imagen.setText('  X: ' + str(int(round(event.xdata, 0))))
            self.label_coord_y_imagen.setText('  Y: ' + str(int(round(event.ydata, 0))))
            self.label_coord_valor.setText('Val: ' + str(round(self.imagen_2d[int(round(event.ydata, 0)), 
                                        int(round(event.xdata, 0))], 2)))
    
    #Click en imagen
    #Sirve para cambiar y graficar al pixel seleccionado directo desde imagen
    #Esto ocurre si el radioButton_imagen esta seleccionado
    def click_imagen(self, event):
        if self.radioButton_imagen.isChecked() and event.button == 1:
            self.pixel_x.setText(str(int(round(event.xdata, 0))))
            self.pixel_y.setText(str(int(round(event.ydata, 0))))
            self.cargarPixel()
        else:
            pass

    def umbral_imagen(self):
        self.colormap_dic = {'Viridis': 'viridis', 'Grices': 'Greys', 'Grices R': 'Greys_r', '12C - 1': 'Paired', '12C - 2': 'Set3',
                                '20C': 'tab20c', 'Cividis': 'cividis', 'Plasma': 'plasma'}
        self.colormap = self.colormap_dic[self.colormap_imagen.currentText()]
        try:
            self.cuentas_min_imagen = int(self.umbral.text())
            self.cuentas_max_imagen = int(self.maximo.text())

            self.imagen.canvas.ax.imshow(self.imagen_2d, cmap = self.colormap, 
                                            vmin=self.cuentas_min_imagen, vmax = self.cuentas_max_imagen, origin = 'lower')
            self.imagen.canvas.draw()
        except:
            pass


    # Se carga informacion del pixel             
    def cargarPixel(self):
        try:
            # if self.pixel_x.text() != '' and self.pixel_y.text() != '' and int(self.PrimerCanal.text()) == int and type(float(self.Resolucion.text())) == float:
            # px_x = self.dimensiones_cubo[0] - int(self.pixel_x.text())
            self.px_x = int(self.pixel_x.text())
            # px_y = self.dimensiones_cubo[1] - int(self.pixel_y.text())
            self.px_y = int(self.pixel_y.text())
            # Datos del pixel
            pixel = self.cubo[:, self.px_y, self.px_x]
            
            # Arreglo lambda para graficar el eje X
            lambda_x = [ float(self.PrimerCanal.text()) + n*float(self.Resolucion.text()) for n in range(len(pixel))]
            self.grafica.canvas.ax.clear()
            self.grafica.canvas.ax.set_xlabel('Longitud de onda (Angstrom)')
            self.grafica.canvas.ax.set_ylabel('Cuentas')
            self.grafica.canvas.ax.plot(lambda_x, pixel)
            self.grafica.canvas.ax.grid(True)
            self.grafica.canvas.draw()
        except:
            pass        

    # Evento al momento de cerrar la ventana
    def closeEvent(self, evento):
        mensaje_cerrar = QMessageBox.question(self, "Salir ...", "Seguro que quieres salir de la aplicacion?", QMessageBox.Yes | QMessageBox.No)
        if mensaje_cerrar == QMessageBox.Yes: evento.accept()
        else: evento.ignore()

        
app = QApplication(sys.argv)
interface_dpo = VentanaPrincipal()
interface_dpo.show()
app.exec_()