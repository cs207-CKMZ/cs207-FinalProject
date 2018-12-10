import math
import matplotlib.pyplot as plt
import numpy as np


#function to calculate acceleration via finite difference
def deriv(f, x):
    '''
    f: function of one variable (x)
    x: point at which the derivative should be calculated
    h: step size - smaller gets more accurate derivatives
    '''
    h = 1e-4
    return ( f(x+h) - f(x) ) / h

def calc_v(p0, v0, a, t):
    '''
    f: function of one variable
    p0: tuple - initial position
    v0: tuple - initial velocity
    '''
    return (v0[0] + a[0]*t, v0[1] + a[1]*t)

def calc_p(p0, v0, a, t):
    '''
    f: function of one variable
    p0: tuple - initial position
    v0: tuple - initial velocity
    '''
    #return v0*t + 0.5*a*t**2
    return (v0[0]*t + 0.5*a[0]*t**2, v0[1]*t + 0.5*a[1]*t**2)

def accel(f, x):
    #returns tuple with acceleration split into x and y directions
    m = 1
    g = -9.8
    theta = np.arctan(deriv(f,x))
    ax = -g*np.sin(theta)*np.cos(theta)
    ay = -g*np.sin(theta)*np.sin(theta)
    return (ax,ay)

def test_f(x):
    return x**2

def run_sim(f=test_f, x0=1, v0=0, xmin=-5, xmax=5):
    if v0 != 0:
        pass
        #calculate based on a triangle for x and y
    x = np.linspace(xmin,xmax,500) #plot test function
    y = [f(i) for i in x] #plot test function
    xr = [x0] #add initial position to the output list
    t = np.linspace(0,10,5000) #define a range of times
    count = 0
    for i in t: #loop over times
        #a = fdoubleprime(test_f, i)
        a = accel(f,xr[count]) #calculate acceleration
        #v0 = calc_v(x0, v0, a)
        newx  = calc_p(x0, v0, a, i)
        xr.append(newx)
        x0 = newx
        count += 1
    plt.plot(x,y,'r',xr,[f(i) for i in xr],'b')
    plt.show()
    return xr, [f(i) for i in xr]
