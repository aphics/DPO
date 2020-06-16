#el modulo re sirve para validar
import sys, re
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
#el modulo iuc sirve para manejar archivos uic
from PyQt5 import uic

class Dialogo(QDialog):
    #creando metodo constructor
    def __init__(self):
        #iniciando objeto
        QDialog.__init__(self)
        #cargango archivo uic
        uic.loadUi("validacion.ui", self)
        #cada que se inserten valores en el campo nombre se valida
        self.nombre.textChanged.connect(self.validar_nombre)
        #cada que inserten valores en el campo email se valida
        self.email.textChanged.connect(self.validar_email)
        #validacion de formulacio
        self.boton.clicked.connect(self.validar_formulario)

    #creando metodo para validar campo nombre
    def validar_nombre(self):
        
        #guardando en variable el texto del campo nombre
        nombre = self.nombre.text()
        # variable para validar
        # lo que esta entre comillas son las expresiones regulares
        # \s es para 
        # re.I sirve para ignorar mayusculas y minusculas
        validar = re.match("^[a-z\sáéíóúñ]+$", nombre, re.I)
        
        # revisaremos que nombre esta vacio
        # si nombre esta vacio cambiamos los bordes a amarillo
        if nombre == "":
            self.nombre.setStyleSheet("border: 1px solid yellow;")
            return False
        # si la validacion no es correcta cambia los bordes a rojo
        elif not validar:
            self.nombre.setStyleSheet("border: 1px solid red;")
            return False
        # en caso de que pase las condiciones anteriores
        else:
            self.nombre.setStyleSheet("border: 1px solid green;")
            return True        

    #creando metodo para validar email
    # se hace igual que el metodo anteior para nombre cambiando lo necesario
    def validar_email(self):
        email = self.email.text()
        validar = re.match("^[a-zA-Z0-9\._-]+@[a-zA-Z0-9-]{2,}[.][a-zA-Z]{2,4}$", email, re.I)
        if email == "":
            self.email.setStyleSheet("border: 1px solid yellow;")
            return False
        elif not validar:
            self.email.setStyleSheet("border: 1px solid red;")
            return False
        else:
            self.email.setStyleSheet("border: 5px solid green;")
            return True

    #creacion de metodo que valida nombre y email 
    def validar_formulario(self):
        if self.validar_nombre() and self.validar_email():
            QMessageBox.information(self, "Formulario correcto", "Validacion correcta", QMessageBox.Discard)
        else:
            QMessageBox.warning(self, "Formulario incorrecto", "Validacion incorrecta", QMessageBox.Discard)

# iniciando aplicacion
app = QApplication(sys.argv)
dialogo = Dialogo()
dialogo.show()
app.exec_()