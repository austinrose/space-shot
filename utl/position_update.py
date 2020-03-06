import math
import numpy as np

# finds new position in SEZ coordinate system
# inputs: F: 1x3 np mat, m: float, x0: 1x3 np mat, v0: 1x3 np mat, dt: float
def newton(F, m, x0, v0, dt):
    a = F / m
    v = v0 + a * dt
    x = x0 + v0 * dt + 0.5 * a * dt**2

    return x, v
