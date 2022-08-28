import sys
import os

from numpy import Infinity
sys.path.append(os.getcwd())
import src.dudraw as dudraw

dudraw.set_canvas_size(600, 600)
NUMBER_OF_LINES = 8
dudraw.clear(dudraw.BLACK)
dudraw.set_pen_width(1 / 301)
dudraw.set_pen_color(dudraw.LIGHT_GRAY)
for i in range(NUMBER_OF_LINES):
    dudraw.line(i * 1 / 8, 0, i * 1 / 8, 1)
    dudraw.line(0, i * 1 / 8, 1, i * 1 / 8)
dudraw.show(float("inf"))