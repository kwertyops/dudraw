import sys
import os
import math
from numpy import Infinity
sys.path.append(os.getcwd())
import src.dudraw as dudraw

while True:
    dudraw.clear()
    if dudraw.mouse_pressed():
        dudraw.text(0.25, 0.25, "Mouse Pressed!")
    if dudraw.mouse_dragged():
        dudraw.text(0.75, 0.25, "Mouse Dragged!")
    if dudraw.mouse_clicked():
        dudraw.text(0.25, 0.75, "Mouse Clicked!")

    dudraw.text(0.5, 0.5, f"{dudraw.mouse_x()}, {dudraw.mouse_y()}")
    dudraw.show(50)
