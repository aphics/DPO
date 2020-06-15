import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox 
from PyQt5 import uic


#Clase heredada de QMainWindow (Constructor de ventanas)
class Ventana(QMainWindow):
    #Metodo constructor de la clase
    def __init__(self):
        #Iniciar el objeto QMainWindow
        QMainWindow.__init__(self)
        #Cargar la configuracion del archivo .ui en el objeto
        uic.loadUi("VentanaPrincipal.ui", self)
        #Para mostrar maximizada descomentar la siguiente linea
        #self.showMaximized()
        #Tamano minimo de ventana
        self.setMinimumSize(1200,600)
        #Para centrar la ventana
        resolucion = QApplication.desktop()
        resolucion_ancho = resolucion.width()
        resolucion_alto = resolucion.height()
        left = ( resolucion_ancho / 2 ) - ( self.frameSize().width() / 2 )
        top = ( resolucion_alto / 2 ) - ( self.frameSize().height() / 2 )
        self.move(left, top)

#Evento para cerrar la ventana
    def closeEvent(self, evento):
        mensaje_cerrar = QMessageBox.question(self, "Salir ...", "Seguro que quieres salir de la aplicacion?", QMessageBox.Yes | QMessageBox.No)
        if mensaje_cerrar == QMessageBox.Yes: evento.accept()
        else: evento.ignore()
        
    def moveEvent(self, evento):
        x = str(evento.pos().x())
        y = str(evento.pos().y())
        self.posicion.setText("x: " + x + "y: " + y)

  
#Instancia para inicial una aplicacion
app = QApplication(sys.argv)
#Crear objeto de la clase
_ventana = Ventana()
#Mostrar ventana
_ventana.show()
#Ejecucion de la aplicacion
app.exec_()               
