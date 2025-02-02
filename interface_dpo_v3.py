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
# from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib
from scipy.optimize import minimize
import numpy as np

from AbrirFITS import AbrirArchivoFITS
from senal_ruido import buscador

from matplotlib.patches import Rectangle

print(matplotlib.__version__)


class VentanaPrincipal(QMainWindow, object):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("interface_dpo_v3.ui", self)
        self.setMinimumSize(1200,770)
        self.setMaximumSize(1200,770)
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
        #Se crea el arreglo con los canales sumados
        self.cubo_suma = np.zeros((self.dimensiones_cubo[1], self.dimensiones_cubo[0]))
        for i in range(self.dimensiones_cubo[0]):
            for j in range(self.dimensiones_cubo[1]):
                self.cubo_suma[j,i] = np.sum(self.cubo[:,j,i])

        #Se carga el primer canal del cubo en el pestana visualizador del cubo
        self.vis_canal.setMaximum(self.dimensiones_cubo[2])
        self.visualizacion_cubo.canvas.ax.imshow(self.cubo[1,:,:], 
                                    vmin=0, vmax = np.mean(self.cubo[1,:,:])*80, origin = 'lower')
        self.visualizacion_cubo.canvas.draw()
        self.vis_canal.valueChanged.connect(self.cambiar_canal)
        self.colormap_cubo.activated.connect(self.cambiar_canal)

        # Umbral y maximo del canal 1
        self.umbral_canal = 0
        self.limite_canal = int(format(np.mean(self.cubo[1,:,:])*80,'0.0f'))
        # Umbral y maximo de la suma
        self.umbral_suma = 0
        self.limite_suma = int(format(np.mean(self.cubo_suma)*80, '0.0f'))



        #Visualiza el valor del minimo y maximo del primer canal en la etiqueta
        self.label_val_min.setText('Min: ' + str(format(np.min(self.cubo[1,:,:]), '0.2f')))
        self.label_val_max.setText('Max: ' + str(format(np.max(self.cubo[1,:,:]), '0.2f')))
        #Visualiza el valor del umbral y limite del primer canal en la casilla
        self.umbral_cubo.setText(str(self.umbral_canal))
        self.limite_cubo.setText(str(self.limite_canal))
        # Visualiza el valor del umbral y limite del cubo suma en la casilla
        self.umbral_cubo_suma.setText(str(self.umbral_suma))
        self.limite_cubo_suma.setText(str(self.limite_suma))
        

        # Actualiza la imagen del cubo cuando se modifica el valor
        # umbral o maximo tanto en modo canal como modo suma
        self.umbral_cubo.returnPressed.connect(self.cambiar_canal)
        self.limite_cubo.returnPressed.connect(self.cambiar_canal)
        self.umbral_cubo_suma.returnPressed.connect(self.cambiar_canal)
        self.limite_cubo_suma.returnPressed.connect(self.cambiar_canal)
            
        #Parametros minimo y maximo del cubo sumado
        self.min_cubo_suma = np.min(self.cubo_suma)
        self.max_cubo_suma = np.max(self.cubo_suma)
        
        self.vista_modo_canal.toggled.connect(self.cambiar_canal)
        self.vista_modo_suma.toggled.connect(self.cambiar_canal)
        

        #Para visualizar perfil del pixel en el modo visualizador del cubo
        self.visualizacion_cubo.canvas.mpl_connect('button_press_event', self.vis_perfil_grafica_click)
        self.visualizacion_cubo.canvas.mpl_connect('motion_notify_event', self.vis_perfil_grafica_libre)
                
        #Se hace click en el boton cargar pixel para obtener informacion
        #a traves del metodo cargarPixel
        self.boton_CargarPixel.clicked.connect(self.cargarPixel)
        #Tambien se puede cargar el pixel al oprimir la tecla 'enter'
        self.pixel_x.returnPressed.connect(self.cargarPixel)        
        self.pixel_y.returnPressed.connect(self.cargarPixel)
        self.analisis_ajuste.canvas.ax.set_xlabel('Longitud de onda (Angstrom)')
        self.analisis_ajuste.canvas.ax.set_ylabel('Cuentas')
        self.analisis_ajuste.canvas.ax.patch.set_facecolor('lightgrey')
        #Tambien se puede cargar el pixel al oprimir la tecla 'enter'
        #de las entradas PrimerCanal y Resolucion
        self.PrimerCanal.returnPressed.connect(self.cargarPixel)
        self.Resolucion.returnPressed.connect(self.cargarPixel)

        # self.vis_perfil.canvas.ax.get_xaxis().set_visible(False)
        # self.vis_perfil.canvas.ax.get_yaxis().set_visible(False)

        # Funcion que carga el pixel en la pestana analisis al hacer click en el boton
        # Además cambia a la pestana analisis
        self.boton_analizar.clicked.connect(self.para_analizar)

        # Funcion que busca ajustar
        self.Ajustar.clicked.connect(self.ajustador)

    # Funcion que carga el pixel en la pestana de analisis
    # Ademas cambia a la pestana analisis
    def para_analizar(self, event):
        
        self.pixel_x.setText(self.pixel_x_vis.text())
        self.pixel_y.setText(self.pixel_y_vis.text())
        self.tabPrincipal.setCurrentIndex(1)
        self.cargarPixel()
                
    #Funcion para visualizar el perfil del pixel cuando se da click en un pixel
    def vis_perfil_grafica_click(self, event):
        try:
            self.rect = []
        except:
            pass
        if self.modo_click.isChecked():
            for x in range(1,3):
                self.vis_x_coord = int(round(event.xdata, 0))
                self.vis_y_coord = int(round(event.ydata, 0))
                self.pixel_seleccionado = self.cubo[:, self.vis_y_coord, self.vis_x_coord]
                self.lambda_x = [float(self.PrimerCanal.text()) + n*float(self.Resolucion.text()) for n in range(len(self.pixel_seleccionado))]
                # Se limpian los axes
                self.vis_perfil.canvas.ax1.clear()
                self.vis_perfil.canvas.ax2.clear()
                self.vis_perfil.canvas.ax3.clear()
                self.vis_perfil.canvas.ax4.clear()
                self.vis_perfil.canvas.ax5.clear()
                self.vis_perfil.canvas.ax6.clear()
                self.vis_perfil.canvas.ax7.clear()
                self.vis_perfil.canvas.ax8.clear()
                self.vis_perfil.canvas.ax9.clear()            
                # Se inicializa con el axes 5 ya que es el pixel central (a estudiar)
                self.vis_perfil.canvas.ax5.clear()
                self.vis_perfil.canvas.ax5.plot(self.lambda_x, self.pixel_seleccionado)
                self.vis_perfil.canvas.ax5.grid(True)
                # Se grafican los demas axes (perfiles alrededor)
                self.vis_perfil.canvas.ax1.plot(self.lambda_x, self.cubo[:, self.vis_y_coord+1, self.vis_x_coord-1])
                self.vis_perfil.canvas.ax2.plot(self.lambda_x, self.cubo[:, self.vis_y_coord+1, self.vis_x_coord])
                self.vis_perfil.canvas.ax3.plot(self.lambda_x, self.cubo[:, self.vis_y_coord+1, self.vis_x_coord+1])
                self.vis_perfil.canvas.ax4.plot(self.lambda_x, self.cubo[:, self.vis_y_coord, self.vis_x_coord-1])
                self.vis_perfil.canvas.ax6.plot(self.lambda_x, self.cubo[:, self.vis_y_coord, self.vis_x_coord+1])
                self.vis_perfil.canvas.ax7.plot(self.lambda_x, self.cubo[:, self.vis_y_coord-1, self.vis_x_coord-1])
                self.vis_perfil.canvas.ax8.plot(self.lambda_x, self.cubo[:, self.vis_y_coord-1, self.vis_x_coord])
                self.vis_perfil.canvas.ax9.plot(self.lambda_x, self.cubo[:, self.vis_y_coord-1, self.vis_x_coord+1])
                self.vis_perfil.canvas.ax1.set_title(str(self.vis_x_coord-1), size=18)
                self.vis_perfil.canvas.ax1.set_ylabel(str(self.vis_y_coord+1), size=18)
                self.vis_perfil.canvas.ax2.set_title(str(self.vis_x_coord), size=18)
                self.vis_perfil.canvas.ax3.set_title(str(self.vis_x_coord-1), size=18)
                self.vis_perfil.canvas.ax4.set_ylabel(str(self.vis_y_coord), size=18)
                self.vis_perfil.canvas.ax7.set_ylabel(str(self.vis_y_coord-1), size=18)
                
                self.vis_perfil.canvas.draw()
                self.pixel_x_vis.setText(str(self.vis_x_coord))
                self.pixel_y_vis.setText(str(self.vis_y_coord))
                self.rect = self.visualizacion_cubo.canvas.ax.add_patch( Rectangle((self.vis_x_coord-0.5, self.vis_y_coord-0.5), 1, 1, ec='r'))
        else:
            pass
    
    #Funcion para visualizar el perfil del pixel cuando se navega en la imagen    
    def vis_perfil_grafica_libre(self, event):
        if self.modo_libre.isChecked():
            try:
                self.vis_x_coord = int(round(event.xdata, 0))
                self.vis_y_coord = int(round(event.ydata, 0))
                self.pixel_seleccionado = self.cubo[:, self.vis_y_coord, self.vis_x_coord]
                self.lambda_x = [float(self.PrimerCanal.text()) + n*float(self.Resolucion.text()) for n in range(len(self.pixel_seleccionado))]
                # Se limpian los axes
                self.vis_perfil.canvas.ax1.clear()
                self.vis_perfil.canvas.ax2.clear()
                self.vis_perfil.canvas.ax3.clear()
                self.vis_perfil.canvas.ax4.clear()
                self.vis_perfil.canvas.ax5.clear()
                self.vis_perfil.canvas.ax6.clear()
                self.vis_perfil.canvas.ax7.clear()
                self.vis_perfil.canvas.ax8.clear()
                self.vis_perfil.canvas.ax9.clear()            
                # Se inicializa con el axes 5 ya que es el pixel central (a estudiar)
                self.vis_perfil.canvas.ax5.clear()
                self.vis_perfil.canvas.ax5.plot(self.lambda_x, self.pixel_seleccionado)
                self.vis_perfil.canvas.ax5.grid(False)
                # Se grafican los demas axes (perfiles alrededor)
                self.vis_perfil.canvas.ax1.plot(self.lambda_x, self.cubo[:, self.vis_y_coord+1, self.vis_x_coord-1])
                self.vis_perfil.canvas.ax2.plot(self.lambda_x, self.cubo[:, self.vis_y_coord+1, self.vis_x_coord])
                self.vis_perfil.canvas.ax3.plot(self.lambda_x, self.cubo[:, self.vis_y_coord+1, self.vis_x_coord+1])
                self.vis_perfil.canvas.ax4.plot(self.lambda_x, self.cubo[:, self.vis_y_coord, self.vis_x_coord-1])
                self.vis_perfil.canvas.ax6.plot(self.lambda_x, self.cubo[:, self.vis_y_coord, self.vis_x_coord+1])
                self.vis_perfil.canvas.ax7.plot(self.lambda_x, self.cubo[:, self.vis_y_coord-1, self.vis_x_coord-1])
                self.vis_perfil.canvas.ax8.plot(self.lambda_x, self.cubo[:, self.vis_y_coord-1, self.vis_x_coord])
                self.vis_perfil.canvas.ax9.plot(self.lambda_x, self.cubo[:, self.vis_y_coord-1, self.vis_x_coord+1])    
                self.vis_perfil.canvas.draw() 
            except:
                pass
        else:
            pass
                  

    #Para cambiar los canales en la pestana de visualizacion del cubo
    def cambiar_canal(self):
        self.colormap_dic = {'Viridis': 'viridis', 'Grises': 'Greys', 'Grises R': 'Greys_r', '12C - 1': 'Paired', '12C - 2': 'Set3',
                                '20C': 'tab20c', 'Cividis': 'cividis', 'Plasma': 'plasma'}
        self.colormap_vis = self.colormap_dic[self.colormap_cubo.currentText()]
        #Si esta activado en modo visualizacion por canal
        if self.vista_modo_canal.isChecked():            
            self.canal = int(self.vis_canal.value()) - 1
            if int(self.limite_cubo.text()) <= int(self.umbral_cubo.text()):
                self.limite_cubo.setText(str(int(self.umbral_cubo.text())+1))
            try:
                self.cuentas_min_canal = int(self.umbral_cubo.text())
                self.cuentas_max_canal = int(self.limite_cubo.text())
                self.label_val_min.setText('Min: ' + str(format(np.min(self.cubo[self.canal,:,:]), '0.2f')))
                self.label_val_max.setText('Max: ' + str(format(np.max(self.cubo[self.canal,:,:]), '0.2f')))
                self.visualizacion_cubo.canvas.ax.imshow(self.cubo[self.canal, :, :], cmap = self.colormap_vis,
                                        vmin=self.cuentas_min_canal, vmax = self.cuentas_max_canal, origin = 'lower')
                self.visualizacion_cubo.canvas.draw()
            except :
                pass
        
        #Si esta activado en modo visualiacion por suma
        if self.vista_modo_suma.isChecked():
            if int(self.limite_cubo_suma.text()) <= int(self.umbral_cubo_suma.text()):
                self.limite_cubo_suma.setText(str( int(self.umbral_cubo_suma.text())+1))
            try:
                self.cuentas_min_vis_suma = int(self.umbral_cubo_suma.text())
                self.cuentas_max_vis_suma = int(self.limite_cubo_suma.text())
                self.label_val_min.setText('Min: ' + str(format(self.min_cubo_suma, '0.2f')))
                self.label_val_max.setText('Max: ' + str(format(self.max_cubo_suma, '0.2f')))
                self.visualizacion_cubo.canvas.ax.imshow(self.cubo_suma, cmap = self.colormap_vis,
                                        vmin = self.cuentas_min_vis_suma, vmax = self.cuentas_max_vis_suma, origin = 'lower')
                self.visualizacion_cubo.canvas.draw()
            except :
                pass

    
    # Se carga informacion del pixel             
    def cargarPixel(self):
        try:
            self.px_x = int(self.pixel_x.text())
            self.px_y = int(self.pixel_y.text())
            self.pixel = self.cubo[:, self.px_y, self.px_x]
            # Arreglo lambda para graficar el eje X
            self.lambda_x = [ float(self.PrimerCanal.text()) + n*float(self.Resolucion.text()) for n in range(len(self.pixel))]
            self.analisis_ajuste.canvas.ax.clear()
            self.analisis_ajuste.canvas.ax.set_xlabel('Longitud de onda (Angstrom)')
            self.analisis_ajuste.canvas.ax.set_ylabel('Cuentas')
            self.analisis_ajuste.canvas.ax.plot(self.lambda_x, self.pixel, color='black', label='Datos')
            self.analisis_ajuste.canvas.ax.grid(True)
            self.analisis_ajuste.canvas.ax.tick_params(axis='x',rotation=45)
            self.analisis_ajuste.canvas.ax.legend()
            self.analisis_ajuste.canvas.ax.patch.set_facecolor('lightgrey')
            self.analisis_ajuste.canvas.draw()
        except:
            pass   
         
    # Funcion Gaussiana que se usa para ajustar
    def fit_gauss(self, x, p):
        A, mu, sigma = p
        return( A * np.exp(-(x-mu)*(x-mu)/(2.0*sigma*sigma)) )

    # Funcion que se usa para calcular una chi**2
    def main_fitter(self, p,x,y,ngauss):
        chi2 = 0
        model = np.zeros(np.array(y).shape)
        split_p = np.split(np.array(p),ngauss)      
        
        for g in range(ngauss):
            gp = split_p[g]
            if gp[0] <= 0:                  # evita amplitud negativa
                return 1e10
            if gp[2] <=0 or gp[2] >= 10:    # Limites en dispersion
                return 1e10
            else:
                model += self.fit_gauss(x,gp)

        chi2 = sum((y-model)**2 )
        return chi2

    def buscador(self, y):
        # -----------
        # Primer paso
        # -----------

        # Se calcula el promedio
        promedio = np.mean(y)

        # Se obtiene el maximo y su posicion
        maximo = max(y)
        # pos_max = y.index(maximo)
        pos_max = np.argmax(y)

        # Se crean los arreglos donde se almacena la senal y ruido. Primer paso
        senal_1_array = np.zeros_like(y)
        ruido_1_array = np.zeros_like(y)
        
        # Ciclo para diferenciar la senal del ruido. Primer paso

        # Condicion para saber si puede ser confiable la informacion
        if y[pos_max-1] > (0.75*promedio) and y[pos_max+1] > (0.75*promedio):
            pos = pos_max
            # Se busca hacia derecha a partir del maximo
            while pos <= len(y)-1:
                if y[pos] >= promedio:
                    senal_1_array[pos] = y[pos]
                if y[pos] < promedio and y[pos-1] > y[pos] and senal_1_array[pos-1] > 0:
                    senal_1_array[pos] = y[pos]
                pos += 1
            # Se busca hacia la izquierda a partir del maximo
            pos = pos_max

            while pos >= 0:
                if y[pos] >= promedio:
                    senal_1_array[pos] = y[pos]
                if y[pos] < promedio and y[pos+1] > y[pos] and senal_1_array[pos+1] > 0:
                    senal_1_array[pos] = y[pos]
                pos -= 1

        # Ciclo para crear el arreglo de ruido a partir del arreglo senal_1_array
        for i in range(len(senal_1_array)):
            if senal_1_array[i] == 0:
                ruido_1_array[i] = y[i]
            else:
                pass

        # Arreglos para almacenar unicamente la informacion de senal_1_array y ruido_1_array
        senal_1 = []
        ruido_1 = []
        # Ciclo para almacenar unicamente la informacion de senal_1_array y ruido_1_array
        for i in range(len(senal_1_array)):
            if senal_1_array[i] != 0:
                senal_1.append(senal_1_array[i])
            if ruido_1_array[i] != 0:
                ruido_1.append(ruido_1_array[i])

        # Calculo del continuo_1 y su desviacion estandar
        continuo_1 = np.mean(ruido_1)
        sigma_continuo_1 = np.sqrt( (1/(len(ruido_1)-1)) * np.sum( (ruido_1-np.mean(ruido_1))**2 ) )

        # -------------
        # Segundo paso
        # -------------

        # Se crean los arreglos donde se almacena la senal y ruido. Segundo paso
        senal_2_array = np.zeros_like(y)
        ruido_2_array = np.zeros_like(y)

        # Ciclo para separa senal_2 de ruido_2 a partir del valor del
        # valor del continuo_1 y la sigma del ruido_1
        # Se busca hacia la derecha a partir del maximo
        pos = pos_max
        while pos <= len(y)-1:
            if y[pos] >= continuo_1:
                senal_2_array[pos] = y[pos]
            if y[pos] < (continuo_1 + sigma_continuo_1):
                senal_2_array[pos] = y[pos]
                break
            if y[pos+1] > y[pos] and y[pos] <= (continuo_1 + (2*sigma_continuo_1)):
                senal_2_array[pos] = y[pos]
                break
            pos += 1
        
        # Se busca hacia la izquierda a partir del maximo
        pos = pos_max
        while pos >= 0:
            if y[pos] >= continuo_1:
                senal_2_array[pos] = y[pos]
            if y[pos] < (continuo_1 + sigma_continuo_1):
                senal_2_array[pos] = y[pos]
                break
            if y[pos-1] > y[pos] and y[pos] <= (continuo_1 + (2*sigma_continuo_1)):
                senal_2_array[pos] = y[pos]
                break
            pos -= 1
        
        # Ciclo para crear el arreglo de ruido_2_array a partir de senal_2_array
        for i in range(len(senal_2_array)):
            if senal_2_array[i] == 0 :
                ruido_2_array[i] = y[i]
            else:
                pass
        
        # Se crean arreglos para almacenar unicamente informacion de ruido_2_array y
        # ruido_2_array
        senal_2 = []
        ruido_2 = []

        # Ciclo para almacenar unicamente la informacion de senal_2_array y ruido_2_array
        for i in range(len(senal_2_array)):
            if senal_2_array[i] != 0:
                senal_2.append(senal_2_array[i])
            if ruido_2_array[i] != 0:
                ruido_2.append(ruido_2_array[i])

        # Calculo del continuo_2 a partir del ruido_2
        continuo_2 = np.mean(ruido_2)

        # Substraccion del continuo_2 a senal_2
        senal_2 = senal_2 - continuo_2
        
        # Promedio de senal_2
        senal = np.mean(senal_2)

        # Desviacion estandar de ruido_2
        sigma_ruido_2 = np.std(ruido_2, ddof =1)

        # Senal a ruido
        s_n = senal / sigma_ruido_2

        salida = [senal_2_array, ruido_2_array, continuo_2, s_n]

        return salida


    # Funcion usada para ajustar
    def ajustador(self):

        def plot_total(ptot, x, N):
            model_tot = np.zeros(np.array(x).shape)
            split_p = np.split(np.array(ptot),N)            
            for g in range(N):
                gp =  split_p[g]
                model_tot += self.fit_gauss(x,gp)            
            return model_tot
        
        # try:
        self.px_x = int(self.pixel_x.text())
        self.px_y = int(self.pixel_y.text())
        self.pixel = self.cubo[:, self.px_y, self.px_x]
        self.data = self.pixel[:]
        self.lambda_x = [ float(self.PrimerCanal.text()) + n*float(self.Resolucion.text()) for n in range(len(self.pixel))]

        self.limpio = self.buscador(self.pixel)
        self.pixel = self.limpio[0]
        self.ruido = self.limpio[1]
        self.zerolev = self.limpio[2]
        self.s_n = self.limpio[3]

        # Valores max y min para amplitud
        amp_min = self.zerolev
        amp_max = np.max(self.pixel)

        # Para obtener la media max y min para ajustar
        mu_min = 0
        mu_max = 0
        # Para buscar mu_min
        aux = 0
        while aux <= len(self.pixel):
            if self.pixel[aux] != 0:
                mu_min = self.lambda_x[aux] + (4* float(self.Resolucion.text()))
                break
            else:
                pass
            aux += 1
        # Para buscar mu_max
        aux = len(self.pixel)-1
        while aux > 0:
            if self.pixel[aux] != 0:
                mu_max = self.lambda_x[aux] - (4* float(self.Resolucion.text()))
                break
            else:
                pass
            aux -= 1

        self.pixel = self.pixel - self.zerolev

        self.iteraciones = 500
        self.Results = {}

        # Fijamos el valor maximo para la barra de progreso dependiendo del numero de iteraciones
        self.progressBar.setMaximum(self.iteraciones-1)


        for i in range(self.iteraciones):
            p0 = []
            for j in range(int(self.Ngauss.value())):
                p0.append(np.random.uniform( amp_min, amp_max ) )     #Amplitud
                p0.append(np.random.uniform(mu_min, mu_max))      #Media
                p0.append(np.random.uniform(1,10))      # Dispersion       
            
            fit = minimize(self.main_fitter, p0, method='Powell', options={'maxiter':15000, 'maxfev':15000, 'disp': False}, args=(self.lambda_x, self.pixel, int(self.Ngauss.value())))
            
            self.Results[fit.fun] = fit.x

            # Se actualiza el valor de la barra de progreso
            self.progressBar.setValue(i)
        
        best = min(self.Results.keys())
        best_fit = self.Results[best]
        
        # Ordenado de Gaussianas a partir de su amplitud
        ordenado = np.split(best_fit, self.Ngauss.value())
        ordenado.sort(key=lambda x: x[0])
        ordenado = ordenado[::-1]
        # Se crea un arreglo secundario        
        best_fit2 = []
        # Se agregan los parametros de cada gaussiana
        for i in range(len(ordenado)):
            for j in range(len(ordenado[i])):
                best_fit2.append(ordenado[i][j])
        # Se devuelve la informacion ordenada al arreglo original best_fit
        best_fit = np.array(best_fit2)

        self.pixel = self.pixel + self.zerolev
        # Convertir valores en nan
        for i in range(len(self.pixel)):
            if self.pixel[i] == 0:
                self.pixel[i] = float('nan')
            if self.ruido[i] == 0:
                self.ruido[i] = float('nan')


        col = ['purple', 'orange', 'cyan', 'lime']
        
        self.analisis_ajuste.canvas.ax.clear()
        self.analisis_ajuste.canvas.ax.plot(self.lambda_x, self.data, label='Datos', color='black')
        self.analisis_ajuste.canvas.ax.plot(self.lambda_x, self.pixel, 'o', label='Senal', color='green', markersize=4, alpha=0.5)
        self.analisis_ajuste.canvas.ax.plot(self.lambda_x, self.ruido, 'x', label='Ruido', color='red', markersize=4, alpha=0.5)

        for i, g in enumerate(np.split(np.array(best_fit),int(self.Ngauss.value()))):
            self.analisis_ajuste.canvas.ax.plot(self.lambda_x, self.fit_gauss(self.lambda_x,g) + self.zerolev, label=f'G{i+1}', color=col[i])

        model_tot = plot_total(best_fit,self.lambda_x,int(self.Ngauss.value()))
        self.analisis_ajuste.canvas.ax.plot(self.lambda_x, model_tot + self.zerolev, label='Ajustado')
        self.analisis_ajuste.canvas.ax.tick_params(axis='x',rotation=45)
        self.analisis_ajuste.canvas.ax.grid(True)
        self.analisis_ajuste.canvas.ax.set_xlabel('Longitud de onda (Angstrom)')
        self.analisis_ajuste.canvas.ax.set_ylabel('Cuentas')
        self.analisis_ajuste.canvas.ax.legend()
        self.analisis_ajuste.canvas.ax.patch.set_facecolor('lightgrey')
        self.analisis_ajuste.canvas.draw()

        # Para mostrar los parametros del ajuste en la interface
        # Primero se hace split en el arreglo que contiene los parametros
        # tambien ayuda para saber cuantas gaussianas se ajustaron
        self.parametros = np.split(best_fit, self.Ngauss.value())

        # Se crean listas con los QLineEdit de los parametros
        self.amplitudes = [self.a1, self.a2, self.a3, self.a4]
        self.medias = [self.m1, self.m2, self.m3, self.m4]
        self.dispersiones = [self.d1, self.d2, self.d3, self.d4]
        self.velocidades = [self.v1, self.v2, self.v3, self.v4]

        # Los QLineEdit debe de borrarse primero
        for i in range(4):
            self.amplitudes[i].setText('')
            self.medias[i].setText('')
            self.dispersiones[i].setText('')
            self.velocidades[i].setText('')
        
        c = 299792.458          # Velocidad de la luz en km/s

        # Se muestran en los QLineEdit los valores de los parametros
        for i, pars in enumerate(self.parametros):
            self.amplitudes[i].setText( str(format(pars[0], '0.2f')) )
            self.medias[i].setText(str(format(pars[1], '0.2f')))
            self.dispersiones[i].setText( str(format( pars[2]*c/6563 , '0.2f')))
            self.velocidades[i].setText( str( format( c*( (pars[1]/6563)-1) , '0.2f' ) ) )
        
        self.continuo.setText(str(format(self.zerolev, '0.2f')))
        self.senal_ruido.setText(str(format(self.s_n, '0.2f')))
        # except:
        #     pass
        

    # Evento al momento de cerrar la ventana
    def closeEvent(self, evento):
        mensaje_cerrar = QMessageBox.question(self, "Salir ...", "Seguro que quieres salir de la aplicacion?", QMessageBox.Yes | QMessageBox.No)
        if mensaje_cerrar == QMessageBox.Yes: evento.accept()
        else: evento.ignore()

app = QApplication(sys.argv)
interface_dpo = VentanaPrincipal()
interface_dpo.show()
app.exec_()
