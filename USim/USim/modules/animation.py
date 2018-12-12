import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import USim.USim.modules.rollingball as RB
import AutoDiff_CKMZ.modules.AutoDiff as AD
from time import time

function_list = [lambda x: AD.sin(x), 
                 lambda x: AD.exp(x), 
                 lambda x: x * AD.sin(x), 
                 lambda x: - AD.log(x), 
                 lambda x: AD.sinh(x), 
                 lambda x: AD.log(x),
                 lambda x: AD.exp(AD.cos(x)),
                 lambda x: 2 ** x, 
                 lambda x: 1 / AD.tan(x), 
                 lambda x: AD.sin(x) / x, 
                 lambda x: 1 / x]


derivative_list = [lambda x: np.cos(x), 
                   lambda x: np.exp(x), 
                   lambda x: np.sin(x) + x * np.cos(x), 
                   lambda x: -1 / x, 
                   lambda x: np.cosh(x), 
                   lambda x: 1 / x,
                   lambda x: - np.exp(np.cos(x)) * np.sin(x),
                   lambda x: 2 ** x * np.log(2), 
                   lambda x: - 1 / np.sin(x) ** 2, 
                   lambda x: (x * np.cos(x) - np.sin(x)) / x ** 2, 
                   lambda x: - 1 / x ** 2]

class function():
    def __init__(self, function_list=None, AD=False):
        self.function_list = function_list
        self.num = len(function_list)
        self.AD = AD
    
    def __getitem__(self, key):
        try: 
            return self.function_list[key]
        except IndexError:
            raise UserError('function index out of range')

function_set = function(function_list)
derivative_set = function(derivative_list)

class Animation():
    def __init__(self, function_index=0, 
                 init_status=(0, 0), 
                 x_range=(0, 4), 
                 option=1, 
                 friction=0,
                 dt=0.0001):
        self.curve = function_set[function_index]
        self.gradient = None
        if option == 0:
            self.gradient = derivative_set[function_index]
        self.x0, self.v0 = init_status
        self.y0 = self.curve(self.x0)
        self.xmin, self.xmax = x_range
        self.option = option
        self.friction = friction
        self.rollingball = None
        self.dt = dt
        
        self.pause = False
        self.stop = False
        
        # for physical simulation setting
        self.rollingball = RB.rollingball(curve=self.curve, 
                                          gradient=self.gradient, 
                                          init_status=(self.x0, self.y0, self.v0), 
                                          option=self.option,
                                          friction=self.friction)
        # for animation setting
        self.fig = plt.figure()
        self.x_range = np.linspace(self.xmin, self.xmax, 1000)
        self.y_range = self.curve(self.x_range)
        self.ymin = min(self.y_range)
        self.ymax = max(self.y_range)
        self.ax = self.fig.add_subplot(111, 
                                  autoscale_on=True,
                                  xlim=(self.xmin, self.xmax), 
                                  ylim=(self.ymin, self.ymax))
        self.ax.grid()
        self.lines = []
        self.lines.append(self.ax.plot([], [], lw=0.5)[0])
        self.lines.append(self.ax.plot([], [], 'o-', lw=2)[0])
        self.time_text = self.ax.text(0.02, 0.95, '', transform=self.ax.transAxes)
        self.velocity_text = self.ax.text(0.02, 0.90, '', transform=self.ax.transAxes)
        self.instruction_text = self.ax.text(0.02, 0.80, '', transform=self.ax.transAxes)
    
    def animation_init(self):
        # initialize animation
        self.lines[0].set_data([], [])
        self.lines[1].set_data([], [])
        self.time_text.set_text('')
        self.velocity_text.set_text('')
        self.instruction_text.set_text('')

        return self.lines, self.time_text, self.velocity_text, self.instruction_text
    
    
    def animate(self, i):
        self.lines[0].set_data(self.x_range, self.y_range)
        count = 0
        frames_rate = 100
        
        if self.stop:
            plt.close()
    
        while count < frames_rate and not self.pause:
            self.rollingball.step(self.dt)
            count += 1
        # check if ball is still in range
        x, y = self.rollingball.position()
        if x < self.xmin - 0.1 or x > self.xmax + 0.1 or y < self.ymin - 0.1 or y > self.ymax + 0.1:
            self.instruction_text.set_text('Out of range! Animation terminates.')
            self.pause = True
        self.lines[1].set_data(*self.rollingball.position())

        self.time_text.set_text('time = %.1f' % self.rollingball.time_elapsed)
        self.velocity_text.set_text('velocity = %.3f ' % self.rollingball.velocity())
        self.instruction_text.set_text('Click to pause and continue. Press Enter to stop.')
        
        return self.lines, self.time_text, self.velocity_text, self.instruction_text
    
    def run_animation(self):
        interval = 1000 * self.dt
        
        self.fig.canvas.mpl_connect('button_press_event', self.onClick)
        self.fig.canvas.mpl_connect('key_press_event', self.onKey)
        ani = animation.FuncAnimation(self.fig, 
                                      self.animate,
                                      frames=1000, 
                                      interval=interval, 
                                      init_func=self.animation_init)
        
        plt.show()
        
        
    def onClick(self, event):
        self.pause ^= True
    
    def onKey(self, event):
        self.stop ^= True
