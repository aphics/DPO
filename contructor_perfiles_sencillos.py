import numpy as np
import matplotlib.pyplot as plt

def gauss(x, p):
    A, mu, sigma = p
    g_ = A * np.exp(-(x-mu)*(x-mu)/(2.0*sigma*sigma))
    return g_

def constructor(x, p, n_gauss, modelo):
    print("p", p)
    p_split = np.split(np.array(p), n_gauss)
    for g in range(n_gauss):
        g_ = gauss(x, p_split[g])
        plt.plot(x, g_ + continuo , label="G"+str(g+1))
        modelo += g_
    return modelo + continuo


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
modelo = np.zeros(np.array(x).shape)
perfil = constructor(x, p3, n_gauss, modelo)
perfil_noisy = perfil + np.random.normal(0, 10, perfil.shape)
print(perfil_noisy)
plt.plot(x, perfil, label="Suma" )
plt.plot(x, perfil_noisy, label="Suma con ruido" )
plt.legend()
plt.show()