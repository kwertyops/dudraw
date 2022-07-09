import sys
import os
sys.path.append(os.getcwd())
import src.dudraw as dudraw

dudraw.set_canvas_size(200, 200)

dudraw.set_x_scale(0, 400)
dudraw.set_y_scale(0, 400)

dudraw.line(0, 25, 400, 25)

dudraw.set_pen_width(1.0)
dudraw.line(0, 50, 400, 50)

dudraw.set_pen_width(20.0)
dudraw.line(0, 100, 400, 100)

dudraw.set_pen_width(40.0)
dudraw.line(0, 150, 400, 150)

dudraw.set_pen_width(100.0)
dudraw.line(0, 300, 400, 300)

dudraw.set_pen_width(20.0)
dudraw.ellipse(dudraw.get_canvas_width()/2, dudraw.get_canvas_height()/2, dudraw.get_canvas_width()/2, dudraw.get_canvas_height()/2)

dudraw.show(float("inf"))