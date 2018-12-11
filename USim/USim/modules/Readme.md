The rollingball.py file is for physical simulation, and the animation.py file is for animation.

Instructions:

We give an example of running animation.

To import the module and set up a new animation, you should do as follows:
```
import animation as Anim
anim = Anim.Animation(function_index=9, 
                      init_status=(0, 0), 
                      x_range=(0.1, 100), option=0, friction=0.2)
```
To run animation, you should do as follows:
```
anim.run_animation()
```

```function_index```: int, function index
```init_status```: tuple, initial status, (x0, v0)
```x_range```: tuple, range of x, (xmin, xmax)
```option```: int, choice of methods for gradient calculation, 0 for analytic one, 1 for AD, 2 for numerical one
```friction```: float, friction coefficient, from 0 to 1
