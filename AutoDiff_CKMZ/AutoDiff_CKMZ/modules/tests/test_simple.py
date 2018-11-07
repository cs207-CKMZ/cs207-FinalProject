import pytest
import numpy as np
from AutoDiff_CKMZ.modules.AutoDiff import AutoDiff as AD

x1 = AD(2)
x2 = AD(3)

'''def test_add():
    assert x1.x + x2.x == 5
    assert x1.dx + x2.dx == 2

def test_sub():
    assert x2.x - x1.x == 1
    assert x2.dx - x1.dx == 2
'''
def test_pow_add():
    f = x1**3 + x1
    assert f.x == 10
    assert f.dx == 13

def test_mul_sub():
    f = 2*x1 - 4
    assert f.x == 0
    assert f.dx == 2

def test_pow_div_add():
    f = x1**4/2 - 3
    assert f.x == 5
    assert f.dx == 16
