# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QPushButton

# class Example(QMainWindow):
    
#     def __init__(self):
#         super().__init__()
                
#         combo = QComboBox(self)
#         combo.addItem("Apple")
#         combo.addItem("Pear")
#         combo.addItem("Lemon")

#         combo.move(50, 50)

#         self.qlabel = QLabel(self)
#         self.qlabel.move(50,16)

#         combo.activated[str].connect(self.onChanged)      

#         self.setGeometry(50,50,320,200)
#         self.setWindowTitle("QLineEdit Example")
#         self.show()

#     def onChanged(self, text):
#         self.qlabel.setText(text)
#         self.qlabel.adjustSize()
        
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = Example()
#     sys.exit(app.exec_())

import numpy as np
import matplotlib.pyplot as plt

noise_normal = np.random.normal(5,0.5,48)
# noise_standar = np.random()

x = np.linspace(1,48,48)
print(x)

print(noise_normal)
# print(noise_standar)

plt.plot(x, noise_normal)
plt.show()
