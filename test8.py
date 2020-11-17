# import numpy as np 
# import matplotlib.pyplot as plt 
# base = np.load("datos_prueba_300A_sin_ruido.npy", allow_pickle=True)
# print(base)

import numpy as np
import matplotlib.pyplot as plt


fig = plt.figure()
x = np.arange(10)
y = 2.5 * np.sin(x / 20 * np.pi)
xerr = np.linspace(2, 4, 10)
xerr = np.random.normal(0, 0.5, x.shape)
# print(yerr)
# yerr = [1,2,1,-1,-1,2,-1,2,-2,2]
# print(yerr)
# plt.errorbar(x, y + 6, yerr=yerr, label='both limits (default)')

# plt.errorbar(x, y + 4, yerr=yerr, uplims=True, label='uplims=True')

# plt.errorbar(x, y + 2, yerr=yerr, uplims=True, lolims=True,
#              label='uplims=True, lolims=True')

upperlimits2 = [True, False] * 5
lowerlimits2 = [False, True] * 5

upperlimits = []
lowerlimits = []
for i in range(len(xerr)):
    if xerr[i] >= 0:
        upperlimits.append(True)
        lowerlimits.append(False)
    else:
        upperlimits.append(False)
        lowerlimits.append(True)
print(upperlimits)
print(lowerlimits)
# upperlimits = [True for i in yerr if yerr[i]>0]
# print(upperlimits)
xerr = abs(xerr)

xerr2 = np.random.normal(0, 0.5, x.shape)
plt.errorbar(x, y, ls='None', xerr=xerr, xuplims=upperlimits, xlolims=lowerlimits,
              ecolor='black', c='red')

plt.errorbar(x, y, ls=':', xerr=xerr2, xuplims=upperlimits2, xlolims=lowerlimits2,
label='subsets of uplims and lolims', ecolor='blue', c='red')
plt.plot(label='color')

# plt.legend(loc='lower right')
plt.legend()
plt.show()