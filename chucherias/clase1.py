#Clase 1

# a = "Publico"
b = "b inicial"
print(b)
print() 

class clase_a():
    a = 10
    # print("Clase A")
    # print("a: ", a)
    global b 
    b = "b privado clase A"
    # print(b)
    global c
    c = "c privado clase A"
    # print(c)
    # print(b)
print()
print(b)
print()
class clase_b():
    print("Clase B")
    global b
    global c
    print(b)
    print(c)

# print(b)
# clase_a()
# print( global b)
# clase_a()
# print()
# print(b)
# clase_b()



import sys
import time

from PyQt5.QtWidgets import (QApplication, QDialog,
                             QProgressBar, QPushButton)

TIME_LIMIT = 100

class Actions(QDialog):
    """
    Simple dialog that consists of a Progress Bar and a Button.
    Clicking on the button results in the start of a timer and
    updates the progress bar.
    """
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Progress Bar')
        self.progress = QProgressBar(self)
        self.progress.setGeometry(0, 0, 300, 25)
        self.progress.setMaximum(100)
        self.button = QPushButton('Start', self)
        self.button.move(0, 30)
        self.show()

        self.button.clicked.connect(self.onButtonClick)

    def onButtonClick(self):
        count = 0
        while count < TIME_LIMIT:
            count += 1
            time.sleep(1)
            self.progress.setValue(count)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Actions()
    sys.exit(app.exec_())
    