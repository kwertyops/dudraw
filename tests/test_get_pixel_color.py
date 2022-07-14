import sys
import os
sys.path.append(os.getcwd())
import src.dudraw as dudraw
import random

dudraw.set_canvas_size(900,521)
dudraw.set_x_scale(0,900)
dudraw.set_y_scale(0,521)
dudraw.picture("tests/carina_nebula.jpg")
count = 0
while True:
    y = random.randint(1, dudraw.get_canvas_height()-1)
    x = random.randint(1, dudraw.get_canvas_width()-1)
    color = dudraw.get_pixel_color(x,y)
    dudraw.set_pen_color(color)
    dudraw.filled_circle(x, y, 7)
    dudraw.show()
