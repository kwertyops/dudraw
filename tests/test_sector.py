import sys
import os

from numpy import Infinity
sys.path.append(os.getcwd())
import src.dudraw as dudraw

dudraw.set_canvas_size(600,600)

dudraw.set_pen_width(0.10)
dudraw.sector(0.5, 0.5, 0.4, 180, 0)

dudraw.show(float('inf'))