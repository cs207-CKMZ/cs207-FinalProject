import AutoDiff_CKMZ.modules.AutoDiff as AD

class rollingball:
    
    def __init__(self, init_status=(1, 1, 0), G=9.8, curve=0, gradient=None, option=0, friction=0, tol=1e-1):
        self.x, self.y, self.v = init_status # intial conditions: initial position, initial velocity
        self.curve = curve # curve function
        self.time_elapsed = 0
        self.G = G # g
        if gradient == None and option == 0:
            raise Exception('Error: No analytic derivative function provided!')
        self.gradient = gradient # analytic derivative function
        self.option = option # 0 for analytic derivative, 1 for AD, 2 for numerical method, for derivative
        if friction < 1 and friction >= 0:
            self.friction = friction
        else:
            raise UserWarning('Wrong friction coefficient: should be from 0 to 1')
        self.tol = tol
           
    def position(self):
        return (self.x, self.y)
    
    def velocity(self):
        return self.v
    
    def slope(self, x):
        if self.option == 0:
            return self.gradient(x)
        if self.option == 1:
            # implement AD here
            obj = AD.AutoDiff(x)
            return self.curve(obj).dx
        if self.option == 2:
            # implement numerical method here
            h = 1e-2
            return (self.curve(x + h) - self.curve(x)) / h
    
    def acceleration(self, x):
        df_x = self.slope(x)
        a = - self.G * df_x / (1 + df_x ** 2) ** 0.5 - self.sign() * self.friction * self.G / (1 + df_x ** 2) ** 0.5
        
        return a
    
    def sign(self):
        if self.v > 0:
            return 1
        elif self.v < 0:
            return -1
        else:
            return 0
    
    def step(self, dt):
        self.time_elapsed += dt
        x = self.x
        y = self.y
        a = self.acceleration(x)
        df_x = self.slope(x)
        sin_theta = df_x / (1 + df_x ** 2) ** 0.5
        cos_theta = 1 / (1 + df_x ** 2) ** 0.5
        
        
        # update s and velocity
        self.v += a * dt
        delta_s = self.v * dt
        delta_x = delta_s * cos_theta
        delta_y = delta_s * sin_theta
        # update x and y
        self.x += delta_x
        self.y += delta_y
        
        # check if the ball is still on the curve
        y_curve = self.curve(self.x)
        if abs(y_curve - self.y) > self.tol:
            raise UserWarning('Ball flies off. Animation terminates.')
