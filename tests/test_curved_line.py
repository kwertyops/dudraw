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
for i in range(1, 48):
    dudraw.line(i*10, math.sin(i/5)*50+250, (i+1)*10, math.sin((i+1)/5)*50+250)

dudraw.show(Infinity)