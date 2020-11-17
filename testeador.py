from scipy.optimize import minimize
import numpy as np 
import matplotlib.pyplot as plt 

base = np.load("datos_prueba.npy", allow_pickle=True)
# print(len(base))
print(base[0][0])
# print(base[0][1])

Y = base[0][1]
X = np.linspace(1,48,48)


def fit_gauss(x, p):
    A, mu, sigma = p
    gauss_ = A * np.exp( -(x-mu)*(x-mu) / (2*sigma*sigma) )
    return gauss_

def main_fitter(p, x, y, ngauss):
    chi2 = 0
    model = np.zeros( np.array(y).shape )
    split_p = np.split( np.array(p), ngauss )

    for g in range(ngauss):
        gp = split_p[g]

        if gp[0] <=0:                   #Evita amplitudes negativas
            return 1e10
        if gp[2] <=0 or gp[2] >10:      #Limites en la dispersion
            return 1e10
        else:
            model += fit_gauss(x, gp)
    
    chi2 = sum( ( y-model )**2 ) / max(y)
    return chi2

datos_testeados = {}

# ---------------------------------------------
# Aqui debe empezar el iterador sobre los datos
# Para cada conjunto de datos con y sin ruido
# ---------------------------------------------
Niters = 10

results = {}
llaves = []

N = 2
zerolev = np.mean(sorted(Y)[:22])
Y = Y - zerolev

for i in range(Niters):
    p0 = []
    for j in range(N):
        p0.append(np.random.uniform(80,130))  # Amplitud
        p0.append(np.random.uniform(1,48))  # Media
        p0.append(np.random.uniform(1.2, 3.4))  # Disp
            
    # options={'maxiter':15000, 'maxfev':15000, 'disp':False, 'adaptive':True}
    options={'maxiter':15000, 'maxfev':15000, 'disp':False}
    fit = minimize(main_fitter, p0, method= 'Powell', options=options, args=(X,Y,N,))
    
    # fit.fun devulve el valor de la funcion objetivo. En mi caso la chi2
    # fit.x devuelve la solucion de la optimizacion
    results[fit.fun] = fit.x
    llaves.append(fit.fun)



a1 = []
m1 = []
s1 = []
a2 = []
m2 = []
s2 = []

for i in range(Niters):
    if results[llaves[i]][0] < results[llaves[i]][3]:
        for j in range(0,3):
            aux = results[llaves[i]][j+3] 
            results[llaves[i]][j+3] = results[llaves[i]][j]
            results[llaves[i]][j] = aux
    else:
        pass
    a1.append( round(results[llaves[i]][0], 2) )
    m1.append( round(results[llaves[i]][1], 2) )
    s1.append( round(results[llaves[i]][2], 2) )
    a2.append( round(results[llaves[i]][3], 2) )
    m2.append( round(results[llaves[i]][4], 2) )
    s2.append( round(results[llaves[i]][5], 2) )

# No se van a colocar barras de error con minimos y maximos en los parametros
# ya que los valores pueden variar demasiado
# print(m1)
# print(m2)

mejor = min ( llaves )
mejores_params = results[mejor]
print(mejores_params)
