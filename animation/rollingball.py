#from AutoDiff_CKMZ.modules.AutoDiff import *
import sys

sys.path.append('../AutoDiff_CKMZ/AutoDiff_CKMZ/modules/')
from AutoDiff import *

class rollingball:
    def __init__(self, init_status=(1, 1, 0), G=9.8, curve=0, gradient=0, option=0):
        self.x, self.y, self.v = init_status # intial conditions: initial position, initial velocity
        self.curve = curve # curve function
        self.time_elapsed = 0
        self.G = G # g
        if gradient == None and option == 0:
            raise Exception('Error: No analytic derivative function provided!')
        self.gradient = gradient # analytic derivative function
        self.option = option # 0 for analytic derivative, 1 for AD, 2 for numerical method, for derivative
        self.ontrack = 1
        df_x = self.slope(self.x)
        sin_theta = df_x / (1 + df_x ** 2) ** 0.5
        cos_theta = 1 / (1 + df_x ** 2) ** 0.5
        self.vx = self.v * cos_theta
        self.vy = self.v * sin_theta

    def position(self):
        return (self.x, self.y)
    
    def velocity(self):
        return self.v
    
    def slope(self, x):
        if self.option == 0:
            return self.gradient(x)
        if self.option == 1:
            # implement AD here
            obj = AutoDiff(x)
            return self.curve(obj).dx
        if self.option == 2:
            h = 1e-2  # 'dx' or step size for numerical approximation
            return (self.curve(x + h) - self.curve(x)) / h
    
    def acceleration(self, x):
        df_x = self.slope(x)
        a = - self.G * df_x / (1 + df_x ** 2) ** 0.5
        
        return a

    def ont(self, dt):
        a = self.acceleration(self.x)
        df_x = self.slope(self.x)
        sin_theta = df_x / (1 + df_x ** 2) ** 0.5
        cos_theta = 1 / (1 + df_x ** 2) ** 0.5

        # update s and velocity
        tmp_v = self.v + a * dt
        delta_s = self.v * dt
        delta_x = delta_s * cos_theta
        delta_y = delta_s * sin_theta
        if (self.y + delta_y <= self.curve(self.x+delta_x)):
            self.v = tmp_v
            self.x += delta_x
            self.y += delta_y
            self.vx = self.v * cos_theta
            self.vy = self.v * sin_theta
        else:
            self.offt(dt)
            self.ontrack = 0

    def offt(self, dt):
        a = -self.G
        delta_x = self.vx * dt
        delta_y = self.vy * dt + 0.5 * a * dt ** 2
        if (self.y + delta_y > self.curve(self.x + delta_x)):
            self.vy += a * dt
            self.v = (self.vx ** 2 + self.vy ** 2) ** 0.5
            self.x += delta_x
            self.y += delta_y
        else:
            self.x += delta_x
            self.y = self.curve(self.x)
            df_x = self.slope(self.x)
            sin_theta = df_x / (1 + df_x ** 2) ** 0.5
            cos_theta = 1 / (1 + df_x ** 2) ** 0.5
            tmp_vx = self.vx
            tmp_vy = self.vy + a * dt
            self.v = tmp_vx * cos_theta + tmp_vy * sin_theta
            self.vx = self.v * cos_theta
            self.vy = self.v * sin_theta
            self.ontrack = 1
    
    def step(self, dt):
        if (self.ontrack == 0):
            self.offt(dt)
        else:
            self.ont(dt)
        self.time_elapsed += dt

