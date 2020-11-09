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
    
a1, mu1, s1 = 320, 24, 2
a2, mu2, s2 = 150, 29, 2.7
a3, mu3, s3 = 230, 33, 3
a4, mu4, s4 = 125, 30, 3.2

p1 = [a1, mu1, s1]
p2 = [a1, mu1, s1, a2, mu2, s2]
p3 = [a1, mu1, s1, a2, mu2, s2, a3, mu3, s3]
p4 = [a1, mu1, s1, a2, mu2, s2, a3, mu3, s3, a4, mu4, s4]

x = np.linspace(1, 48, 48)
n_gauss = 3
continuo = 50
artificial = constructor_gaussianas(x, p3, n_gauss)
# print(artificial)

Amplitudes_principales = [80, 120, 200, 300]
Amplitud_principal = Amplitudes_principales[0]

# Amplitudes = np.linspace(0.3*Amplitud_principal, 0.9*Amplitud_principal, 7)
Amplitudes = np.linspace(0.3*Amplitud_principal, 0.9*Amplitud_principal, 2)
print(Amplitudes)

Media_principal = 24
# Medias = np.linspace(Media_principal-6, Media_principal+6, 25)
Medias = np.linspace(Media_principal-6, Media_principal+6, 5)

Sigma_principal = 2
# Sigmas = np.linspace(1.2, 3.4, 22)
Sigmas = np.linspace(1.2, 3.4, 1)
for i in range(len(Sigmas)):
    Sigmas[i] = round(Sigmas[i],1)

# for media_ in Medias:
#     for sigma_ in Sigmas:
#         for amplitud_ in Amplitudes:
#             modelo = np.zeros(np.array(x).shape)
#             g_principal = gauss(x, [Amplitud_principal, Media_principal, Sigma_principal])
#             plt.plot(x, g_principal)
#             modelo += g_principal
#             g_segunda = gauss(x, [amplitud_, media_, sigma_])
#             plt.plot(x, g_segunda, label=("A: ",  amplitud_, "S: ", sigma_, "M: ", media_))
#             modelo += g_segunda
#             plt.plot(x, modelo )
#             plt.legend()
#             plt.show()
# plt.legend()
# plt.show()

g1 = gauss(x, [250, Media_principal, Sigma_principal]) 
g2 = gauss(x, [180, 21, 1.2])
g3 = g1 + g2 + np.random.normal(0, 5, np.array(g2).shape)
print(g3)
plt.plot(x, g1, label="G1")
plt.plot(x, g2, label="G2")
plt.plot(x, g3, label="Suma")
plt.legend()
plt.show()