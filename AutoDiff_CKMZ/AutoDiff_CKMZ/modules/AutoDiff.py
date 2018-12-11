import numpy as np

class AutoDiff():
    """Class for Autodifferentiation objects, to be used for forward mode automatic differentiation

    INPUTS
    ======
    x: number or array of numbers, values at which the function and derivatives will be calculated
    dx: number or array of numbers, default is 1. Must be same dimensions as x
    """
    def __init__(self, x, dx = 1.0):
        self.x = x
        self.dx = np.array(dx)

    def __add__(self, other):
        """Overload addition
        
        INPUTS
        ======
        other: the second term to be added.
        
        RETURNS
        =======
        AutoDiff object which is the sum of self and other.
        
        EXAMPLES
        ========
        >>> x = AutoDiff(2.0)
        >>> x + 2
        AutoDiff(4.0, 1.0)
        
        >>> y = AutoDiff(2.0)
        >>> x + y
        AutoDiff(4.0, 2.0)
        """
        try:
            return AutoDiff(self.x+other.x, self.dx+other.dx)
        except AttributeError:
            return AutoDiff(self.x+other, self.dx)
        
    def __radd__(self, other):
        """Overload addition
        
        INPUTS
        ======
        other: the first term to be added.
        
        RETURNS
        =======
        AutoDiff object which is the sum of other and self.
        
        EXAMPLES
        ========
        >>> x = AutoDiff(2.0)
        >>> 2 + x
        AutoDiff(4.0, 1.0)
        """
        return self + other
    
    def __sub__(self, other):
        """Overload subtraction
        
        INPUTS
        ======
        other: subtrahend.
        
        RETURNS
        =======
        AutoDiff object which is the result of self-other.
        
        EXAMPLES
        ========
        >>> x = AutoDiff(1.0)
        >>> x - 1
        AutoDiff(0.0, 1.0)
        
        >>> y = AutoDiff(1.0)
        >>> x - y
        AutoDiff(0.0, 0.0)
        """
        try:
            return AutoDiff(self.x-other.x, self.dx-other.dx)
        except AttributeError:
            return AutoDiff(self.x-other, self.dx)
    
    def __rsub__(self, other):
        """Overload subtraction
        
        INPUTS
        ======
        other: minuend.
        
        RETURNS
        =======
        AutoDiff object which is the result of other - self.
        
        EXAMPLES
        ========
        >>> x = AutoDiff(1.0)
        >>> 1 - x
        AutoDiff(0.0, -1.0)
        """
        try:
            return AutoDiff(-self.x+other.x, -self.dx+other.dx)
        except AttributeError:
            return AutoDiff(-self.x+other, -self.dx)
        
    def __mul__(self, other):
        """Overload multiplication
        
        INPUTS
        ======
        other: the second term in the multiplication.
        
        RETURNS
        =======
        AutoDiff object which is the multiplication of self and other.
        
        EXAMPLES
        ========
        >>> x = AutoDiff(2.0)
        >>> x * 2
        AutoDiff(4.0, 2.0)
        
        >>> y = AutoDiff(2.0)
        >>> x * y
        AutoDiff(4.0, 4.0)
        """
        try:
            return AutoDiff(self.x * other.x, self.x * other.dx + self.dx * other.x)
        except AttributeError:
            return AutoDiff(self.x * other, self.dx * other)

    def __rmul__(self, other):
        """Overload multiplication
        
        INPUTS
        ======
        other: the first term in the multiplication.
        
        RETURNS
        =======
        AutoDiff object which is the multiplication of other and self.
        
        EXAMPLES
        ========
        >>> x = AutoDiff(2.0)
        >>> 2 * x
        AutoDiff(4.0, 2.0)
        """
        return self * other

    def __truediv__(self, other):
        """Overload division
        
        INPUTS
        ======
        other: divisor.
        
        RETURNS
        =======
        AutoDiff object which is the result of self/other.
        
        EXAMPLES
        ========
        >>> x = AutoDiff(2.0)
        >>> x / 2
        AutoDiff(1.0, 0.5)
        
        >>> y = AutoDiff(2.0)
        >>> x / y
        AutoDiff(1.0, 0.0)
        """
        try:
            return AutoDiff(self.x / other.x, (self.dx * other.x - self.x * other.dx)/other.x**2)
        except AttributeError:
            return AutoDiff(self.x / other, self.dx / other)
            
    def __rtruediv__(self, other):
        """Overload division
        
        INPUTS
        ======
        other: dividend.
        
        RETURNS
        =======
        AutoDiff object which is the result of other/self.
        
        EXAMPLES
        ========
        >>> x = AutoDiff(1.0)
        >>> 1 / x
        AutoDiff(1.0, -1.0)
        """
        if isinstance(other, AutoDiff):
            return other/self
        else:
            return AutoDiff(other,0)/self

    def __neg__(self):
        return AutoDiff(-self.x, -self.dx)

    def __repr__(self):
        return 'AutoDiff({}, {})'.format(self.x, self.dx)

    def __pow__(self, other):
        """Overwrites ** for AutoDiff objects

        INPUTS
        ======
        other: number or AutoDiff object, AutoDiff object is raised to this number.

        RETURNS
        =======
        AutoDiff object with all values raised to the nth power and derivatives according to the power rule.

        EXAMPLES
        =======
        >>> x = AutoDiff(2)
        >>> x**3.0
        AutoDiff(8.0, 12.0)
        """
        try:
            return AutoDiff(self.x ** other.x, self.x ** other.x * (other.dx * np.log(self.x) + other.x / self.x * self.dx))
        except AttributeError:
            if other == 0:
                return AutoDiff(self.x**other, 0)
            else:
                try:
                    other = float(other)
                    return AutoDiff(self.x**other, other*self.x**(other-1)*self.dx)
                except:
                    raise TypeError('Term in exponent must be a number. See AutoDiff.pow() for power functions') 

    def __rpow__(self, other):
        '''Overwrites ** for AutoDiff objects

        INPUTS
        =======
        other: float or AutoDiff object, the base of power

        RETURNS
        =======
        AutoDiff object performing other to the self, i.e. other^x

        EXAMPLES
        =======
        >>> x = AutoDiff(2.0, 1.0)
        >>> 2 ** x
        AutoDiff(4.0, 2.772588722239781)
        '''
        try:
            return AutoDiff(other.x ** self.x, other.x ** self.x * (self.dx * np.log(other.x) + self.x / other.x * other.dx))
        except AttributeError:
            if other <= 0:
                raise Exception('Error: non-positive value for logarithm')
            return AutoDiff(other ** self.x, other ** self.x * np.log(other) * self.dx)
    
    def __eq__(self, other):
        try:
            return (self.x == other.x) & (self.dx == other.dx)
        except AttributeError:
            return (self.x == other) & (self.dx == 0)
    
    def __ne__(self, other):
        return not (self == other)

# basic functions
def exp(AD):
    """Basic functions of the form e**x

    INPUTS
    ======
    AD: AutoDiff object or number or array of numbers

    RETURNS
    =======
    AutoDiff object with e**x as values and derivatives dx*e**x.

    EXAMPLES
    =======
    >>> x = AutoDiff(0)
    >>> exp(x)
    AutoDiff(1.0, 1.0)
    """
    try:
        return AutoDiff(np.exp(AD.x), AD.dx*np.exp(AD.x))
    except AttributeError:
        return np.exp(AD)


def log(AD, base=np.e):
    """Basic functions of the form log(x), where log is natural log
        
    INPUTS
    ======
    AD: AutoDiff object or number or array of numbers
        base: positive number, log base. If not given, will assume natural log.

    RETURNS
    =======
    AutoDiff object with log(x)/log(base) as values and derivatives dx/x.

    EXAMPLES
    =======
    >>> x = AutoDiff(100)
    >>> log(x, 10)
    AutoDiff(2.0, 0.004342944819032518)
    """
    try:
        base = float(base)
    except ValueError:
        raise ValueError('base must be a number.')
    try:
        return AutoDiff(np.log(AD.x)/np.log(base), AD.dx/np.log(base)*(1/AD.x))
    except AttributeError:
        return np.log(AD)/np.log(base)
    
def sin(AD):
    """sine function for auto-differentiation

    INPUTS
    ======
    AD: AutoDiff object, float, array-like variable

    RETURNS
    ======
    AutoDiff object of sin(AD)

    EXAMPLES
    ======
    >>> x = AutoDiff(0.0)
    >>> sin(x)
    AutoDiff(0.0, 1.0)
    """
    try:
        return AutoDiff(np.sin(AD.x), np.cos(AD.x) * AD.dx)
    except AttributeError:
        return np.sin(AD)

def cos(AD):
    """cosine function for auto-differentiation

    INPUTS
    ======
    AD: AutoDiff object, float, array-like variable

    RETURNS
    ======
    AutoDiff object of cos(AD)

    EXAMPLES
    ======
    >>> x = AutoDiff(0.0)
    >>> cos(x)
    AutoDiff(1.0, -0.0)
    """
    try:
        return AutoDiff(np.cos(AD.x), -np.sin(AD.x) * AD.dx)
    except AttributeError:
        return np.cos(AD)

def tan(AD):
    """tangent function for auto-differentiation

    INPUTS
    ======
    AD: AutoDiff object, float, array-like variable

    RETURNS
    ======
    AutoDiff object of tan(AD)

    EXAMPLES
    ======
    >>> x = AutoDiff(0.0, -1.0)
    >>> tan(x)
    AutoDiff(0.0, -1.0)
    """
    try:
        return AutoDiff(np.tan(AD.x), 1 / np.cos(AD.x) ** 2 * AD.dx)
    except AttributeError:
        return np.tan(AD)

def arcsin(AD):
    """arcsin function for auto-differentiation
    
    INPUTS
    ======
    AD: AutoDiff object, float, array-like variable

    RETURNS
    ======
    AutoDiff object of arcsin(AD)

    EXAMPLES
    ======
    >>> x = AutoDiff(0.5)
    >>> arcsin(x)
    AutoDiff(0.5235987755982989, 1.1547005383792517)
    """
    try:
        return AutoDiff(np.arcsin(AD.x), 1/np.sqrt(1-AD.x**2) * AD.dx)
    except AttributeError:
        return np.arcsin(AD)

def arccos(AD):
    """arccos function for auto-differentiation
    
    INPUTS
    ======
    AD: AutoDiff object, float, array-like variable

    RETURNS
    ======
    AutoDiff object of arccos(AD)

    EXAMPLES
    ======
    >>> x = AutoDiff(0.5)
    >>> arccos(x)
    AutoDiff(1.0471975511965979, -1.1547005383792517)
    """
    try:
        return AutoDiff(np.arccos(AD.x), -1/np.sqrt(1-AD.x**2) * AD.dx)
    except AttributeError:
        return np.arccos(AD)

def arctan(AD):
    """arctan function for auto-differentiation
    
    INPUTS
    ======
    AD: AutoDiff object, float, array-like variable

    RETURNS
    ======
    AutoDiff object of arctan(AD)

    EXAMPLES
    ======
    >>> x = AutoDiff(1)
    >>> arctan(x)
    AutoDiff(0.7853981633974483, 0.5)
    """
    try:
        return AutoDiff(np.arctan(AD.x), 1/(1+AD.x**2) * AD.dx)
    except AttributeError:
        return np.arctan(AD)
        
def sinh(AD):
    """Hyperbolic function sinh for auto-differentiation
    
    INPUTS
    ======
    AD: AutoDiff object, float, array-like variable

    RETURNS
    ======
    AutoDiff object of sinh(AD)

    EXAMPLES
    ======
    >>> x = AutoDiff(0)
    >>> sinh(x)
    AutoDiff(0.0, 1.0)
    """
    try:
        return AutoDiff(np.sinh(AD.x), np.cosh(AD.x) * AD.dx)
    except AttributeError:
        return np.sinh(AD)

def cosh(AD):
    """Hyperbolic function cosh for auto-differentiation
    
    INPUTS
    ======
    AD: AutoDiff object, float, array-like variable

    RETURNS
    ======
    AutoDiff object of cosh(AD)

    EXAMPLES
    ======
    >>> x = AutoDiff(0)
    >>> cosh(x)
    AutoDiff(1.0, 0.0)
    """
    try:
        return AutoDiff(np.cosh(AD.x), np.sinh(AD.x) * AD.dx)
    except AttributeError:
        return np.cosh(AD)

def tanh(AD):
    """Hyperbolic function tanh for auto-differentiation
    
    INPUTS
    ======
    AD: AutoDiff object, float, array-like variable

    RETURNS
    ======
    AutoDiff object of tanh(AD)

    EXAMPLES
    ======
    >>> x = AutoDiff(0)
    >>> tanh(x)
    AutoDiff(0.0, 1.0)
    """
    try:
        return AutoDiff(np.tanh(AD.x), 1/np.cosh(AD.x)**2 * AD.dx)
    except AttributeError:
        return np.tanh(AD)
      
def sqrt(AD):
    """square root function for AutoDiff objects

    INPUTS
    ======
    AD: AutoDiff object, float, array-like variable

    RETURNS
    =======
    AutoDiff object of sqrt(AD)

    EXAMPLES
    =======
    >>> x = AutoDiff(4)
    >>> sqrt(x)
    AutoDiff(2.0, 0.25)
    """
    return AD**0.5

def logistic(AD):
    """standard form logistic function for AutoDiff objects

        INPUTS
        ======
        AD: AutoDiff object, float, array-like variable

        RETURNS
        =======
        AutoDiff object of 1/(1+exp(-x))

        EXAMPLES
        =======
        >>> x = AutoDiff(0)
        >>> logistic(x)
        AutoDiff(0.5, 0.25)
        """
    try:
        return AutoDiff(1/(1+np.e**(-AD.x)), np.e**(-AD.x)/(1+np.e**(-AD.x))**2 * AD.dx)
    except AttributeError:
        return 1/(1+np.e**(-AD))

