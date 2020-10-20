from scipy.optimize import minimize
import numpy as np

def gauss_1(x, A, mu, sigma, y0):
    gaussiana_1 = (A * np.exp( -(x-mu)**2 / (2*sigma**2) ) ) + y0
    return gaussiana_1

def gauss_2(x, A_1, mu_1, sigma_1, A_2, mu_2, sigma_2, y0):
    gaussiana_2 = ( A_1 * np.exp( -(x-mu_1)**2 / 2*sigma_1**2 ) ) + 
                    ( A_2 * np.epx( -(x-mu_2)**2 / 2*sigma_2**2 ) ) + y0
    return gaussiana_2

def gauss_3(x, A_1, mu_1, sigma_1, A_2, mu_2, sigma_2, A_3, mu_3, sigma_3, y0):
    gaussiana_3 = ( A_1 * np.exp( -(x-mu_1)**2 / 2*sigma_1**2 ) ) + 
                    ( A_2 * np.epx( -(x-mu_2)**2 / 2*sigma_2**2 ) ) +
                        ( A_3 * np.epx( -(x-mu_3)**2 / 2*sigma_3**2 ) ) + y0
    return gaussiana_3

def gauss_4(x, A_1, mu_1, sigma_1, A_2, mu_2, sigma_2, A_3, mu_3, sigma_3, A_4, mu_4, sigma_4, y0):
    gaussiana_4 = ( A_1 * np.exp( -(x-mu_1)**2 / 2*sigma_1**2 ) ) + 
                    ( A_2 * np.epx( -(x-mu_2)**2 / 2*sigma_2**2 ) ) +
                        ( A_3 * np.epx( -(x-mu_3)**2 / 2*sigma_3**2 ) ) +
                            ( A_4 * np.epx( -(x-mu_4)**2 / 2*sigma_4**2 ) ) + y0
    return gaussiana_4


