import numpy as np

class AutoDiff():
	def __init__(self, x, dx = 1):
		self.x = x
		self.dx = dx
	
	def __add__(self, other):
		try:
			return AutoDiff(self.x+other.x, self.dx+other.dx)
		except AttributeError:
			return AutoDiff(self.x+other, self.dx)
		
	def __radd__(self, other):
		return self + other
	
	def __mul__(self, other):
		try:
			return AutoDiff(self.x * other.x, self.x * other.dx + self.dx * other.x)
		except AttributeError:
			return AutoDiff(self.x * other, self.dx * other)
	
	def __rmul__(self, other):
		return self * other
	
	def __truediv__(self, other):
		try:
			return AutoDiff(self.x / other.x, (self.dx * other.x - self.x * other.dx)/other.x**2)
		except AttributeError:
			return AutoDiff(self.x / other, self.dx / other)
			
	def __rtruediv__(self, other):
		if isinstance(other, AutoDiff):
			return other/self
		else:
			return AutoDiff(other)/self
	
	def __neg__(self):
        return AutoDiff(-self.x, -self.dx)
	
	def __repr__(self):
		print('x = {}, dx = {}'.format(self.x, self.dx))
	
	def __pow__(self, other):
  '''
  '''
		if other == 0:
			return AutoDiff(self.x**other, 0)
    try:
      other = float(other)
      return AutoDiff(self.x**other, other*self.x**(other-1)*self.dx)
    except:
      raise TypeError('Term in exponent must be a number. See AutoDiff.pow() for power functions') 
    
  def exp(self):
    return AutoDiff(np.exp(self.x), self.dx*np.exp(self.x))

  def log(self, base = None):
    if base == None:
       log(self, base = e)
    else:
      return AutoDiff(np.log(self.x)/np.log(base), self.dx/np.log(base)*(1/self.x))

	# basic functions
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
