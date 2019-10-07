import numpy as np
from astropy.visualization import astropy_mpl_style
import matplotlib.pyplot as plt

from astropy.io import fits
from scipy import asarray as ar, exp
from scipy.optimize import curve_fit
from astropy.table import Table
from scipy.integrate import quad
from tqdm import tqdm
from time import sleep

# Importa unicamente la funcion param_pixel desde el modulo
# parametros del pixel
# from parametros_del_pixel import param_pixel

# Importa toda el modulo parametros_del_pixel pero hay que llamar
# a cada funcion analisis_pixel.funcion()
import analisis_pixel



plt.style.use(astropy_mpl_style)





# Solicta el nombre del archivo FITS
#cubo_fits = raw_input("Ingresa el nombre del cubo FITS: ")
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
#lmb_ch1 = input('Ingrese la longitud de onda del primer canal (En Angstrom): ')
lmb_ch1 = 6643
# Solicita al usuario la resolucion por canal
#resol_ch = input('Ingrese el valor de la resolucion por canal (En Angstrom): ')
resol_ch = 0.43
print
# Crea el arreglo de la longitud de onda asociada a cada canal
# a partir de los valores ingresados por el usuario
lambda_file = []
for i in range(dimension[0]):
    lambda_file.append(lmb_ch1+(i*resol_ch))


datos_pixel = datos_cubo[0:dimension[0], 195, 149]

media2 = sum(lambda_file*datos_pixel)/sum(datos_pixel)
a = analisis_pixel.param_pixel(datos_pixel, lambda_file, dimension[0])


print a
