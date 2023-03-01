import sys
import os
sys.path.append(os.getcwd())
import src.dudraw as dudraw

dudraw.set_font_size(24)
while True:
    dudraw.clear()
    keys_typed = dudraw.keys_typed()
    keys_released = dudraw.keys_released()
    if len(keys_typed) > 0:
        dudraw.text(0.25, 0.25, str(keys_typed))
    if len(keys_released) > 0:
        dudraw.text(0.75, 0.25, str(keys_released))
    if len(dudraw.keys_pressed()) > 0:
        dudraw.text(0.25, 0.75, str(dudraw.keys_pressed()))

    dudraw.show(50)