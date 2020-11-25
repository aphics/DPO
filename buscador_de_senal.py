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
A2 = 245
mu2 = 28
sigma2 = 1.8


g1 = gauss(x, A1, mu1, sigma1)
g2 = gauss(x, A2, mu2, sigma2) 
ruido_artificial = np.random.normal(0, 2, x.shape) 
y = g1 + g2 + ruido_artificial + 50
y2 = g1 + g2
y = np.random.uniform(50, 10, x.shape)
y = list( round(i,2) for i in y)
# print(y) 

# -----------
# Primer paso
# -----------

# Promedio
promedio = np.mean(y)
print("promedio: ", promedio)

# Maximo y su posicion
maximo = max(y)
pos_max = y.index(maximo)
print("max: ", maximo, "posicion maximo: ", pos_max)

# -----------
# Arrays para separar senal de ruido. Primer paso
senal_1_array = np.zeros(np.array(y).shape)
ruido_1_array = np.zeros(np.array(y).shape)

# Ciclo para diferenciar senal de ruido
if y[pos_max-1] > (0.75*promedio) and y[pos_max+1] > (0.75*promedio):
    pos = pos_max
    while pos <= len(y)-1:
        if y[pos] >= promedio:
            senal_1_array[pos] = y[pos]
        if y[pos] < promedio and y[pos-1] > y[pos] and senal_1_array[pos-1] > 0:
            senal_1_array[pos] = y[pos]
        pos += 1
    pos = pos_max

    while pos >= 0:
        if y[pos] >= promedio:
            senal_1_array[pos] = y[pos]
        if y[pos] < promedio and y[pos+1] > y[pos] and senal_1_array[pos+1] > 0:
            senal_1_array[pos] = y[pos]
        pos -= 1

# Ciclo para crear array de rudio_1 a partir del array de senal_1
for i in range(len(senal_1_array)):
    if senal_1_array[i] == 0:
        ruido_1_array[i] = y[i]
    else:
        pass

# Arrays para almacenar informacion unicamente de senal_1 y de ruido_1
senal = []
ruido = []
# Ciclo para almacenar informacion unicamente de senal_1 y de ruido_1
for i in range(len(senal_1_array)):
    if senal_1_array[i] != 0:
        senal.append(senal_1_array[i])
    if ruido_1_array[i] != 0:
        ruido.append(ruido_1_array[i])

# Calculo del continuo_1 y su desviacion estandar
continuo_1 = np.mean(ruido)
sigma_continuo_1 = np.sqrt( (1/(len(ruido)-1)) * np.sum( ( ruido - np.mean(ruido) )**2 ) )
print("continuo 1 : ", continuo_1)
print("sigma: ", sigma_continuo_1)

# --------------
# Segundo paso
# --------------

# Array de senal_2 y ruido_2
senal_2_array = np.zeros_like(y)
ruido_2_array = np.zeros_like(y)

# Ciclo para separar senal_2 de ruido_2 a partir del valor del 
# continuo_1 y la sigma del ruido_1
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

# Ciclo para crear el array ruido_2 a partir de senal_2
for i in range(len(senal_2_array)):
    if senal_2_array[i] == 0:
        ruido_2_array[i] = y[i]
    else:
        pass

# Array para almacenar unicamente la informacion de senal_2 y ruido_2
senal_2 = []
ruido_2 = []
# Ciclo para almacenar unicamente la informacion de senal_2 y ruido_2
for i in range(len(senal_2_array)):
    if senal_2_array[i] != 0:
        senal_2.append(senal_2_array[i])
    if ruido_2_array[i] != 0:
        ruido_2.append(ruido_2_array[i])
print("senal 2: ", senal_2)
print("ruido 2: ", ruido_2)


# Obtencion del continuo a partir de ruido_2
continuo_2 = np.mean(ruido_2)
print("continuo 2: ", continuo_2)
# Substracción del continuo_2 a senal_2
senal_2 = senal_2-continuo_2
# Suma de senal_2
senal_sum = np.mean(senal_2)
print("senal suma: ", senal_sum)
# Calculo de la desviacion estandar de ruido_2
sigma_ruido_2 = np.std(ruido_2, ddof = 1)
print("Sigma ruido 2: ", sigma_ruido_2)
# print("sigma 2: ", sigma2)
print("senal a ruido ratio: ", senal_sum/sigma_ruido_2)






# plt.plot(x, g1 + 50, label="G1")
# plt.plot(x, g2 + 50, label="G2")
# plt.plot(x, ruido_artificial, label="Ruido artificial")
plt.plot(x, y, '.-', label="Datos")
# plt.plot(x, senal_1_array, label="Senal 1")
# plt.plot(x, ruido_1_array, label ="Ruido 1")
plt.plot(x, np.full_like(x, promedio), label="Promedio" )
# plt.plot(x, np.full_like(x, continuo_1), label="Cont 1" )
# plt.plot(x, np.full_like(x, continuo_1+sigma_continuo_1), label="Cont 1 + sigma 1")
plt.plot(x, np.full_like(y, continuo_2), label="Continuo real")
plt.plot(x, senal_2_array, '.', label="senal 2")
# plt.plot(x, ruido_2_array, label="ruido 2")
plt.legend()
plt.show()