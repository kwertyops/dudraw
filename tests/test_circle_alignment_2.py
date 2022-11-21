import sys
import os
import math

from numpy import Infinity
sys.path.append(os.getcwd())
import src.dudraw as dudraw
import random

dudraw.set_canvas_size(500,500)
# dudraw.clear(dudraw.BLACK)
dudraw.set_pen_color(dudraw.CYAN)
# dudraw.set_pen_width(0.005)
dudraw.set_pen_color(dudraw.CYAN)
dudraw.filled_circle(0.5, 0.5, 0.4)
dudraw.set_pen_color(dudraw.BLACK)
dudraw.circle(0.5, 0.5, 0.4)
for i in range(50):
    x = random.random()
    y = random.random()
    radius = random.random()*0.1
    dudraw.set_pen_color(dudraw.CYAN)
    dudraw.filled_circle(x, y, radius)
    dudraw.set_pen_color(dudraw.BLACK)
    dudraw.circle(x, y, radius)
dudraw.show(float('inf'))