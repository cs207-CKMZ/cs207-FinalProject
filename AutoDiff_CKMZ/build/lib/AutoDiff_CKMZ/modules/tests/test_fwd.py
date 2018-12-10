import pytest
import numpy as np
#from AutoDiff_CKMZ.modules.AutoDiff import AutoDiff
import AutoDiff_CKMZ.modules.AutoDiff as AD

x1 = AD.AutoDiff(2.0)
x2 = AD.AutoDiff(3.0)

tol = 1e-8

def test_add():
    f = x1 + 3
    assert f.x == 5
    assert f.dx == 1

def test_radd():
    f = 1 + x1
    assert f.x == 3
    assert f.dx == 1

def test_sub():
    f = x1 - 3
    assert f.x == -1
    assert f.dx == 1

def test_rsub():
    f = 3 - x1
    assert f.x == 1
    assert f.dx == -1

def test_mul():
    f = x1*x2
    assert f.x == 6
    assert f.dx == 5

def test_rmul():
    f = 3*x1
    assert f.x == 6
    assert f.dx == 3

def test_div():
    f = x1/x2
    assert f.x == 2/3
    assert f.dx == (1/3) - 2/9

def test_rdiv():
    f = 4/x1
    assert f.x == 2
    assert f.dx == -1
    f = x1.__rtruediv__(x2)
    assert f.x == 3/2.0
    assert f.dx == -0.25

def test_neg():
    f = -x1
    assert f.x == -2
    assert f.dx == -1

def test_pow():
    f = x1**3
    assert f.x == 8
    assert f.dx == 12
    try:
        AD.AutoDiff(-2.0)**3
    except Exception:
        assert True
    f = x1**0
    assert f.x == 1
    assert f.dx == 0
    try:
        x1**'a'
    except TypeError:
        assert True

def test_rpow():
    f = 3**x1
    assert f.x == 9
    assert tol > abs (f.dx - 9.887510598)
    f = x1.__rpow__(x2)
    assert f.x == 9
    assert tol > abs (f.dx - 15.8875106)
    try:
        x1.__rpow__(AD.AutoDiff(-2.0))
    except Exception:
        assert True
    try:
        (-2.0)**x1
    except Exception:
        assert True

def test_eq():
    assert x1 == AD.AutoDiff(2.0)
    assert AD.AutoDiff(2.0, 0) == 2.0

def test_ne():
    assert x1 != x2

def test_exp():
    f = AD.exp(x1)
    assert f.x == np.exp(2)
    assert f.dx == np.exp(2)

def test_log():
    f = AD.log(x1)
    assert f.x == np.log(2)
    assert f.dx == 1/2

def test_sin():
    f = AD.sin(x1)
    assert f.x == np.sin(2)
    assert f.dx == np.cos(2)

def test_cos():
    f = AD.cos(x1)
    assert f.x == np.cos(2)
    assert f.dx == -np.sin(2)

def test_tan():
    f = AD.tan(x1)
    assert f.x == np.tan(2)
    assert f.dx == 1/np.cos(2)**2

def test_arctan():
    f = AD.arctan(x1)
    assert f.x == np.arctan(2)
    assert f.dx == 1/(1+2**2)
    f = AD.arctan(0.5)
    assert f.x == np.arctan(0.5)
    assert f.dx == 0

def test_arccos():
    f = AD.arccos(AD.AutoDiff(0.5))
    assert f.x == np.arccos(0.5)
    assert f.dx == -1/np.sqrt(1-0.5**2)
    f = AD.arccos(0.5)
    assert f.x == np.arccos(0.5)
    assert f.dx == 0

def test_arcsin():
    f = AD.arcsin(AD.AutoDiff(0.5))
    assert f.x == np.arcsin(0.5)
    assert f.dx == 1/np.sqrt(1-0.5**2)
    f = AD.arcsin(0.5)
    assert f.x == np.arcsin(0.5)
    assert f.dx == 0

def test_tanh():
    f = AD.tanh(x1)
    assert f.x == np.tanh(2)
    assert f.dx == 1/(np.cosh(2)**2)
    f = AD.tanh(2)
    assert f.x == np.tanh(2)
    assert f.dx == 0

def test_cosh():
    f = AD.cosh(x1)
    assert f.x == np.cosh(2)
    assert f.dx == np.sinh(2)
    f = AD.cosh(0.5)
    assert f.x == np.cosh(0.5)
    assert f.dx == 0

def test_sinh():
    f = AD.sinh(x1)
    assert f.x == np.sinh(2)
    assert f.dx == np.cosh(2)
    f = AD.sinh(0.5)
    assert f.x == np.sinh(0.5)
    assert f.dx == 0

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
