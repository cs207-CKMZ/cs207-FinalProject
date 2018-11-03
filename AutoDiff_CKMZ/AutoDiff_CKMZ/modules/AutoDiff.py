import numpy as np

lass AutoDiff():
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
	
	# basic functions
	def sin(self, other):
		# sine function
		return AutoDiff(np.sin(other.x), np.cos(other.x) * other.dx)
	
	def cos(self, other):
		# cosine function
		return AutoDiff(np.cos(other.x), -np.sin(other.x) * other.dx)

	def tan(self, other):
		# tangent function
		return AutoDiff(np.tan(other.x), other.dx / np.cos(other.x) ** 2)

	def pow(self, x, other):
		# power function:
		if x <= 0:
			raise Exception('Error: non-positive value for logarithm')
		return AutoDiff(x ** other.x, x ** other.x * other.dx * np.log(x))


		