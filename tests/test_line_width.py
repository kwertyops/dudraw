import sys
import os
sys.path.append(os.getcwd())
import src.dudraw as dudraw

dudraw.set_canvas_size(200, 200)

dudraw.set_x_scale(0, 400)
dudraw.set_y_scale(0, 400)

dudraw.set_pen_radius(0.5)
dudraw.line(0, 50, 400, 50)

dudraw.set_pen_radius(10.0)
dudraw.line(0, 100, 400, 100)

dudraw.set_pen_radius(20.0)
dudraw.line(0, 150, 400, 150)

dudraw.set_pen_radius(50.0)
dudraw.line(0, 300, 400, 300)

dudraw.set_pen_radius(10.0)
dudraw.ellipse(dudraw.get_canvas_width()/2, dudraw.get_canvas_height()/2, dudraw.get_canvas_width()/2, dudraw.get_canvas_height()/2)

dudraw.show()