# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 00:39:34 2020

@author: aphics
"""


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
from astropy.io import fits

class AbrirArchivoFITS(QWidget, object):

    def __init__(self):
        super().__init__()
        self.left = 10
        self.top = 10
        #Se obtiene informacion para centrar ventana
        resolucion = QApplication.desktop()
        resolucion_ancho = resolucion.width()
        resolucion_alto = resolucion.height()
        #Se fijan valores para centrar la ventana
        self.left = ( resolucion_ancho / 2 ) - ( self.frameSize().width() / 2 )
        self.top = ( resolucion_alto / 2 ) - ( self.frameSize().height() / 2 )
        self.width = 640
        self.height = 480        
        self.initUI()
    
    def initUI(self):
        self.setGeometry(self.left, self.top, self.width, self.height)        
        self.openFileNameDialog()
        # self.openFileNamesDialog()
        # self.saveFileDialog() 
        
        self.show()
    
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getOpenFileName(self,"Abrir cubo de datos FITS", "","Imagen FITS(*.fits)", options=options)
    
    def Archivo(self):
        #Apertura del archivo FITS
        hdu_list = fits.open(self.fileName)
        #Se carga la información del FITS en un arreglo
        cubo = hdu_list[0].data
        dimensiones_cubo = cubo.shape
        #Se cierra el archivo FITS
        hdu_list.close() 
        #Arreglo donde se regresa informacion del cubo y el cubo
        info = [dimensiones_cubo, cubo, self.fileName]
        return info
    
    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        if files:
            print(files)
    
    #Metodo para guardar un archivo
    #No usado para el programa
    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AbrirArchivoFITS()
    sys.exit(app.exec_())
