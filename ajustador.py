from scipy.optimize import minimize
import numpy as np
import matplotlib.pyplot as plt

flujo1 = [ 60.76659012,  57.62647247,  50.41750336,  49.53574753,  48.33449936,
43.66425323,  41.04115295,  44.66896057,  50.56383896,  50.29148102,
48.44561386,  50.44940948,  51.58250809,  59.35596085,  77.53921509,
91.3781662 , 103.63374329, 123.92726898, 152.38206482, 170.97193909,
178.31158447 ,201.74856567, 216.82427979, 194.56236267, 156.55189514,
128.12651062  ,96.53326416,  70.87791443,  64.37514496,  64.37010193,
69.20238495,  74.72666168,  73.84421539,  70.54618073,  67.37627411,
70.02364349,  71.76290894,  70.48664093,  66.65513611,  62.97803116,
63.47818756 , 63.48593521,  63.65970612,  65.12601471,  61.96345139,
56.5904007  , 56.21949005]

# def gauss_1(x, y0, A, mu, sigma):
#     gaussiana_1 = (A * np.exp( -(x-mu)**2 / (2*sigma**2) ) ) + y0
#     return gaussiana_1

# def gauss_2(x, y0, A_1, mu_1, sigma_1, A_2, mu_2, sigma_2):
#     gaussiana_2 = ( A_1 * np.exp( -(x-mu_1)**2 / 2*sigma_1**2 ) ) + ( 
#                     A_2 * np.epx( -(x-mu_2)**2 / 2*sigma_2**2 ) ) + y0
#     return gaussiana_2

# def gauss_3(x, y0, A_1, mu_1, sigma_1, A_2, mu_2, sigma_2, A_3, mu_3, sigma_3):
#     gaussiana_3 = ( A_1 * np.exp( -(x-mu_1)**2 / 2*sigma_1**2 ) ) + ( 
#                     A_2 * np.epx( -(x-mu_2)**2 / 2*sigma_2**2 ) ) + ( 
#                     A_3 * np.epx( -(x-mu_3)**2 / 2*sigma_3**2 ) ) + y0
#     return gaussiana_3

# def gauss_4(x, y0, A_1, mu_1, sigma_1, A_2, mu_2, sigma_2, A_3, mu_3, sigma_3, 
#                 A_4, mu_4, sigma_4):
#     gaussiana_4 = ( A_1 * np.exp( -(x-mu_1)**2 / 2*sigma_1**2 ) ) + ( 
#                     A_2 * np.epx( -(x-mu_2)**2 / 2*sigma_2**2 ) ) + ( 
#                     A_3 * np.epx( -(x-mu_3)**2 / 2*sigma_3**2 ) ) + ( 
#                     A_4 * np.epx( -(x-mu_4)**2 / 2*sigma_4**2 ) ) + y0
#     return gaussiana_4

def gauss_1(x, A, mu, sigma):
    gaussiana_1 = (A * np.exp( -(x-mu)**2 / (2*(sigma**2)) ) ) + y0
    return gaussiana_1

def gauss_2(x, A_1, mu_1, sigma_1, A_2, mu_2, sigma_2):
    gaussiana_2 = ( A_1 * np.exp( -(x-mu_1)**2 / 2*(sigma_1**2 )) ) + ( 
                    A_2 * np.exp( -(x-mu_2)**2 / 2*(sigma_2**2 )) ) + y0
    return gaussiana_2

def gauss_3(x, A_1, mu_1, sigma_1, A_2, mu_2, sigma_2, A_3, mu_3, sigma_3):
    gaussiana_3 = ( A_1 * np.exp( -(x-mu_1)**2 / 2*sigma_1**2 ) ) + ( 
                    A_2 * np.exp( -(x-mu_2)**2 / 2*sigma_2**2 ) ) + ( 
                    A_3 * np.exp( -(x-mu_3)**2 / 2*sigma_3**2 ) ) + y0
    return gaussiana_3

def gauss_4(x, A_1, mu_1, sigma_1, A_2, mu_2, sigma_2, A_3, mu_3, sigma_3, 
                A_4, mu_4, sigma_4):
    gaussiana_4 = ( A_1 * np.exp( -(x-mu_1)**2 / 2*sigma_1**2 ) ) + ( 
                    A_2 * np.exp( -(x-mu_2)**2 / 2*sigma_2**2 ) ) + ( 
                    A_3 * np.exp( -(x-mu_3)**2 / 2*sigma_3**2 ) ) + ( 
                    A_4 * np.exp( -(x-mu_4)**2 / 2*sigma_4**2 ) ) + y0
    return gaussiana_4

def main_fitter(p, x, y , Ngauss):
    chi2 = 0 
    model = np.zeros_like(y)

    if Ngauss == 1:
        model = gauss_1(x, p[0], p[1], p[2])
        chi2 = sum((y-model)**2) 
    if Ngauss == 2:
        model = gauss_2(x, p[0], p[1], p[2], p[3], p[4], p[5])  
        chi2 = sum((y-model)**2) 
    if Ngauss == 3:
        model = gauss_3(x, p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8])  
        chi2 = sum((y-model)**2) 
    if Ngauss == 4:
        model = gauss_4(x, p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11])  
        chi2 = sum((y-model)**2) 

    return chi2

Y = np.array(flujo1)
X = [1 + n*0.43 for n in range(0, len(Y))]

Ngauss = 4

N_iter = 10
Resultados = {}

y0 = np.min(Y)

for i in range (N_iter):
    # p0 = np.empty(Ngauss)
    p0 = []
    # p0.append(np.min(Y))
    for j in range(Ngauss):
        p0.append(np.random.uniform(80,130))      #Amplitud
        # p0.append(np.random.uniform(6650, 6670))  # Media
        # p0.append(np.random.uniform(12, 30))  # Media
        p0.append(np.random.uniform(7.5, 17))  # Media
        p0.append(np.random.uniform(1, 8))        # Disp
    print('p0: ', p0)
    fit = minimize(main_fitter, p0, method = "Powell", args=(X, Y, Ngauss), options={'disp':False})

    Resultados[fit.fun] = fit.x

best = min(Resultados.keys())
print(best)
best_fit = Resultados[best]
print(best_fit)

prueba = []
for i in range(Ngauss):
    prueba.append(gauss_1(X, best_fit[i*3], best_fit[(i*3)+1], best_fit[(i*3)+2]))
    
# print(prueba)
# prueba1 = gauss_1(X, best_fit[0], best_fit[1], best_fit[2])
# prueba2 = gauss_1(X, best_fit[3], best_fit[4], best_fit[5])
# prueba3 = gauss_1(X, best_fit[6], best_fit[7], best_fit[8])
# prueba4 = gauss_1(X, best_fit[9], best_fit[10], best_fit[11])
suma = gauss_2(X, best_fit[0], best_fit[1], best_fit[2], best_fit[3], best_fit[4], best_fit[5])
# # prueba = gauss_3(X, best_fit[0], best_fit[1], best_fit[2], best_fit[3], best_fit[4], best_fit[5], 
# #                     best_fit[6], best_fit[7], best_fit[8])
# # prueba = gauss_4(X, best_fit[0], best_fit[1], best_fit[2], best_fit[3], best_fit[4], best_fit[5], 
# #                     best_fit[6], best_fit[7], best_fit[8], best_fit[9], best_fit[10], best_fit[11])

# # print(prueba)
plt.plot(X,Y, label='data')
plt.plot(X,prueba[0], label='G1')
plt.plot(X,prueba[1], label='G2')
plt.plot(X,prueba[2], label='G3')
plt.plot(X,prueba[3], label='G4')
plt.plot(X,suma, label='Suma')
plt.legend()
plt.show()