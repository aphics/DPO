from scipy.optimize import minimize
import numpy as np

def gauss_1(x, A, mu, sigma, y0):
    gaussiana_1 = (A * np.exp( -(x-mu)**2 / (2*sigma**2) ) ) + y0
    return gaussiana_1

def gauss_2(x, A_1, mu_1, sigma_1, A_2, mu_2, sigma_2, y0):
    gaussiana_2 = ( A1 * np.exp( -(x-mu_1)**2 / 2*sigma_1**2 ) ) + 
                    ( A2 * np.epx( -(x-mu_2)**2 / 2*sigma_2**2 ) ) + y0