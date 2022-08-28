import sys
import os

from numpy import Infinity
sys.path.append(os.getcwd())
import src.dudraw as dudraw

dudraw.set_canvas_size(400, 400)
dudraw.set_x_scale(0,10)
dudraw.set_y_scale(0,10)
dudraw.set_pen_width(0.0)

dudraw.polygon([0, 1.0, 0.5], [0.6, 0.6, 1.0])

dudraw.show(Infinity)