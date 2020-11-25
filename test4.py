
# import matplotlib.pyplot as plt 
import numpy as np

# fig, ax = plt.subplots()
# ax.plot(np.random.rand(10))

# def onclick(event):
#     print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
#           ('double' if event.dblclick else 'single', event.button,
#            event.x, event.y, event.xdata, event.ydata))

# cid = fig.canvas.mpl_connect('button_press_event', onclick)


a = [10, 2, 3]
b = [8, 3, 4]
c = [9, 1, 2]
d = [11, 3, 4]

# x = [a,b]
x = np.array([a,b,c])
# x = [a,b,c,d]

print(x)
nuevo = np.sort(x, order=)[::-1]
print(nuevo)

