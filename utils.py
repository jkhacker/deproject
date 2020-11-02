import numpy as np

def gen_func(x, y):
    return 2*np.exp(x) - y

def exact_func(x, c):
    return np.exp(x) + c*np.exp(-x)

def find_coef(x0, y0):
    return (y0 - np.exp(x0))/np.exp(-x0)

def func_title():
    return "y' = 2e^x - y"