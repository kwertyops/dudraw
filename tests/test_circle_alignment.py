import sys
import os
import math

from numpy import Infinity
sys.path.append(os.getcwd())
import src.dudraw as dudraw

dudraw.set_canvas_size(600, 600)
dudraw.clear(dudraw.BLACK)
dudraw.set_pen_color(dudraw.GRAY)
dudraw.set_pen_width(8.0 / 600)

# gray radial lines on a black background
for i in range(16):
    dudraw.line(
        0.5 + 0.1 * math.cos(i * math.pi / 8),
        0.5 + 0.1 * math.sin(i * math.pi / 8),
        0.5 + 2 * math.cos(i * math.pi / 8),
        0.5 + 2 * math.sin(i * math.pi / 8),
    )
for i in range(1, 7):
    dudraw.circle(0.5, 0.5, 0.1 * i)

dudraw.set_pen_color(dudraw.WHITE)

for i in range(1, 16):
    for j in range(2, 7):
        # white dots should just cover the intersection
        dudraw.filled_circle(
            0.5 + 0.1 * j * math.cos(i * math.pi / 8),
            0.5 + 0.1 * j * math.sin(i * math.pi / 8),
            8.0 / 600,
        )
# the innermost circle needs them spaced further apart
for i in range(1, 16, 2):
    # white dots should just cover the intersection
    dudraw.filled_circle(
        0.5 + 0.1 * math.cos(i * math.pi / 8),
        0.5 + 0.1 * math.sin(i * math.pi / 8),
        8.0 / 600,
    )

dudraw.show(float("inf"))