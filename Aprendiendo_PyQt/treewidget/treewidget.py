# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 17:30:55 2020

@author: aphics
"""


import sys, time
from PyQt5.QtWidgets import QApplication, QDialog, QTreeWidgetItem
from PyQt5 import uic
from os import listdir, path, stat, startfile
from mimetypes import MimeTypes

class Dialogo(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("treewidget.ui", self)
        self.boton.clicked.connect(self.getDir)
        self.directorio.itemDoubleClicked.connect(self.openElement)
                
    def getDir(self):
        #Eliminar todas las filas de la busqueda anterior
        self.directorio.clear()
        #Ruta indicada por el usuario
        dir = self.ruta.text()
        #Comprobar si se trata de un directorio
        if path.isdir(dir):
            #Recorre sus elementos
            for element in listdir(dir):
                name = element
                pathinfo = dir + "\\" + name
                informacion = stat(pathinfo)
                #Si es un directorio
                if path.isdir(pathinfo):
                    type = "Carpeta de archivos"
                    size = ""
                else:
                    mime = MimeTypes()
                    type = mime.guess_type(pathinfo)[0]
                    size = str(informacion.st_size) + "bytes"
                #Fecha de modificacion
                date = str(time.ctime(informacion.st_mtime))
                #Crear un array para crear la fila con los items
                row = [name, date, type, size]
                #insertar la fila
                self.directorio.insertTopLevelItems(0,[QTreeWidgetItem(self.directorio, row)])
               
    def openElement(self):
        #Obener el item seleccionado por el usuario
        item = self.directorio.currentItem()
        #Crear la ruta accediendo al nombre del elemento(carpeta o archivo)
        elemento = self.ruta.text()+"\\"+item.text(0)
        #Para coprobar si es un directorio, navegar a su contenido
        if path.isdir(elemento):
            self.ruta.setText(elemento)
            self.getDir()
        #Si es un archivo abrrlo con el programa que lo abre por defecto
        else:
            startfile(elemento)
                    

app = QApplication(sys.argv)
dialogo = Dialogo()
dialogo.show()
app.exec_()