The rollingball.py file is for physical simulation, and the animation.ipynb file is for animation.

Our work should be in the rollingball.py file, spefically in the rollingball.slope function, where different ways of calculating gradients are implemented. I noted 'implement AD here' and 'implement numerical estimate here'.

To initialize a case, you should first define your own curve function, and if you are not going to use analytic gradient function, please set 'option' to be nonzero. Then, you should import the module first and initialize one as follows:
```
import rollingball as RB
r1 = RB.rollingball(curve=curve, gradient=gradient, init_status=(0.5, curve(0.5), option=0))
```
To update the position and velocity for certain times with proper time step and record your updates, you should do as follows:
```
dt = 0.0001
count = 0
x = []
y = []
v = []
while count < MAX:
    r1.step(dt)
    x.append(r1.x)
    y.append(r1.y)
    v.append(r1.velocity())
    count += 1
```

Note: you need to install FFmpeg to run animation.ipynb.
