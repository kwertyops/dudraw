import sys
import os
import math
from numpy import Infinity
sys.path.append(os.getcwd())
import src.dudraw as dudraw

with open("tests/CO_elevations_feet.txt", "r") as file:
    elevations = []
    max = 0
    min = 15000
    for line in file:
        new_line = []
        values = line.split()
        for value in values:
            if int(value)> max:
                max = int(value)
            if int(value)<min:
                min = int(value)
            new_line.append(int(value))
        elevations.append(new_line)
    
dudraw.set_canvas_size(760,560)
dudraw.set_x_scale(0,760)
dudraw.set_y_scale(0,560)
for i in range(len(elevations)):
    for j in range(len(elevations[i])):
        intensity= int((elevations[i][j]-min)/(max-min)*255)
        dudraw.set_pen_color_rgb(intensity,intensity,intensity)
        dudraw.point(j,559-i)

while not dudraw.has_next_key_typed():
    if dudraw.mouse_pressed():
        dudraw.set_pen_color(dudraw.WHITE)
        dudraw.filled_rectangle(740,20,20,10)
        dudraw.set_pen_color(dudraw.BLACK)
        dudraw.text(740,20,str(elevations[int(560-dudraw.mouse_y())][int(dudraw.mouse_x())]))
    dudraw.show()