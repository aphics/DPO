import numpy as np
from scipy.optimize import curve_fit
from scipy.integrate import quad


def gauss_fit(x, a, x0, sigma, y0):
    return y0 + (a * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2)))


def gauss_fit_sin_continuo(x, a, x0, sigma):
    return a * np.exp((-(x - x0) ** 2) / (2 * sigma ** 2))


def param_pixel(datos_pixel, lambda_file, dimension_z):
    min_aux = min(datos_pixel)
    continuo = sum(datos_pixel)/dimension_z
    # Condicion para no tabajar con valores negativos
    if min_aux >= 0:
        # Valor de la media calculada a partir del baricentro
        media_inicial = sum(lambda_file*datos_pixel)/sum(datos_pixel)

        # Valor de la dispersion (sigma)
        sigma_inicial = np.sqrt(sum(datos_pixel*(lambda_file-media_inicial)**2)/sum(datos_pixel))

        # Condicion inicial para Amplitud
        amplitud_inicial = np.max(datos_pixel)
        if amplitud_inicial == 0:
            amplitud_inicial = media_inicial

        # Condicion inicial para lambda central
        lambda_central_inicial = np.argmax(datos_pixel)

        # Ajuste
        try:
            popt, pcov = curve_fit(gauss_fit, lambda_file, datos_pixel, p0=[media_inicial, lambda_central_inicial, sigma_inicial, 1])
            amplitud_gaussiana = popt[0]
            lambda_central = popt[1]
            sigma = popt[2]
            continuo = popt[3]
            fwhm = 2 * np.sqrt(2*np.log(10))*np.absolute(sigma)
            mono = quad(gauss_fit_sin_continuo, 1, dim[0], args=(A,X0,desv))
            mon0 = mono[0]

            return amplitud_gaussiana


        except:
            print("error en calculo")
