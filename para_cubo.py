#----------------------------
#Autor: Edgar Sandoval Trejo
#
#Este programa ajusta de ser posible una funcion Gaussiana a cada pixel de
#un cubo de datos de dimensiones (x,y,z), donde la coordenada z es el
#numero de canal.
#El ajuste devuelve los parametros de la funcion Gaussiana, Amplitud,
#desviacion (sigma) y la media, con los cuales se calculan los valores de
#longitud de onda y velocidad observada, senal a ruido, FWHM, Monocromatico
#y Continuo para cada pixel y posteriormente se genera una imagen tipo
#FITS de cada mapa
#
#Ultima actualizacion: 25 enero 2018
# Librerias usadas
import numpy as np
from astropy.visualization import astropy_mpl_style
import matplotlib.pyplot as plt
plt.style.use(astropy_mpl_style)
from astropy.utils.data import download_file
from astropy.io import fits
from scipy import asarray as ar,exp
from scipy.optimize import curve_fit
from astropy.table import Table
from scipy.integrate import quad										#Paqueteria para integrar
#
from tqdm import tqdm													#Paqueteria para generar barra de progreso
from time import sleep
#-----------------------------
# Definicion de las funciones Guassianas a ajustar
def gauss_fit(x,a,x0,sigma,y0):
	return y0+a*np.exp(-(x-x0)**2/(2*sigma**2))
def gaussiana(x,A,X0,desv):
	return A*np.exp((-(x-X0)**2)/(2*desv**2))
#-----------------------------
# Codigo
image_file = raw_input("Ingresa el nombre del archivo fits: ")							#Nombre del archivo
hdu_list = fits.open(image_file)   										#Apertura del archivo fits
image_data = hdu_list[0].data      										#Carga la informacion fits en un arreglo
#print(type(image_data))           										#Descomentar para conocer tipo de archivo
dim = image_data.shape             										#Obtiene las dimensiones del cubo. El arreglo esta invertido z,y,x
print('Dimensiones del cubo')
print('(x,y,z) = ('+str(dim[2])+','+str(dim[1])+','+str(dim[0])+')')
print
hdu_list.close()                   										#Cierre del archivo fits. La informacion ya se cargo en la variable image_data
print()
lmb_ch1 = input('Longitud de onda del primer canal (En Angstrom): ')
resol_ch = input('Valor de la resolucion por canal (En Angstrom): ')
print()
lambda_file = []
for i in range(dim[0]):
	lambda_file.append(lmb_ch1+(i*resol_ch))
#------------------------------
#Creacion de archivos FITS
signal_noise = fits.PrimaryHDU()										#Archivo FITS de Senal a ruido
signal_noise.data = np.zeros((dim[1],dim[2]))

continuo = fits.PrimaryHDU()											#Archivo FITS del Continuo
continuo.data = np.zeros((dim[1],dim[2]))

velocity_field = fits.PrimaryHDU()										#Archivo FITS de mapa de velocidades
velocity_field.data = np.zeros((dim[1],dim[2]))

fwhm_field = fits.PrimaryHDU()											#Archivo FITs de FWHM
fwhm_field.data = np.zeros((dim[1],dim[2]))

mono_field = fits.PrimaryHDU()											#Archivo FITS del Monocromatico
mono_field.data = np.zeros((dim[1],dim[2]))
################################################################
# Llenar de valores None
for i in range(dim[2]):
	for j in range(dim[1]):
		signal_noise.data[j,i]=None
		continuo.data[j,i]=None
		velocity_field.data[j,i]=None
		fwhm_field.data[j,i]=None
		mono_field.data[j,i]=None
#------------------------------
sr = input('Ingresar el valor de senal a ruido para trabajar: ')						#Senal a ruido para trabajar
print
for i in tqdm(range(dim[2]),desc='Progreso'):									#Rango en coordenada x
	for j in range(dim[1]):									       		#Rango en coordenada y
		#print(' x = '+str(i+1)+' y ='+str(j))
		#sleep(0.1)
		puntos = image_data[0:dim[0], j, i]
		min_aux = min(puntos)
		continuo.data[j,i]=sum(puntos)/dim[0]
		if min_aux >= 0.0:										#Condicionante para no trabajar con valores negativos
			x=ar(range(dim[0]))
			x=x+1
			#-------------------------------
			mean = sum(x*puntos)/sum(puntos)							#Media
			sigma = np.sqrt(sum(puntos*(x-mean)**2)/sum(puntos))					#Desviacion estandar
			M = np.max(puntos)									#Condicion inicial para la amplitud
			if M == 0:
				M = mean
			X0 = np.argmax(puntos)									#Condicion inicial para la lambda central
			#--------------
			# Ajuste
			try:											#Ajuste en caso de encontrar parametros iniciales
				popt, pcov = curve_fit(gauss_fit,x,puntos,p0=[mean,X0,sigma,1.0])
				A = popt[0]									#Amplitud de Gaussiana respecto a y0
				lambda_central = popt[1]							#Lamba central de la Gaussiana
				desv = popt[2]									#Desviacion estandar
				y0 = popt[3]									#Valor de y0
				s_n=(A+y0)/y0									#Senal a ruido
				fwhm = 2 * np.sqrt(2*np.log(10))*np.absolute(desv)				#FWHM
				mono = quad(gaussiana, 1, dim[0], args=(A,X0,desv))				#Calculo del monocromatico
				mono = mono[0]									#Valor del monocromatico
				#-----------
				suma = 0
				for k in range(dim[0]):
					f_fit = gauss_fit(x[k],A,X0,desv,y0)
					dif = (puntos[k] - f_fit)/np.max(puntos)				#Incluye normalizacion
					suma = suma + dif**2
				desviacion = np.sqrt(suma/dim[0])						#Parametro de buen ajuste
				#-----------
				pend = 0									#Calculo de la velocidad
				def linea(x,pend,b):								#Funcion para interpolar lambda
					return (pend*x)+b
				popt2, pcov2 = curve_fit(linea,x,lambda_file,p0=None)
				m = popt2[0]									#Pendiendte de la recta
				b = popt2[1]									#Ordenada al origen
				lambda_central = (m*X0)+b							#Valor de lambda respecto al valor maximo del ajuste
				v = 299792.458*((lambda_central/6562.8)-1)					#Velocidad calculada de Doppler
				#-----------
				if s_n>=sr and desviacion<=0.15 and desv<2*dim[0]/3:				#Condiciones de buen pixel:
					signal_noise.data[j,i] = s_n						#Asigna los valores correspondientes
					continuo.data[j,i] = y0							#dado que el ajuste fue bueno y cumple
					velocity_field.data[j,i] = v						#con el criterio de buena senal a ruido
					fwhm_field.data[j,i] = fwhm
					mono_field.data[j,i] = mono
				else:
					signal_noise.data[j,i] = None
					velocity_field.data[j,i] = None
					fwhm_field.data[j,i] = None
					mono_field.data[j,i] = None
			except:											#En caso de NO ajustar
				signal_noise.data[j, i] = None							#S/N = 0
				velocity_field.data[j,i] = None							#Velocidad = 0
				fwhm_field.data[j,i] = None							#FWHM = 0
				mono_field.data[j,i] = None							#Mono = 0
#--------------------------------
name = image_file[:-5]
sn_name = 'SR_' + name + '_sn' + str(sr) + '.fits'
con_name = 'CONT_' + name + '_sn' + str(sr) + '.fits'
vf_name = 'VF_' + name + '_sn' + str(sr) + '.fits'
fwhm_name = 'FWHM_' + name + '_sn' + str(sr) + '.fits'
mono_name = 'Mono_' + name + '_sn' + str(sr) + '.fits'
signal_noise.writeto(sn_name, overwrite=True)									#Escritura a archivo FITS senal a ruido
continuo.writeto(con_name, overwrite=True)									#Escritura a archivo FITS continuo
velocity_field.writeto(vf_name, overwrite=True)									#Escritura a archivo FITs campo de velocidades
fwhm_field.writeto(fwhm_name, overwrite=True)									#Escritura a archivo FITS FWHM
mono_field.writeto(mono_name, overwrite=True)									#Escritura a archivo FITS monocromatico