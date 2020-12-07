import numpy as np 
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic

class clase_A(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("ventana.ui", self)
    
    def imprime(self, dims, interface):
        print('imprime')
        print(dims)
        # interface.labelDimensionesArchivo.setText("x: " + str(dims[0]) + ", y: "+ 
                                                # str(dims[1]) + ", z: " + 
                                                # str(dims[2]))

# app = QApplication(sys.argv)
# window = clase_A()
# window.show()
# app.exec()

# print('Hola')
