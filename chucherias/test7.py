import numpy as np 
import matplotlib.pyplot as plt 
# base = np.load("datos_prueba_300A_sin_ruido.npy", allow_pickle=True)
# print(base)


# a = []
# b = []
# b.append([1,2,3])
# b.append([4,5,6,7])
# b.append([8,9,10,11])
# b.append([1.5,2.5,3.5, 0.9])
# b.append([1.6,2.6,3.6, 1])

# a.append(b)

# c = []
# c.append([1,2,4])
# c.append([12,13,14,15])
# c.append([16,17,18,19])
# c.append([1.2, 2.2, 4.2, 0.5])
# c.append([1.3, 2.3, 4.3, 0.6])

# a.append(c)

# d = []
# d.append([1,2,3])
# d.append([12,13,14,15])
# d.append([16,17,18,19])
# d.append([1.1, 2.1, 5.1, 0.1])
# d.append([1.2, 2.2, 5.2, 0.2])
# a.append(d)


# d = []
# d.append([1,2,3])
# d.append([4,5,6,7])
# d.append([8,9,10,11])
# d.append([1.5,2.5,8.5, 0.9])
# d.append([1.6,2.6,8.6, 1])

# a.append(d)

# e = []
# e.append([1,2,4])
# e.append([4,5,6,7])
# e.append([8,9,10,11])
# e.append([1.5,2.5,8.5, 0.9])
# e.append([1.6,2.6,8.6, 1])

# a.append(e)

# # print(a)
# print(len(a))

# x = []
# x2 = []

# y = []
# y2 = []

# for i, eval in enumerate(a):
#     # print(eval)
#     # if eval[0] == [1,2,4]:
#     if eval[0][1] == 4:
#         print(eval)
#         x.append(eval[3][2])
#         y.append(eval[3][3])
#         # print(x[i], y[i])
#         x2.append(eval[4][2])
#         y2.append(eval[4][3])
#         # print(x2[i], y2[i])
# print(x, y)
# print(x2, y2)
# plt.plot(x, y, 'bo', ls = '--', label="ruido 1")
# plt.plot(x2, y2, 'go', ls='--', label="ruido 2")
# plt.title("Para p1 y p2 fijos")
# plt.xlabel("valor")
# plt.ylabel("chi")
# plt.legend()
# plt.show()

resultados = {}
A = 300
media = 24
sigma = 1.2
llave = str(A)+'-'+str(media)+'-'+str(sigma)
print(llave, type(llave))
resultados[llave] = [A,media,sigma]
print(resultados)