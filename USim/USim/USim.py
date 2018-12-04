from AutoDiff_CKMZ import AutoDiff

g = 9.8 # acceleration m/s^2

def theta(potential):
  return AutoDiff.arctan(potential)
  # Possible difficulty: have to interpret text to functions.

def a_y(potential):
  t = theta(potential)
  return g*AutoDiff.sin(t)*AutoDiff.cos(t)-g

def a_x(potential):
  t = theta(potential)
  return g*AutoDiff.sin(t)**2

def xV(potential, v0=0, dt = 1):
  return v0 + dt*a_x(potential)

def yV(potential, v0=0, dt = 1):
  return v0 + dt*a_y(potential)