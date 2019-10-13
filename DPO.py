import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
from astropy.io import fits
# from scipy import asarray as ar, exp
# from scipy.optimize import curve_fit
# from scipy.integrate import quad
# from tqdm import tqdm
# from time import sleep

# Importa unicamente la funcion param_pixel desde el modulo
# parametros del pixel
# from parametros_del_pixel import param_pixel

# Importa el modulo parametros_del_pixel completo pero hay que llamar
# a cada funcion analisis_pixel.funcion()
import analisis_pixel

def gauss_fit(x, a, x0, sigma, y0):
    return y0 + (a * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2)))

# Estilos de graficas. Descomentar el estilo deseado
# plt.style.use(astropy_mpl_style)      # Estilo normal de astropy
# plt.style.use("dark_background")      # Con fondo negro
# plt.style.use("Solarize_Light2")      # Estilo amarillento
# plt.style.use("bmh")                  # Con fondo gris
plt.style.use("ggplot")               # Con fondo gris
# plt.style.use("seaborn-poster")       # Estilo de grafica para poster


# Solicta el nombre del archivo FITS
# cubo_fits = raw_input("Ingresa el nombre del cubo FITS: ")
cubo_fits = "cubo.fits"
# Realiza apertura del archivo FITS (HDU). HDU = Header Data Unity
hdu_list = fits.open(cubo_fits)
# Carga la informacion del archivo FITS a un arreglo de 3 dimensiones
datos_cubo = hdu_list[0].data
# Carga las dimensiones del cubo a la variable dimension
dimension = datos_cubo.shape
# Cierra el archivo FITS para no modificar el archivo original
# La informacion ya se cargo a la variable datos_cubo
hdu_list.close()

print
print("Nombre del cubo: "+str(cubo_fits))
print("Dimensiones del cubo")
print("(x,y,z) = (" + str(dimension[2]) + "," + str(dimension[1]) + "," + str(dimension[0]) + ")")
print

# Solicita al usuario el valor de la longitud de onda del primer canal
# lmb_ch1 = input('Ingrese la longitud de onda del primer canal (En Angstrom): ')
lmb_ch1 = 6643
# Solicita al usuario la resolucion por canal
# resol_ch = input('Ingrese el valor de la resolucion por canal (En Angstrom): ')
resol_ch = 0.43

# Crea el arreglo de la longitud de onda asociada a cada canal
# a partir de los valores ingresados por el usuario
lambda_file = []
for i in range(dimension[0]):
    lambda_file.append(lmb_ch1+(i*resol_ch))

# Solicita al usuario la coordenada x del pixel a analizar
# equis=input('Introduzca la coordenada x = ')
equis = 149
# Solicita al usuario la coordenada y del pixel a analizar
# ye=input('Introduzca la coordenada y = ')
ye = 265
# Reajusta las coordenadas del pixel de acuerdo al acomodo de ADHOCw
equis = equis - 1
ye = dimension[1] - ye


# Carga la informacion del pixel a analizar a la funcion analisis_pixel
# La forma de ingresar las coordenadas zon z,y,x
datos_pixel = datos_cubo[0:dimension[0], ye, equis]

a = analisis_pixel.param_pixel(datos_pixel, lambda_file, dimension[0])

# print a

# observables = [amplitud_gaussiana, lambda_observada, sigma, continuo, fwhm, mono, velocidad_observada]
# analisis = [ajuste, ajuste_normal, datos_pixel_normal, diferencia_datos_ajuste, diferencia_datos_ajuste_normal, buen_ajuste]
# parametros = [observables, analisis]
# Grafica

plt.plot(lambda_file, datos_pixel, 'bo:', label='Senal')
plt.plot(lambda_file, a[1][0], 'g:', label='Ajuste')
plt.errorbar(lambda_file, a[1][0], yerr=a[1][3], ecolor='r', elinewidth=1, linewidth=0)
plt.legend()
plt.title('Pixel = (' + str(equis + 1) + ',' + str(dimension[1] - ye) + ')')
plt.xlabel('Lambda')
plt.ylabel('Senal')
plt.show()
