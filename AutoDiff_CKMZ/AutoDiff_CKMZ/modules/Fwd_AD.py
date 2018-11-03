import math

e = math.e

class Fwd_Diff():
  def __init__(self, x):
        self.val = x
        self.der = 1

  def __pow__(self, other):
  '''
  '''
    try:
      other = float(other)
      self.val = self.val**other
      self.der = other*self**(other-1)
    except:
      raise TypeError('Term in exponent must be a number.') 
    
  def exp(self):
    self.val = math.exp(self.val)
    self.der = self.der*math.exp(self)

  def log(self, base = None):
    if base == None:
       log(self, base = e)
    else:
      self.val = math.log(self.val)/math.log(base)
      self.der = self.der/math.log(base)*(1/self)