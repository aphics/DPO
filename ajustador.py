from scipy.optimize import minimize
import numpy as np

def ajuste_gauss(x, A, mu, sigma):
    gaussiana_ = (A * np.exp( - (x - mu)**2 / (2 * sigma**2))) + y0
    return gaussiana_

def 