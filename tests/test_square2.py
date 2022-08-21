import sys
import os

from numpy import Infinity
sys.path.append(os.getcwd())
import src.dudraw as dudraw

# open a 600x600 pixel canvas, and set the scale to one unit per pixel
dudraw.set_canvas_size(600,600)

dudraw.set_scale( 0, 600 )

dudraw.clear(dudraw.LIGHT_GRAY)

dudraw.set_pen_color( dudraw.BLACK )
dudraw.filled_square( 300, 300, 200 )

dudraw.set_pen_color( dudraw.CYAN )
dudraw.filled_circle( 300, 300, 200 )

dudraw.show( 100000 )