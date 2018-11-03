#for now, write the tests on the autograd package - must be sure that our tests work!
#additionally, begin with tests for scalar functions of a scalar

import autograd.numpy as np
from autograd import grad
import pytest
#import AutoDiff_CKMZ.Fwd_AD as Fwd_AD

y = np.array([3])

def test_add():
    def f(x):
        return x + x
    fprime = grad(f)
    assert fprime(y) == np.array([2])

def test_sub():
    def f(x):
        return x - x
    fprime = grad(f)
    assert fprime(y) == np.array([0])

def test_mul():
    def f(x):
        return 4*x
    fprime = grad(f)
    assert fprime(y) == np.array([4])

def test_div():
    def f(x):
        return x/4
    fprime = grad(f)
    assert fprime(y) == np.array([1/4])

def test_neg():
    def f(x):
        return -x
    fprime = grad(f)
    assert fprime(y) == np.array([-1])

def test_pow():
    def f(x):
        return x**2
    fprime = grad(f)
    assert fprime(y) == np.array([6])

def test_sin():
    fprime = grad(np.sin)
    assert fprime(np.pi) == np.array([-1])

def test_arcsin():
    fprime = grad(np.arcsin)
    assert True

def test_cos():
    fprime = grad(np.cos)
    assert fprime(np.pi/2) == np.array([-1])

def test_arccos():
    fprime = grad(np.arccos)
    assert True

def test_tan():
    fprime = grad(np.tan)
    assert fprime(np.pi) == np.array([1])

def test_arctan():
    fprime = grad(np.arctan)
    assert True

def test_e():
    fprime = grad(np.exp)
    assert fprime(y) == np.exp(y)

def test_ln():
    fprime = grad(np.log)
    assert fprime(y) == np.array(1/y)

