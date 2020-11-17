import numpy as np 
from astropy.io import fits
import matplotlib.pyplot as plt 


def gauss(x, A, mu, sigma):
    gauss_ = A * np.exp( -(x-mu)*(x-mu) / ( 2*sigma*sigma) )
    return gauss_

x = np.linspace(1, 48, 48)
A1 = 150
mu1 = 24
sigma1 = 2.3
A2 = 145
mu2 = 27
sigma2 = 1.8


g1 = gauss(x, A1, mu1, sigma1)
g2 = gauss(x, A2, mu2, sigma2) 
ruido_artificial = np.random.normal(0, 10, x.shape) 
y = g1 + g2 + ruido_artificial
y2 = g1 + g2
y = list( round(i,2) for i in y)
# print(y) 
promedio = np.mean(y)
print("promedio: ", promedio)
maximo = max(y)
pos = y.index(maximo)
# print(maximo, pos)
senal_1 = np.zeros(np.array(y).shape)
ruido = np.zeros(np.array(x).shape)
# print(senal)
for i in range(len(x)):
    if y[i] > (0.75*promedio):
        senal_1[i] = y[i]
        ruido[i] = 0
    else:
        senal_1[i] = 0
        ruido[i] = y[i]



print(senal_1)
print(ruido)
    


plt.plot(x, senal_1, '.', label='senal 1')
plt.plot(x, ruido, '.', label='ruido')

plt.plot(x, np.full(np.array(y).shape, promedio), label='Promedio')
# plt.plot(x, ruido_artificial, '.', label='ruido artificial')
# plt.plot(x, y2, label='Perfil sin ruido')
# plt.plot(x, g1, label="G1")
# plt.plot(x, g2, label="G2")
# plt.plot(x, y, '.', label="Perfil con ruido")
plt.legend()
plt.show()