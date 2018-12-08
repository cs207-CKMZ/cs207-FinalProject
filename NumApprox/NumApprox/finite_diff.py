import math
import matplotlib.pyplot as plt
import numpy as np


#function to calculate acceleration via finite difference
def fdoubleprime(f, x):
    '''
    f: function of one variable (x)
    x: point at which the derivative should be calculated
    h: step size - smaller gets more accurate derivatives
    '''
    h = 1e-4
    return ( f(x+h) - 2*f(x) + f(x-h) ) / h**2

def calc_v(p0, v0, a):
    '''
    f: function of one variable
    p0: tuple - initial position
    v0: tuple - initial velocity
    '''
    t = 1
    return (v0[0] + a[0]*t, v0[1] + a[1]*t)

def calc_p(p0, v0, a):
    '''
    f: function of one variable
    p0: tuple - initial position
    v0: tuple - initial velocity
    '''
    t = 1
    return (v0[0]*t + 0.5*a[0]*t**2, v0[1]*t + 0.5*a[1]*t**2)

def accel(f, x):
    #returns tuple with acceleration split into x and y directions
    m = 1
    g = 9.8
    a_mag = fdoubleprime(f, x)
    print(m*g/a_mag)
    return (m*g*math.sin(math.acos(m*g/a_mag)), m*g)

def test_f(x):
    return x**2

def run_sim():
    v0 = (0,0)
    x0 = (1, test_f(-1.9))
    x = np.linspace(-5,5,500)
    y = [test_f(i) for i in x]
    #accel = [fdoubleprime(test_f,i) for i in x]
    xr = [0]
    for i in x:
        #a = fdoubleprime(test_f, i)
        a = accel(test_f,i)
        v0 = calc_v(x0, v0, a)
        newx  = calc_p(x0, v0, a)
        xr.append(newx)
        x0 = newx
    plt.plot(x,y,'r',newx,'b')
    #plt.legend('rollercoaster','acceleration')
    plt.show()

run_sim()

