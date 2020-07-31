from matplotlib import pyplot as plt

fig1 = plt.figure(1)
plt.plot([[1,2], [3, 4]])
fig2 = plt.figure(2)
plt.plot([[1,2], [3, 4]])

fig1.set_size_inches(3, 3)
fig2.set_size_inches(4, 5)

plt.show()