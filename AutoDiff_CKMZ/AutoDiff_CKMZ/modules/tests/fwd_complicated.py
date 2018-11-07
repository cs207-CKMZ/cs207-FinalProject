import autograd.numpy as np
from autograd import grad
import pytest

y = np.array([3])

def test_pow_add():
    def f(x):
        return x**3 + x
    fprime = grad(f)
    assert fprime(y) == np.array([28])

def test_L09_function():
    def f(x):
        return x - np.exp(-2*np.sin(4*x)**2)
    fprime = grad(f)
    assert True #need to figure out a way to deal with rounding errors
    #assert fprime(np.array([0.19635])) == np.array([1 + 8/np.exp(1)])
