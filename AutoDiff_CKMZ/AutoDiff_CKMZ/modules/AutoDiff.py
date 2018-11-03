class AutoDiff:
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
	
	def __repr__(self):
		print('x = {}, dx = {}'.format(self.x, self.dx))
		