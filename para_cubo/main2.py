# ----------------------------
# Autor: Edgar Sandoval Trejo
#
# Este programa ajusta de ser posible una funcion Gaussiana a un pixel de
# un cubo de datos de dimensiones (x,y,z), donde la coordenada z es el
# numero de canal.
# El ajuste devuelve los parametros de la funcion Gaussiana, Amplitud,
# desviacion (sigma) y la media, con los cuales se calculan los valores de
# longitud de onda y velocidad observada, senal a ruido, FWHM, Monocromatico
# y Continuo.
#
# Ultima actualizacion: 27 enero 2018
# Librerias usadas

import numpy as np
from astropy.visualization import astropy_mpl_style
import matplotlib.pyplot as plt
from astropy.io import fits
from scipy import asarray as ar, exp
from scipy.optimize import curve_fit
from scipy.integrate import quad

plt.style.use(astropy_mpl_style)

# -----------------------------
# Definicion de la funcion Guassiana a ajustar


def gauss_fit(x, a, x0, sigma, y0):
    return y0+a*np.exp(-(x-x0)**2/(2*sigma**2))


def gauss_fit_sin_continuo(x, a, x0, desv):
    return a*np.exp((-(x-x0)**2)/(2*desv**2))


# -----------------------------
# Codigo
# -----------------------------

# Solicita al usuario el nombre del cubo de datos FITS
# image_file = raw_input("Ingresa el nombre del archivo fits: ")
cubo_fits = "cubo.fits"
# Realiza la apertura de la informacion del cubo FITS (HDU). Header Data Unity
hud_list = fits.open(cubo_fits)
# Carga la informacion a un arreglo
image_data = hud_list[0].data
# Carga la dimension del cubo a la variable dimension
dimension = image_data.shape
print
print('--------Dimensiones del cubo--------')
print('(x,y,z) = (' + str(dimension[2]) + ',' + str(dimension[1]) + ',' + str(dimension[0]) + ')')
print
hud_list.close()                 										#Cierre del archivo fits. La informacion ya se cargo en la variable image_data
print
#lmb_ch1 = input('Longitud de onda del primer canal (En Angstrom): ')
lmb_ch1=6643
#resol_ch = input('Valor de la resolucion por canal (En Angstrom): ')
resol_ch=.43
print()
lambda_file = []
for i in range(dimension[0]):
    lambda_file.append(lmb_ch1+(i*resol_ch))
#------------------------------
print('-------Coordenadas del pixel--------')
equis=input('Introduzca la coordenada x = ')									#Solicita coordenada x del pixel
ye=input('Introduzca la coordenada y = ')									#Solicita coordenada y del pixel
equis=equis-1
ye= dimension[1] - ye

datos_cubo = image_data[0:dimension[0], ye, equis]
x=ar(range(dimension[0]))
x=x+1
#-------------------------------
mean = sum(x * datos_cubo) / sum(datos_cubo)										#Media(Por la forma en realidad es el baricentro)
sigma = np.sqrt(sum(datos_cubo * (x - mean) ** 2) / sum(datos_cubo))								#Desviacion estandar
M = np.max(datos_cubo)												#Condicion inicial para la amplitud
if M ==0:
	M = mean
X0 = np.argmax(datos_cubo)												#Condicion inicial para la lambda central
print ()
print ('----------Condiciones iniciales-----------')
print ('(En base a los canales y no a longitud de onda)')
print
print ('Media         ' + str(mean))
print ('Sigma         ' + str(sigma))
print ('Amplitud      ' + str(M))
print ('Valor central ' + str(X0))

#--------------
# Ajuste
print
try:
	popt, pcov = curve_fit(gauss_fit, x, datos_cubo, p0=[mean, X0, sigma, 1])						#Ajuste
	A = popt[0]												#Amplitud de Gaussiana respecto de y0
	X0 = popt[1]			 									#Lamba central de la Gaussiana,(MEAN)
	desv = popt[2]												#Desviacion estandar
	y0 = popt[3]												#Valor de y0
	s_n=(A+y0)/y0												#Senal a ruido
	fwhm = 2 * np.sqrt(2*np.log(10))*np.absolute(desv)							#FWHM
	mono = quad(gauss_fit_sin_continuo, 1, dimension[0], args=(A, X0, desv))							#Calculo del monocromatico
	mono = mono[0]												#Valor del monocromatico
except:
	A = 0													#Amplitud de cero por no ajustar
	y0 = 0 													#y0 de cero por no ajustar
	s_n= 0													#Senal a ruido de cero por no ajustar
	fwhm = 0												#FWHM de cero por no ajustar
	mono = 0
#------------------------------
sum = 0
for i in range(dimension[0]):												#Calculo de buen ajuste
	f_fit = gauss_fit(x[i],A,X0,desv,y0)
	sus = (datos_cubo[i] - f_fit) / np.max(datos_cubo)
	sum = sum + sus**2
desviacion = np.sqrt(sum / dimension[0])
pend = 0													#Calculo de la velocidad
def linea(x,pend,b):												#Funcion para interpolar lambda
	return (pend*x)+b
popt2, pcov2 = curve_fit(linea,x,lambda_file,p0=None)
m = popt2[0]													#Pendiendte de la recta
b = popt2[1]													#Ordenada al origen
print (m,b)
lambda_central = (m*X0)+b											#Valor de lambda respecto al valor maximo del ajuste
#lambda_bari = (m*mean)+b
v = 299792.458*((lambda_central/6562.8)-1)									#Velocidad observada respecto de Halpha
#v_bari = 299792.458*((lambda_bari/6562.8)-1)									#Velocidad observada respecto de Halpha (baricentro)

#-----------------------------------
print ()
print ('--------Parametros de la Gaussiana--------')								#parametros de la Gaussiana
print ('(En base a los canales y no a longitud de onda)')
print('Amplitud                 ' + str(A))
#print('Amplitud                 ' + str(A+y0))
print('Media                    ' + str(X0))
print('Sigma                    ' + str(desv))
print('desviacion del ajuste    ' + str(desviacion))								#Parametro de buen ajuste
print ()
print ('----------Parametros del pixel------------')
print('Monocromatico            ' + str(mono))
print('Continuo                 ' + str(y0))
print('FWHM                     ' + str(fwhm))
print('S/N                      ' + str(s_n))
print('lambda observada         ' + str(lambda_central))
#print('lambda baricentro        ' + str(lambda_bari))
print('velocidad observada      ' + str(v) + 'km/s')
#print('velocidad baricentro     ' + str(v_bari) + 'km/s')
#----------------------------------
# Grafica
plt.plot(lambda_file, datos_cubo, 'bo:', label='Senal')
#plt.plot(lambda_file,puntos,label='Senal')
plt.plot(lambda_file,gauss_fit(x,*popt),'ro:',label='Ajuste')
#plt.plot(lambda_file,gauss_fit(x,*popt),label='Ajuste')
plt.legend()
plt.title('Pixel = (' + str(equis+1) +',' + str(dimension[1] - ye) + ')')
plt.xlabel('Lambda')
plt.ylabel('Senal')
plt.show()
#-----------------------------