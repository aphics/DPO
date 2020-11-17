import numpy as np
import matplotlib.pyplot as plt 

def gauss(x, p):
    A, mu, sigma = p
    g_ = A * np.exp(-(x-mu)*(x-mu)/(2.0*sigma*sigma))
    return g_

def constructor_gaussianas(x, p, n_gauss):
    modelo = np.zeros(np.array(x).shape)
    p_split = np.split(np.array(p), n_gauss)
    for g in range(n_gauss):
        g_ = gauss(x, p_split[g])
        modelo += g_
    modelo += continuo
    datos = []
    datos.append(modelo)
    datos.append(p_split)
    return datos
    

x = np.linspace(1, 48, 48)

# Amplitudes_principales = [300, 200, 120, 80]
Amplitudes_principales = [300,80]
print(Amplitudes_principales)

# Medias = np.linspace(29, 24, 11)
Medias = np.linspace(25, 29, 9)
print(Medias)

# Sigmas = np.linspace(1.2, 3.4, 22)
Sigmas = np.linspace(1.2, 3.4, 2)
for i in range(len(Sigmas)):
    Sigmas[i] = round(Sigmas[i],1)

print(Sigmas)

datos = []

for i, AP in enumerate(Amplitudes_principales):
    for k, SP in enumerate(Sigmas):
        Amplitudes = np.linspace(0.3*AP, 0.3*AP, 2)
        for l, ampli_ in enumerate(Amplitudes):
            for m, media_ in enumerate(Medias):
                for n, sigma_ in enumerate(Sigmas):
                    modelo = np.full(np.array(x).shape, 50)
                    g_principal = gauss(x, [AP, 24, SP])
                    g_segunda = gauss(x, [ampli_, media_, sigma_])
                    modelo = g_principal + g_segunda   
                    modelo_5 = modelo + np.random.normal(0, 5, modelo.shape)
                    modelo_7 = modelo + np.random.normal(0, 7, modelo.shape)
                    modelo_8 = modelo + np.random.normal(0, 8, modelo.shape)
                    modelo_10 = modelo + np.random.normal(0, 10, modelo.shape)
                    params = [AP, 24, SP, ampli_, media_, sigma_]
                    data = []
                    data.append(params)
                    data.append(modelo)
                    data.append(modelo_5)
                    data.append(modelo_7)
                    data.append(modelo_8)
                    data.append(modelo_10)
                    datos.append(data)
                    # print(AP, MP, SP, ampli_, media_, sigma_)

print(len(datos))
np.save("datos_prueba", datos)