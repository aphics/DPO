import numpy as np
import scipy.interpolate
import pandas as pd
import pylab
import matplotlib.pyplot as plt

wl = [i for i in range(1, 48)]
wl = np.array(wl)


def twin_peaks(wl, flux, delta, R, order=10):
  #La interpolacion permite la evaluacion del espectro a diferentes
  #longitudes de onda después del desplazamiento del arreglo
  rawf = scipy.interpolate.interp1d(wl, flux, bounds_error=False, fill_value=0)
  outf = np.zeros_like(flux)
  outf = outf + flux
  for m in range(1, order+1):
    outf = outf + ((-1)**m) * (R**m) * rawf(wl + (m*delta))
  return outf

flujo1 = [84.08533478,  84.02542877,  84.66689301,  88.79040527,  86.8771286, 
  83.41867065,  83.0365448,   84.22647858,  87.75096893,  86.83274078,
  83.89840698,  82.84483337,  83.69030762,  85.57483673,  94.89457703,
 103.85523987, 117.34669495, 143.28482056, 174.83866882, 201.7688446,
 241.28216553, 291.57144165, 325.38766479, 319.13180542, 289.13284302,
 253.55194092, 204.79350281, 158.77116394, 135.0980835,  120.62703705,
 115.70630646, 110.98122406, 102.01681519,  99.22322083,  96.96622467,
  96.37690735,  97.89134979,  99.12454987,  98.53933716,  95.95309448,
  95.34304047,  98.02826691,  94.52275848,  87.6909256,   85.04315186,
  83.69382477,  80.32698822]

flujo2 = [ 60.76659012,  57.62647247,  50.41750336,  49.53574753,  48.33449936,
  43.66425323,  41.04115295,  44.66896057,  50.56383896,  50.29148102,
  48.44561386,  50.44940948,  51.58250809,  59.35596085,  77.53921509,
  91.3781662 , 103.63374329, 123.92726898, 152.38206482, 170.97193909,
 178.31158447 ,201.74856567, 216.82427979, 194.56236267, 156.55189514,
 128.12651062  ,96.53326416,  70.87791443,  64.37514496,  64.37010193,
  69.20238495,  74.72666168,  73.84421539,  70.54618073,  67.37627411,
  70.02364349,  71.76290894,  70.48664093,  66.65513611,  62.97803116,
  63.47818756 , 63.48593521,  63.65970612,  65.12601471,  61.96345139,
  56.5904007  , 56.21949005]

flujo3 = [ 34.51300049,  35.04608917,  33.54432678,  37.79356384,  40.9273262,
  38.60827255,  36.60696411,  39.29825211,  42.8025322,   41.11476135,
  37.01183701,  38.25086212,  39.82696915,  45.49356461,  57.84592056,
  63.74675751,  71.27405548,  90.15153503, 105.11828613, 124.74910736,
 141.62988281, 139.71665955, 122.26168823, 108.24037933, 110.01968384,
  99.83040619,  70.3952713,   55.88486481,  57.34952545,  56.50667191,
  57.90737534,  60.49988937,  54.65034103,  43.25989914,  42.46909714,
  48.96273041,  49.04454422,  48.71305084,  50.70087433,  50.2251091,
  44.70508194,  40.60639191,  40.11267853,  43.38873672,  44.70631409,
  37.76773453,  31.70433426]

flujo4 = [ 55.44453812,  53.05897522,  52.17845535,  57.08400345,  58.71550369,
  56.29227448,  57.38964081,  57.90274811,  60.02680206,  64.8446579,
  65.73215485,  67.73951721,  67.41873932,  63.23197556,  63.86708832,
  67.05869293,  82.51724243, 105.86291504, 114.51498413, 137.49758911,
 181.33885193, 193.70155334, 173.63934326, 168.8387146 , 191.18556213,
 175.63951111, 113.57263184,  81.41274261,  83.6239624 ,  80.16750336,
  82.07486725,  85.80405426,  76.75112915,  58.83892441,  56.83065033,
  66.05215454,  67.11582184,  66.24571991,  74.72193146,  84.91313171,
  77.871521  ,  62.41158295,  58.20238495,  63.55883026,  66.0831604,
  61.10548401,  54.90304565]

flujo1 = np.array(flujo1)
flujo2 = np.array(flujo2)
flujo3 = np.array(flujo3)
flujo4 = np.array(flujo4)
print(flujo4, np.diff(flujo4))


delta = -5
R = 0.6
trans1 = twin_peaks(wl=wl, flux=flujo4, delta=delta, R=R, order=1)

trans2 = twin_peaks(wl=wl, flux=flujo4, delta=delta, R=R, order=2)
trans3 = twin_peaks(wl=wl, flux=flujo4, delta=delta, R=R, order=3)
trans4 = twin_peaks(wl=wl, flux=flujo4, delta=delta, R=R, order=4)
trans5 = twin_peaks(wl=wl, flux=flujo4, delta=delta, R=R, order=5)
trans6 = twin_peaks(wl=wl, flux=flujo4, delta=delta, R=R, order=6)
trans7 = twin_peaks(wl=wl, flux=flujo4, delta=delta, R=R, order=7)
trans8 = twin_peaks(wl=wl, flux=flujo4, delta=delta, R=R, order=8)
trans9 = twin_peaks(wl=wl, flux=flujo4, delta=delta, R=R, order=9)
trans10 = twin_peaks(wl=wl, flux=flujo2, delta=delta, R=R, order=10)



# print(flujo2, len(flujo1))
# 
# print(wl)

plt.plot(wl, flujo2, label="flujo")
# plt.plot(wl, trans1, label="trans 1")
# plt.plot(wl, trans2, label="trans 2")
# plt.plot(wl, trans3, label="trans 3")
# plt.plot(wl, trans4, label="trans 4")
# plt.plot(wl, trans5, label="trans 5")
# plt.plot(wl, trans6, label="trans 6")
# plt.plot(wl, trans7, label="trans 7")
# plt.plot(wl, trans8, label="trans 8")
# plt.plot(wl, trans9, label="trans 9")
# plt.plot(wl, trans10, label="trans 10")
plt.legend()
plt.show()



