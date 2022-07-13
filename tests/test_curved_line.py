import sys
import os
import math
from numpy import Infinity
sys.path.append(os.getcwd())
import src.dudraw as dudraw

dudraw.set_canvas_size(500,500)
dudraw.set_x_scale(0,500)
dudraw.set_y_scale(0,500)
dudraw.clear(dudraw.BLACK)

dudraw.set_pen_color(dudraw.WHITE)
dudraw.set_pen_width(20)

points = []
for i in range(1, 200):
    points.append((i*2, math.sin(i/5)*50+250))
    
dudraw.polyline([p[0] for p in points], [p[1] for p in points])

dudraw.show(Infinity)