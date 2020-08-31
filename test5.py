import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def gauss(x, A, x0, sigma):
    #Una funcion Gaussiana sin y0 (offset)
    gauss_ = []
    for i in range(x.size):
        gauss_ += [A * np.exp( -(x[i]-x0)**2 / (2*(sigma**2)))]
    return np.array(gauss_)

def gauss_y0(x, A, x0, sigma, y0):
    #Una funcion Gaussiana con y0 (offset)
    gauss_ = []
    for i in range(x.size):
        gauss_ += [A * np.exp( -(x[i]-x0)**2 / (2*(sigma**2))) + y0]
    return np.array(gauss_)

def gauss2(x, A1, x01, sigma1, A2, x02, sigma2):
    #Dos funciones Gaussianas sin y0 (offset)
    gauss2_ = []
    for i in range(x.size):
        gauss2_ += [ (A1 * np.exp( -(x[i]-x01)**2 / (2*sigma1**2))) + 
                        (A2 * np.exp( -(x[1]-x02)**2 / (2*sigma2**2)))]
    return np.array(gauss2_)

def gauss2_y0(x, A1, x01, sigma1, A2, x02, sigma2, y0):
    #Dos funciones Gaussianas con y0 (offset)
    gauss2_ = []
    for i in range(x.size):
        gauss2_ += [ (A1 * np.exp( -(x[i]-x01)**2 / (2*sigma1**2))) + 
                        (A2 * np.exp( -(x[1]-x02)**2 / (2*sigma2**2))) + y0]
    return np.array(gauss2_)

x = [ i for i in range(1, 48)]
x = np.array(x)

#Agrego 2 conjuntos de datos
#Flujo 1
# flujo = [ 60.76659012,  57.62647247,  50.41750336,  49.53574753,  48.33449936,
#   43.66425323,  41.04115295,  44.66896057,  50.56383896,  50.29148102,
#   48.44561386,  50.44940948,  51.58250809,  59.35596085,  77.53921509,
#   91.3781662 , 103.63374329, 123.92726898, 152.38206482, 170.97193909,
#  178.31158447 ,201.74856567, 216.82427979, 194.56236267, 156.55189514,
#  128.12651062  ,96.53326416,  70.87791443,  64.37514496,  64.37010193,
#   69.20238495,  74.72666168,  73.84421539,  70.54618073,  67.37627411,
#   70.02364349,  71.76290894,  70.48664093,  66.65513611,  62.97803116,
#   63.47818756 , 63.48593521,  63.65970612,  65.12601471,  61.96345139,
#   56.5904007  , 56.21949005]

#Flujo 2
flujo = [ 34.51300049,  35.04608917,  33.54432678,  37.79356384,  40.9273262,
  38.60827255,  36.60696411,  39.29825211,  42.8025322,   41.11476135,
  37.01183701,  38.25086212,  39.82696915,  45.49356461,  57.84592056,
  63.74675751,  71.27405548,  90.15153503, 105.11828613, 124.74910736,
 141.62988281, 139.71665955, 122.26168823, 108.24037933, 110.01968384,
  99.83040619,  70.3952713,   55.88486481,  57.34952545,  56.50667191,
  57.90737534,  60.49988937,  54.65034103,  43.25989914,  42.46909714,
  48.96273041,  49.04454422,  48.71305084,  50.70087433,  50.2251091,
  44.70508194,  40.60639191,  40.11267853,  43.38873672,  44.70631409,
  37.76773453,  31.70433426]

flujo = np.array(flujo)   

#Ajuste de dos Gaussianas sin considerar y0 (offset)
popt, pcov = curve_fit(gauss2, x, flujo)
#popt = A1, x01, sigma1, A2, x02, sigma2
g1 = gauss(x, popt[0], popt[1], popt[2])
g2 = gauss(x, popt[3], popt[4], popt[5])

#Ajuste de dos Gaussianas considerando y0 (offset)
popt_y0, pcov_y0 = curve_fit(gauss2_y0, x, flujo)
#popt = A1, x01, sigma1, A2, x02, sigma2, y0
g1_y0 = gauss_y0(x, popt_y0[0], popt_y0[1], popt_y0[2], popt_y0[6])
g2_y0 = gauss_y0(x, popt_y0[3], popt_y0[4], popt_y0[5], popt_y0[6])




plt.plot(x, flujo, label="Observado") 
plt.plot(x, g1, label="G1")
plt.plot(x, g2, label="G2")
plt.plot(x, g1_y0, label="G1 + y0")
plt.plot(x, g2_y0, label="G2 + y0")
plt.legend()
plt.show()

# plt.hist(flujo, bins=47, density = True, histtype = 'stepfilled')
# plt.show()