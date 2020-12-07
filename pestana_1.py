"""
Creado el 2 de diciembre del 2020

Autor: Edgar Sandoval Trejo

En este archivo se encuentra la clase y los metodos que inicializan la 
pestana 1 (visualizacion)

"""

import numpy as np

# Clase que inicializa la pestana visualizacion_cubo
class visualizacion():

    # Metodo constructor. Necesita la interface, el cubo y sus dimensiones
    # Estas son pasadas desde la clase VentanaPrincipal
    def __init__(self, interface, cubo, dims):
        self.interface = interface
        self.cubo = cubo
        self.dims = dims

        # Se construye la imagen del cubo sumado mediante el metodo cubo_sumado
        self.cubo_suma = self.cubo_sumado()

        # Se visualiza el primer canal con el metodo primer_canal
        self.primer_canal()

        # -------------------------------------------------------
        # Widgets de accion
        print('widgets de accion')

        self.interface.vis_canal.valueChanged.connect(self.cambiar_canal)

    # Metodo que construye la imagen del cubo sumado sobre los canales (eje Z)
    def cubo_sumado(self):
        suma = np.zeros((self.dims[1], self.dims[0]))
        for i in range(self.dims[0]):
            for j in range(self.dims[1]):
                suma[j,i] = np.sum(self.cubo[:,j,i])
        print('calculo del cubo')
        return suma

    # Metodo que permite visualizar el primer canal en la pestana
    def primer_canal(self):
        # Se establece el numero maximo de canales
        self.interface.vis_canal.setMaximum(self.dims[2])

        # Se muestra el primer canal
        self.interface.visualizacion_cubo.canvas.ax.imshow(
            self.cubo[1,:,:], vmin=0, vmax=np.mean(self.cubo[1,:,:]*80),
            origin='lower')
        self.interface.visualizacion_cubo.canvas.draw()

        # Visualiza el min y max del primer canal en interface
        self.interface.label_val_min.setText('Min: ' + str(
            format(np.min(self.cubo[1,:,:]), '0.2f')))
        self.interface.label_val_max.setText('Max: ' + str(
            format(np.max(self.cubo[1,:,:]), '0.2f')))

        # Calculo del limite del canal 1 y del cubo suma. Valores iniciales
        self.umbral_canal = 0
        self.limite_canal = int(format(np.mean(self.cubo[1,:,:])*80, '0.0f'))
        self.umbral_suma = 0
        self.limite_suma = int(format(np.mean(self.cubo_suma)*80, '0.0f'))

        # Se visualiza en interface valor del umbral y limite
        # del primer canal y cubo suma. Valores iniciales
        self.interface.umbral_cubo.setText(str(self.umbral_canal))
        self.interface.limite_cubo.setText(str(self.limite_canal))
        self.interface.umbral_cubo_suma.setText(str(self.umbral_suma))
        self.interface.limite_cubo_suma.setText(str(self.limite_suma))
        print('calculo primer canal')
    
    # Metodo que cambia la imagen dependiendo del canal seleccionado
    def cambiar_canal(self):
        print('entra cambiar canal')
        # Diccionario con los diferentes mapas de colores
        self.colormap_dic = {'Viridis': 'viridis', 'Grises': 'Greys', 
            'Grises R': 'Greys_r', '12C - 1': 'Paired', '12C - 2': 'Set3',
            '20C': 'tab20c', 'Cividis': 'cividis', 'Plasma': 'plasma'}
        # Mapa de color seleccionado
        self.colormap_selec = self.colormap_dic[
            self.interface.colormap_cubo.currentText()]
        print('entra 1')
        # Si esta activado del modo de visualizacion por canal
        if self.interface.vista_modo_canal.isChecked():
            # self.canal toma el valor que se muestra en la interface
            # Se resta 1 debido a que el arreglo de python empieza en 0
            self.canal = int(self.interface.vis_canal.value())-1

            # Para que no ocurra problemas en que el valor del umbral este por 
            # encima del valor limite se hace una revision del valor
            # Si el valor del limite esta por debajo del valor umbral,
            # se cambia el valor limite por el valor umbral +1
            if (int(self.interface.limite_cubo.text()) <= 
                int(self.interface.umbral_cubo.text())):
                self.interface.limite_cubo.setText(
                    str(int(self.interface.umbral_cubo.text()+1)))
            
            # Se muestra la imagen

            # Se obtienen los valores umbral y limite de la interface
            self.cuentas_min_canal = int(self.interface.umbral_cubo.text())
            self.cuentas_max_canal = int(self.interface.limite_cubo.text())
            # Se grafica la imagen
            self.interface.visualizacion_cubo.canvas.ax.imshow(
                self.cubo[self.canal,:,:], cmap=self.colormap_selec,
                vmin=self.cuentas_min_canal, vmax=self.cuentas_max_canal,
                origin='lower')
            self.interface.visualizacion_cubo.canvas.draw()
            # Se muestra en interface el valor min y max del canal mostrado
            self.interface.label_val_min.setText(
                'Min: ' + str(format(
                np.min(self.cubo[self.canal,:,:]), '0.2f')))