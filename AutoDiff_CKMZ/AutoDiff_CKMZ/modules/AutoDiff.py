import numpy as np

class AutoDiff():
    """Class for Autodifferentiation objects, to be used for forward mode automatic differentiation

    INPUTS
    ======
    x: number or array of numbers, values at which the function and derivatives will be calculated
    dx: number or array of numbers, default is 1. Must be same dimensions as x
    """
    def __init__(self, x, dx = 1):
        self.x = x
        self.dx = dx
        self._e = np.e

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
        >>> x = AutoDiff(2)
        >>> x + 2
        AutoDiff(4,1)
        
        >>> y = AutoDiff(2)
        >>> x + y
        AutoDiff(7,2)
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
        >>> x = AutoDiff(2)
        >>> 2 + x
        AutoDiff(4,1)
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
        >>> x = AutoDiff(1)
        >>> x - 1
        AutoDiff(0,1)
        
        >>> y = AutoDiff(1)
        >>> x - y
        AutoDiff(-1,0)
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
        >>> x = AutoDiff(1)
        >>> 1 - x
        AutoDiff(0,1)
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
        >>> x = AutoDiff(2)
        >>> x * 2
        AutoDiff(4,2)
        
        >>> y = AutoDiff(2)
        >>> x * y
        AutoDiff(4,8)
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
        >>> x = AutoDiff(2)
        >>> 2 * x
        AutoDiff(4,2)
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
        >>> x = AutoDiff(2)
        >>> x / 2
        AutoDiff(1,0.5)
        
        >>> y = AutoDiff(2)
        >>> x / y
        AutoDiff(1,0)
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
        >>> x = AutoDiff(1)
        >>> 1 / x
        AutoDiff(1,-1)
        """
        if isinstance(other, AutoDiff):
            return other/self
        else:
            return AutoDiff(other)/self

    def __neg__(self):
        return AutoDiff(-self.x, -self.dx)

    def __repr__(self):
        return 'AutoDiff({},{})'.format(self.x, self.dx)

    def __pow__(self, other):
        """Overwrites ** for AutoDiff objects

        INPUTS
        ======
        other: number, AutoDiff object is raised to this number.

        RETURNS
        =======
        AutoDiff object with all values raised to the nth power and derivatives according to the power rule.

        EXAMPLES
        =======
        >>> x = AutoDiff(2)
        >>> x**3
        AutoDiff(8, 12)
        """

        try:
            if other.x <= 0:
                raise Exception('Error: non-positive value for logarithm')
            return AutoDiff(other.x ** self.x, other.x ** self.x * (self.dx * np.log(other.x) + self.x / other.x * other.dx))
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
        other: float, the base of power

        RETURNS
        =======
        AutoDiff object performing other to the self, i.e. other^x

        EXAMPLES
        =======
        >>> x = AutoDiff(2, 1)
        >>> 2 ** x
        AutoDiff(4, 2.772588722239781)
        '''
        try:
            if other.x <= 0:
                raise Exception('Error: non-positive value for logarithm')
            return AutoDiff(other.x ** self.x, other.x ** self.x * (self.dx * np.log(other.x) + self.x / other.x * other.dx))
        except AttributeError:
            if other <= 0:
                raise Exception('Error: non-positive value for logarithm')
            return AutoDiff(other ** self.x, other ** self.x * np.log(other) * self.dx)

    # basic functions
    def exp(self, AD):
        """Basic functions of the form e**x

        INPUTS
        =======
        AD: AutoDiff object or number or array of numbers

        RETURNS
        =======
        AutoDiff object with e**x as values and derivatives dx*e**x.

        EXAMPLES
        =======
        >>> x = AutoDiff(0)
        >>> exp(x)
        AutoDiff(1, 1)
        """
        try:
            return AutoDiff(np.exp(AD.x), AD.dx*np.exp(AD.x))
        except AttributeError:
            return AutoDiff(np.exp(AD), 0)

    def log(self, AD, base = None):
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
        AutoDiff(2, 0.004342944819032518)
        """
        if base == None:
            log(self, base = np.e)
        else:
            try:
                return AutoDiff(np.log(AD.x)/np.log(base), AD.dx/np.log(base)*(1/AD.x))
            except AttributeError:
                return AutoDiff(np.log(AD)/np.log(base), 0)
                
    def sin(self, AD):
        # sine function
        try:
            return AutoDiff(np.sin(AD.x), np.cos(AD.x) * AD.dx)
        except AttributeError:
            return AutoDiff(np.sin(AD), 0)

    def cos(self, AD):
        # cosine function
        try:
            return AutoDiff(np.cos(AD.x), -np.sin(AD.x) * AD.dx)
        except AttributeError:
            return AutoDiff(np.cos(AD), 0)

    def tan(self, AD):
        # tangent function
        try:
            return AutoDiff(np.tan(AD.x), AD.dx / np.cos(AD.x) ** 2)
        except AttributeError:
            return AutoDiff(np.tan(AD), 0)

    def pow(self, AD1, AD2):
        # power function:
        if type(AD1) == AutoDiff and (type(AD2) == int or type(AD2) == float):
            return AD1 ** AD2
        elif type(AD2) == AutoDiff and (type(AD1) == int or type(AD1) == float):
            if AD1 <= 0:
                raise Exception('Error: non-positive value for logarithm')
            return AutoDiff(AD1 ** AD2.x, AD1 ** AD2.x * AD2.dx * np.log(AD1))
        elif type(AD1) == AutoDiff and type(AD2) == AutoDiff:
            if AD1.x <= 0:
                raise Exception('Error: non-positive value for logarithm')
            return AutoDiff(AD1.x ** AD2.x, AD1.x ** AD2.x * (AD2.dx * np.log(AD1.x) + AD2.x / AD1.x * AD1.dx))


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
    AutoDiff(1, 1)
    """
    try:
        return AutoDiff(np.exp(AD.x), AD.dx*np.exp(AD.x))
    except AttributeError:
        return AutoDiff(np.exp(AD), 0)


def log(AD, base=None):
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
    AutoDiff(2, 0.004342944819032518)
    """
    if base == None:
        base = np.e
    try:
        return AutoDiff(np.log(AD.x)/np.log(base), AD.dx/np.log(base)*(1/AD.x))
    except AttributeError:
        return AutoDiff(np.log(AD)/np.log(base), 0)
    
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
    AutoDiff(0.0,1.0)
    """
    try:
        return AutoDiff(np.sin(AD.x), np.cos(AD.x) * AD.dx)
    except AttributeError:
        return AutoDiff(np.sin(AD), 0)

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
    AutoDiff(1.0,0.0)
    """
    try:
        return AutoDiff(np.cos(AD.x), -np.sin(AD.x) * AD.dx)
    except AttributeError:
        return AutoDiff(np.cos(AD), 0)

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
    AutoDiff(0.0,-1.0)
    """
    try:
        return AutoDiff(np.tan(AD.x), 1 / np.cos(AD.x) ** 2 * AD.dx)
    except AttributeError:
        return AutoDiff(np.tan(AD), 0)

def pow(AD1, AD2):
    # power function:
    if type(AD1) == AutoDiff and (type(AD2) == int or type(AD2) == float):
        return AD1 ** AD2
    elif type(AD2) == AutoDiff and (type(AD1) == int or type(AD1) == float):
        if AD1 <= 0:
            raise Exception('Error: non-positive value for logarithm')
        return AutoDiff(AD1 ** AD2.x, AD1 ** AD2.x * AD2.dx * np.log(AD1))
    elif type(AD1) == AutoDiff and type(AD2) == AutoDiff:
        if AD1.x <= 0:
            raise Exception('Error: non-positive value for logarithm')
        return AutoDiff(AD1.x ** AD2.x, AD1.x ** AD2.x * (AD2.dx * np.log(AD1.x) + AD2.x / AD1.x * AD1.dx))

