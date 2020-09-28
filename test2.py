import matplotlib.pyplot as plt
import numpy as np
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(np.random.rand(10))

def onclick(event):
    print( 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
        event.button, event.x, event.y, event.xdata, event.ydata))

cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()

import pandas as pd

df = pd.DataFrame({'uno': [1, 2, 3], 'tres': [7, 9, 8], 'dos': [4, 5, 6]}, index=['x', 'z', 'y'])

print(df)

print()

# Orden por índice (fila):
print(df.sort_index())

print()

# Ordenar por índice (columna):
print(df.sort_index(axis=1, ascending=False))

print()

# Ordenar por los valores de la columna 'tres':
print(df.sort_values(by='tres', ascending=False))