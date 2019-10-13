import numpy as np
from scipy.optimize import curve_fit
from scipy.integrate import quad


def gauss_fit(x, a, x0, sigma, y0):
    return y0 + (a * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2)))


def gauss_fit_sin_continuo(x, a, x0, sigma):
    return a * (np.exp((-(x - x0)**2) / (2 * (sigma**2))))


def param_pixel(datos_pixel, lambda_file, dimension_z):
    min_aux = min(datos_pixel)
    # Condicion para no tabajar con valores negativos
    if min_aux >= 0:
        # Valor de la media calculada a partir del baricentro
        media_inicial = sum(lambda_file*datos_pixel)/sum(datos_pixel)

        # Valor de la dispersion (sigma)
        sigma_inicial = np.sqrt(sum(datos_pixel*(lambda_file-media_inicial)**2)/sum(datos_pixel))

        # Condicion inicial para Amplitud
        amplitud_inicial = np.max(datos_pixel)

        # Ajuste
        try:
            # Se ajusta una funcion Gaussiana usando la funcion curve_fit
            # La variable popt devuelve un arreglo con los parametros del ajuste
            # La variable pcov devuelve la matriz de covarianza
            popt, pcov = curve_fit(gauss_fit, lambda_file, datos_pixel, p0=[amplitud_inicial, media_inicial, sigma_inicial, 1])
            amplitud_gaussiana = popt[0]
            lambda_observada = popt[1]
            sigma = popt[2]
            continuo = popt[3]

            # Se calcula el Full Width at Half Maximum utilizando el valor sigma
            fwhm = 2 * np.sqrt(2*np.log(10))*np.absolute(sigma)

            # Se calcula el monocromatico usando la funcion quad
            # La funcion quad devuelve un arreglo donde la primer entrada corresponde
            # al valor de la integral y la segunda al erro relativo.
            # Posteriormente se redefine la variable como el valor de la integral
            mono = quad(gauss_fit_sin_continuo, lambda_file[0], lambda_file[-1], args=(amplitud_gaussiana, lambda_observada, sigma))
            mono = mono[0]

            # Se calcula la velocidad observada respecto de Halpha
            velocidad_observada = 299792.458 * ((lambda_observada / 6562.8) - 1)

            # Se calcula el parametro buen_ajuste. Este parametro cuantifica que tan bueno fue el ajuste
            # Para calcular se normaliza el ajuste y datos_pixel con el maximo de ambos conjuntos de datos
            # Este parametro se calcula:
            # buen ajuste = sqrt(1/N * sum((datos_pixel_normal[i] - ajuste_normal[i])**2))
            # La formula para obtener este parametro es similar a la desviacion estandar

            ajuste = gauss_fit(lambda_file, amplitud_gaussiana, lambda_observada, sigma, continuo)
            maximo_ajuste_y_datos = max(max(ajuste), max(datos_pixel))
            datos_pixel_normal = datos_pixel / maximo_ajuste_y_datos
            ajuste_normal = ajuste / maximo_ajuste_y_datos

            diferencia_datos_ajuste = np.absolute(datos_pixel-ajuste)
            diferencia_datos_ajuste_normal = np.absolute(datos_pixel_normal - ajuste_normal)

            buen_ajuste = np.sqrt(np.sum(diferencia_datos_ajuste_normal*diferencia_datos_ajuste_normal)/dimension_z)

            observables = [amplitud_gaussiana, lambda_observada, sigma, continuo, fwhm, mono, velocidad_observada]
            analisis = [ajuste, ajuste_normal, datos_pixel_normal, diferencia_datos_ajuste, diferencia_datos_ajuste_normal, buen_ajuste]

            parametros = [observables, analisis]

            return parametros
        except:
            print "error en calculo"
