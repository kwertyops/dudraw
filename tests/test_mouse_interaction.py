import sys
import os
import math
from numpy import Infinity
sys.path.append(os.getcwd())
import src.dudraw as dudraw

while True:
    dudraw.clear()
    if dudraw.mouse_is_pressed():
        dudraw.text(0.25, 0.25, "Mouse Is Pressed!")
    if dudraw.mouse_dragged():
        dudraw.text(0.75, 0.25, "Mouse Dragged!")
    if dudraw.mouse_clicked():
        dudraw.text(0.25, 0.75, "Mouse Clicked!")
    if dudraw.mouse_released():
        dudraw.text(0.75, 0.75, "Mouse Released!")

    dudraw.text(0.5, 0.5, f"{dudraw.mouse_x()}, {dudraw.mouse_y()}")
    dudraw.show(50)
