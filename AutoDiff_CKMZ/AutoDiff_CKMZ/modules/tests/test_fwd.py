import pytest
import numpy as np
#from AutoDiff_CKMZ.modules.AutoDiff import AutoDiff
import AutoDiff_CKMZ.modules.AutoDiff as AD

x1 = AD.AutoDiff(2.0)
x2 = AD.AutoDiff(3.0)

tol = 1e-8

def test_pow_add():
    f = x1**3 + x1
    assert f.x == 10.0
    assert f.dx == 13.0

def test_mul_sub():
    f = 2*x1 - 4
    assert f.x == 0
    assert f.dx == 2

def test_pow_div_add():
    f = x1**4/2 - 3
    assert f.x == 5
    assert f.dx == 16

def test_sin_pow_log():
    f = AD.sin(x1)**2*AD.log(x1)
    assert tol > abs(f.x - 0.573109206726)
    assert tol > abs(f.dx - -0.111164610647518727)


def test_tan_exp_div_neg():
    f = -AD.tan(x1)/AD.exp(x1)
    assert tol > abs(f.x - 0.29571298878)
    assert tol > abs(f.dx - -1.077192940578)

def test_cos_log10_rpow():
    f = AD.cos(AD.log(2**x1,base=10))
    assert tol > abs(f.x - 0.82417070595)
    assert tol > abs(f.dx - -0.17048576675265)

def test_log_invalid_base():
    with pytest.raises(ValueError):
        AD.log(x1, base='a')

def test_notADinput():
    f = AD.cos(1)
    assert f.x == np.cos(1)
    assert f.dx == 0

    f = AD.sin(1)
    assert f.x == np.sin(1)
    assert f.dx == 0

    f = AD.tan(1)
    assert f.x == np.tan(1)
    assert f.dx == 0

    f = AD.log(1)
    assert f.x == np.log(1)
    assert f.dx == 0

    f = AD.exp(1)
    assert f.x == np.exp(1)
    assert f.dx == 0
