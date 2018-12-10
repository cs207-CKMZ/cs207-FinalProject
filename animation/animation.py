import rollingball as RB
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# for plots and animation
def curve(x):
    return (x - 2) ** 4

def gradient(x):
    return 4 * (x - 2) ** 3

import rollingball as RB
r1 = RB.rollingball(curve=curve, gradient=gradient, init_status=(0.5, curve(0.5), 0))

fig = plt.figure()
ax = fig.add_subplot(111, autoscale_on=True,
                     xlim=(0, 4), ylim=(0, 10))
ax.grid()

lines = []
lines.append(ax.plot([], [], lw=0.5)[0])
lines.append(ax.plot([], [], 'o-', lw=2)[0])
time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
velocity_text = ax.text(0.02, 0.90, '', transform=ax.transAxes)

def init():
    """initialize animation"""
    lines[0].set_data([], [])
    lines[1].set_data([], [])
    time_text.set_text('')
    velocity_text.set_text('')
    return lines, time_text, velocity_text

dt = 1 / 10000
def animate(i):
    """perform animation step"""
    global r1, dt

    x = np.linspace(0, 4, 10000)
    y = curve(x)
    lines[0].set_data(x, y)
    
    count = 0
    frames_rate = 100 # number of iterations per frame
    while count < frames_rate:
        r1.step(dt)
        count += 1
    lines[1].set_data( *r1.position())

    time_text.set_text('time = %.1f' % r1.time_elapsed)
    velocity_text.set_text('velocity = %.3f ' % r1.velocity())
    return lines, time_text, velocity_text

from time import time
t0 = time()
animate(0)
t1 = time()

interval = 1000 * dt - (t1 - t0)

ani = animation.FuncAnimation(fig, animate, frames=1000,
                              interval=interval, init_func=init)

# generate movie
ani.save('static.mp4', fps=100, writer='ffmpeg', extra_args=['-vcodec', 'libx264'])