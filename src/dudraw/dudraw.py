"""
dudraw.py

The dudraw module defines functions that allow the user to create a
drawing.  A drawing appears on the canvas.  The canvas appears
in the window.  As a convenience, the module also imports the
commonly used Color objects defined in the color module.
"""

import time
import os
import sys
import math
from typing import Sequence

from .color import *

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
import pygame.gfxdraw
import pygame.font

# -----------------------------------------------------------------------

# Default Sizes and Values

_BORDER = 0.0
# _BORDER = 0.05
_DEFAULT_XMIN = 0.0
_DEFAULT_XMAX = 1.0
_DEFAULT_YMIN = 0.0
_DEFAULT_YMAX = 1.0
_DEFAULT_CANVAS_SIZE = 512
_DEFAULT_PEN_WIDTH = 0.0  # should correspond to a width of 1 pixel on the canvas.
_DEFAULT_PEN_COLOR = BLACK

_DEFAULT_FONT_FAMILY = "Helvetica"
_DEFAULT_FONT_SIZE = 12

_xmin = None
_ymin = None
_xmax = None
_ymax = None

_font_family = _DEFAULT_FONT_FAMILY
_font_size = _DEFAULT_FONT_SIZE

_canvas_width = float(_DEFAULT_CANVAS_SIZE)
_canvas_height = float(_DEFAULT_CANVAS_SIZE)
_pen_width = None
_pen_color = _DEFAULT_PEN_COLOR
_keys_typed = []

# Has the window been created?
_window_created = False

# -----------------------------------------------------------------------
# Begin added by Alan J. Broder
# -----------------------------------------------------------------------

# Keep track of mouse status

# Has the mouse been left-clicked since the last time we checked?
_mouse_pressed = False

# The position of the mouse as of the most recent mouse click
_mouse_pos = None


# -----------------------------------------------------------------------
# End added by Alan J. Broder
# -----------------------------------------------------------------------

# -----------------------------------------------------------------------


def _pygame_color(c: Color) -> pygame.Color:
    """
    Convert c, an object of type Color, to an equivalent object
    of type pygame.Color.  Return the result.
    """
    r = c.get_red()
    g = c.get_green()
    b = c.get_blue()
    return pygame.Color(r, g, b)


# -----------------------------------------------------------------------

# Private functions to scale and factor X and Y values.


def _scale_x(x: float) -> float:
    return _canvas_width * (x - _xmin) / (_xmax - _xmin)


def _scale_y(y: float) -> float:
    return _canvas_height * (_ymax - y) / (_ymax - _ymin)


def _factor_x(w: float) -> float:
    return w * _canvas_width / abs(_xmax - _xmin)


def _factor_y(h: float) -> float:
    return h * _canvas_height / abs(_ymax - _ymin)


# -----------------------------------------------------------------------
# Begin added by Alan J. Broder
# -----------------------------------------------------------------------


def _user_x(x: float) -> float:
    return _xmin + x * (_xmax - _xmin) / _canvas_width


def _user_y(y: float) -> float:
    return _ymax - y * (_ymax - _ymin) / _canvas_height


def _pen_width_pixels() -> float:
    return min(_factor_x(_pen_width), _factor_y(_pen_width))


def _line_width_pixels() -> float:
    return max(_pen_width_pixels(), 1.0)


# -----------------------------------------------------------------------
# End added by Alan J. Broder
# -----------------------------------------------------------------------

# -----------------------------------------------------------------------


def set_canvas_size(w: float = _DEFAULT_CANVAS_SIZE, h: float = _DEFAULT_CANVAS_SIZE):
    """
    Set the size of the canvas to w pixels wide and h pixels high.
    Calling this function is optional. If you call it, you must do
    so before calling any drawing function.
    """
    global _background
    global _surface
    global _canvas_width
    global _canvas_height
    global _window_created

    if _window_created:
        raise Exception("The dudraw window already was created")

    if (w < 1) or (h < 1):
        raise Exception("width and height must be positive")

    _canvas_width = w
    _canvas_height = h
    _background = pygame.display.set_mode([w, h])
    pygame.display.set_caption("")
    _surface = pygame.Surface((w, h))
    _surface.fill(_pygame_color(WHITE))
    _window_created = True


def get_canvas_width() -> float:
    """
    Return the width of the current canvas
    """
    return abs(_xmax - _xmin)


def get_canvas_height() -> float:
    """
    Return the height of the current canvas
    """
    return abs(_ymax - _ymin)


def get_pixel_color(x: float, y: float) -> pygame.Color:
    """
    Return the color of the pixel at the given user coordinates
    """
    _make_sure_window_created()
    return _surface.get_at((int(_scale_x(x)), int(_scale_y(y))))


def set_x_scale(min: float = _DEFAULT_XMIN, max: float = _DEFAULT_XMAX):
    """
    Set the x-scale of the canvas such that the minimum x value
    is min and the maximum x value is max.
    """
    global _xmin
    global _xmax
    min = float(min)
    max = float(max)
    if min >= max:
        raise Exception("min must be less than max")
    size = max - min
    _xmin = min - _BORDER * size
    _xmax = max + _BORDER * size


def set_y_scale(min: float = _DEFAULT_YMIN, max: float = _DEFAULT_YMAX):
    """
    Set the y-scale of the canvas such that the minimum y value
    is min and the maximum y value is max.
    """
    global _ymin
    global _ymax
    min = float(min)
    max = float(max)
    if min >= max:
        raise Exception("min must be less than max")
    size = max - min
    _ymin = min - _BORDER * size
    _ymax = max + _BORDER * size


def set_scale():
    set_x_scale()
    set_y_scale()


def set_scale(min: float, max: float):
    set_x_scale(min, max)
    set_y_scale(min, max)


def set_pen_width(w: float = _DEFAULT_PEN_WIDTH):
    """
    Set the pen radius to r, thus affecting the subsequent drawing
    of points and lines. If r is 0.0, then points will be drawn with
    the minimum possible radius and lines with the minimum possible
    width.
    """
    global _pen_width
    w = float(w)
    if w < 0.0:
        raise Exception("Argument to set_pen_width() must be non-neg")
    # _penRadius = r * float(_DEFAULT_CANVAS_SIZE)
    _pen_width = w


def set_pen_color(c: Color = _DEFAULT_PEN_COLOR):
    """
    Set the pen color to c, where c is an object of class Color.
    c defaults to dudraw.BLACK.
    """
    global _pen_color
    _pen_color = c


def set_pen_color_rgb(r: int = 255, g: int = 255, b: int = 255):
    """
    Set the pen color to c, where c is an object of class Color.
    c defaults to dudraw.BLACK.
    """
    c = Color(r, g, b)
    global _pen_color
    _pen_color = c


def get_pen_color():
    """
    Returns the value of _penColor as an object of class Color.
    """
    return _pen_color


def set_font_family(f: str = _DEFAULT_FONT_FAMILY):
    """
    Set the font family to f (e.g. 'Helvetica' or 'Courier').
    """
    global _font_family
    _font_family = f


def set_font_size(s: int = _DEFAULT_FONT_SIZE):
    """
    Set the font size to s (e.g. 12 or 16).
    """
    global _font_size
    _font_size = s


# -----------------------------------------------------------------------


def _make_sure_window_created():
    global _window_created
    if not _window_created:
        set_canvas_size()
        _window_created = True


# -----------------------------------------------------------------------

# Functions to draw shapes, text, and images on the background canvas.


def _pixel(x: float, y: float):
    """
    Draw on the background canvas a pixel at (x, y).
    """
    _make_sure_window_created()
    xs = _scale_x(x)
    xy = _scale_y(y)
    pygame.gfxdraw.pixel(_surface, int(round(xs)), int(round(xy)), _pygame_color(_pen_color))


def point(x: float, y: float):
    """
    Draw on the background canvas a point at (x, y).
    """
    _make_sure_window_created()
    x = float(x)
    y = float(y)
    line_width = _line_width_pixels()
    if line_width < 2.0:
        # If the point is going to be 1 pixel wide, just draw a pixel.
        _pixel(x, y)
    else:
        xs = _scale_x(x)
        ys = _scale_y(y)
        pygame.draw.ellipse(
            _surface,
            _pygame_color(_pen_color),
            pygame.Rect(xs - line_width / 2, ys - line_width / 2, line_width, line_width),
            0,
        )


def _thick_line(x0: float, y0: float, x1: float, y1: float, r: float):
    """
    Draw on the background canvas a line from (x0, y0) to (x1, y1).
    Draw the line with a pen whose radius is r.
    """
    xs0 = _scale_x(x0)
    ys0 = _scale_y(y0)
    xs1 = _scale_x(x1)
    ys1 = _scale_y(y1)
    if (abs(xs0 - xs1) < 1.0) and (abs(ys0 - ys1) < 1.0):
        filled_circle(x0, y0, r)
        return
    x_mid = (x0 + x1) / 2
    y_mid = (y0 + y1) / 2
    _thick_line(x0, y0, x_mid, y_mid, r)
    _thick_line(x_mid, y_mid, x1, y1, r)


def line(x0: float, y0: float, x1: float, y1: float):
    """
    Draw on the background canvas a line from (x0, y0) to (x1, y1).
    """
    _make_sure_window_created()
    x0 = float(x0)
    y0 = float(y0)
    x1 = float(x1)
    y1 = float(y1)
    line_width = _line_width_pixels()

    if line_width < 2.0:
        x0s = _scale_x(x0)
        y0s = _scale_y(y0)
        x1s = _scale_x(x1)
        y1s = _scale_y(y1)
        pygame.draw.line(_surface, _pygame_color(_pen_color), (x0s, y0s), (x1s, y1s), int(line_width))
    else:
        vec = pygame.Vector2(x1 - x0, y1 - y0)
        w = vec.rotate(90).normalize()
        w.scale_to_length(line_width/2.0)
        xs = [x0 + w.x, x0 - w.x, x1 - w.x, x1 + w.x,]
        ys = [y0 + w.y, y0 - w.y, y1 - w.y, y1 + w.y,]
        filled_polygon(xs, ys)


def circle(x: float, y: float, r: float):
    """
    Draw on the background canvas a circle of radius r centered on
    (x, y).
    """
    _make_sure_window_created()
    x = float(x)
    y = float(y)
    r = float(r)
    ws = _factor_x(2.0 * r)
    hs = _factor_y(2.0 * r)
    line_width = _line_width_pixels()
    if (ws <= 1.0) and (hs <= 1.0):
        # If the radius is too small, then simply draw a pixel.
        _pixel(x, y)
    else:
        xs = _scale_x(x)
        ys = _scale_y(y)
        pygame.draw.ellipse(
            _surface,
            _pygame_color(_pen_color),
            pygame.Rect(xs - ws / 2.0, ys - hs / 2.0, ws, hs),
            int(round(line_width)),
        )


def filled_circle(x: float, y: float, r: float):
    """
    Draw on the background canvas a filled circle of radius r
    centered on (x, y).
    """
    _make_sure_window_created()
    x = float(x)
    y = float(y)
    r = float(r)
    ws = _factor_x(2.0 * r)
    hs = _factor_y(2.0 * r)
    # If the radius is too small, then simply draw a pixel.
    if (ws <= 1.0) and (hs <= 1.0):
        _pixel(x, y)
    else:
        xs = _scale_x(x)
        ys = _scale_y(y)
        pygame.draw.ellipse(_surface, _pygame_color(_pen_color), pygame.Rect(xs - ws / 2.0, ys - hs / 2.0, ws, hs), 0)


def ellipse(x: float, y: float, half_width: float, half_height: float):
    """
    Draw on the background canvas an ellipse centered at (x, y) with
    a width of 2.0 * half_width, and a height of 2.0 * half_height.
    """
    _make_sure_window_created()
    x = float(x)
    y = float(y)
    half_width = float(half_width)
    half_height = float(half_height)
    ws = _factor_x(2.0 * half_width)
    hs = _factor_y(2.0 * half_height)
    line_width = _line_width_pixels()
    if (ws <= 1.0) and (hs <= 1.0):
        # If the radius is too small, then simply draw a pixel.
        _pixel(x, y)
    else:
        xs = _scale_x(x)
        ys = _scale_y(y)
        pygame.draw.ellipse(
            _surface,
            _pygame_color(_pen_color),
            pygame.Rect(xs - ws / 2.0, ys - hs / 2.0, ws, hs),
            int(round(line_width)),
        )


def filled_ellipse(x: float, y: float, half_width: float, half_height: float):
    """
    Draw on the background canvas a filled ellipse centered at (x, y)
    with a width of 2.0 * half_width, and a height of 2.0 * half_height.
    """
    _make_sure_window_created()
    x = float(x)
    y = float(y)
    half_width = float(half_width)
    half_height = float(half_height)
    ws = _factor_x(2.0 * half_width)
    hs = _factor_y(2.0 * half_height)
    if (ws <= 1.0) and (hs <= 1.0):
        # If the radius is too small, then simply draw a pixel.
        _pixel(x, y)
    else:
        xs = _scale_x(x)
        ys = _scale_y(y)
        pygame.draw.ellipse(_surface, _pygame_color(_pen_color), pygame.Rect(xs - ws / 2.0, ys - hs / 2.0, ws, hs), 0)


def rectangle(x: float, y: float, half_width: float, half_height: float):
    """
    Draw on the background canvas a rectangle of width (2 * halfWidth
    and height (2 * halfHeight) centered at point (x, y).
    """
    global _surface
    _make_sure_window_created()
    x = float(x) - float(half_width)
    y = float(y) - float(half_height)
    half_width = 2 * float(half_width)
    half_height = 2 * float(half_height)
    ws = _factor_x(half_width)
    hs = _factor_y(half_height)
    line_width = _line_width_pixels()
    if (ws <= 1.0) and (hs <= 1.0):
        # If the rectangle is too small, then simply draw a pixel.
        _pixel(x, y)
    else:
        xs = _scale_x(x)
        ys = _scale_y(y)
        pygame.draw.rect(_surface, _pygame_color(_pen_color), pygame.Rect(xs, ys - hs, ws, hs), int(round(line_width)))


def filled_rectangle(x: float, y: float, half_width: float, half_height: float):
    """
    Draw on the background canvas a rectangle of width (2 * halfWidth
    and height (2 * halfHeight) centered at point (x, y).
    """
    global _surface
    _make_sure_window_created()
    x = float(x) - float(half_width)
    y = float(y) - float(half_height)
    w = 2 * float(half_width)
    h = 2 * float(half_height)
    ws = _factor_x(w)
    hs = _factor_y(h)
    # If the rectangle is too small, then simply draw a pixel.
    if (ws <= 1.0) and (hs <= 1.0):
        _pixel(x, y)
    else:
        xs = _scale_x(x)
        ys = _scale_y(y)
        pygame.draw.rect(_surface, _pygame_color(_pen_color), pygame.Rect(xs, ys - hs, ws, hs), 0)


def square(x: float, y: float, r: float):
    """
    Draw on the background canvas a square whose sides are of length
    2r, centered on (x, y).
    """
    _make_sure_window_created()
    rectangle(x - r, y - r, 2.0 * r, 2.0 * r)


def filled_square(x: float, y: float, r: float):
    """
    Draw on the background canvas a filled square whose sides are of
    length 2r, centered on (x, y).
    """
    _make_sure_window_created()
    filled_rectangle(x - r, y - r, 2.0 * r, 2.0 * r)


def polygon(x: Sequence[float], y: Sequence[float]):
    """
    Draw on the background canvas a polygon with coordinates
    (x[i], y[i]).
    """
    global _surface
    _make_sure_window_created()
    line_width = _line_width_pixels()
    # Scale X and Y values.
    x_scaled = []
    for xi in x:
        x_scaled.append(_scale_x(float(xi)))
    y_scaled = []
    for yi in y:
        y_scaled.append(_scale_y(float(yi)))
    points = []
    for i in range(len(x)):
        points.append((x_scaled[i], y_scaled[i]))
    points.append((x_scaled[0], y_scaled[0]))
    pygame.draw.polygon(_surface, _pygame_color(_pen_color), points, int(round(line_width)))


def filled_polygon(x: Sequence[float], y: Sequence[float]):
    """
    Draw on the background canvas a filled polygon with coordinates
    (x[i], y[i]).
    """
    global _surface
    _make_sure_window_created()
    # Scale X and Y values.
    x_scaled = []
    for xi in x:
        x_scaled.append(_scale_x(float(xi)))
    y_scaled = []
    for yi in y:
        y_scaled.append(_scale_y(float(yi)))
    points = []
    for i in range(len(x)):
        points.append((x_scaled[i], y_scaled[i]))
    points.append((x_scaled[0], y_scaled[0]))
    pygame.draw.polygon(_surface, _pygame_color(_pen_color), points, 0)


def triangle(x0: float, y0: float, x1: float, y1: float, x2: float, y2: float):
    """
    Draw a triangle on the canvas with corners at (x0, y0),
    (x1, y1), and (x2, y2).
    """
    _make_sure_window_created()
    polygon([x0, x1, x2], [y0, y1, y2])


def filled_triangle(x0: float, y0: float, x1: float, y1: float, x2: float, y2: float):
    """
    Draw a filled triangle on the canvas with corners at
    (x0, y0), (x1, y1), and (x2, y2).
    """
    _make_sure_window_created()
    filled_polygon([x0, x1, x2], [y0, y1, y2])


def quadrilateral(x0: float, y0: float, x1: float, y1: float, x2: float, y2: float, x3: float, y3: float):
    """
    Draw a quadrilateral on the canvas with corners at (x0, y0),
    (x1, y1), (x2, y2), and (x3, y3).
    """
    _make_sure_window_created()
    polygon([x0, x1, x2, x3], [y0, y1, y2, y3])


def filled_quadrilateral(x0: float, y0: float, x1: float, y1: float, x2: float, y2: float, x3: float, y3: float):
    """
    Draw a filled quadrilateral on the canvas with corners at
    (x0, y0), (x1, y1), (x2, y2), and (x3, y3).
    """
    _make_sure_window_created()
    filled_polygon([x0, x1, x2, x3], [y0, y1, y2, y3])


def arc(x: float, y: float, r: float, angle1: float, angle2: float):
    """
    Draw an arc portion between angle1 and angle2, of the
    circumference of a circle centered at (x, y) with a radius r.
    """
    _make_sure_window_created()
    x = float(x)
    y = float(y)
    r = float(r)
    angle1 = float(angle1)
    angle2 = float(angle2)
    while (angle2 - angle1) < 0:
        angle2 += 360
    circle_points = 4 * (_factor_x(r) + _factor_y(r))
    num_points = circle_points * ((angle2 - angle1) / 360)
    for i in range(0, int(num_points)):
        angle_in = angle1 + (i * 360 / circle_points)
        angle_in = angle_in * math.pi / 180
        x0 = (math.cos(angle_in) * r) + x
        y0 = (math.sin(angle_in) * r) + y
        angle_out = angle1 + ((i + 1) * 360 / circle_points)
        angle_out = angle_out * math.pi / 180
        x1 = (math.cos(angle_out) * r) + x
        y1 = (math.sin(angle_out) * r) + y
        line(x0, y0, x1, y1)


def elliptical_arc(x: float, y: float, half_width: float, half_height: float, angle1: float, angle2: float):
    """
    Draw an arc portion between angle1 and angle2, of the
    circumference of an ellipse centered at (x, y) with a width
    of half_width, and a height of 2.0 * half_height.
    """
    _make_sure_window_created()
    x = float(x)
    y = float(y)
    half_width = float(half_width)
    half_height = float(half_height)
    angle1 = float(angle1)
    angle2 = float(angle2)
    while (angle2 - angle1) < 0:
        angle2 += 360
    circle_points = 4 * (_factor_x(half_width) + _factor_y(half_height))
    num_points = circle_points * ((angle2 - angle1) / 360)
    for i in range(0, int(num_points)):
        angle_in = angle1 + (i * 360 / circle_points)
        angle_in = angle_in * math.pi / 180
        x0 = (math.cos(angle_in) * half_width) + x
        y0 = (math.sin(angle_in) * half_height) + y
        angle_out = angle1 + ((i + 1) * 360 / circle_points)
        angle_out = angle_out * math.pi / 180
        x1 = (math.cos(angle_out) * half_width) + x
        y1 = (math.sin(angle_out) * half_height) + y
        line(x0, y0, x1, y1)


def sector(x: float, y: float, r: float, angle1: float, angle2: float):
    """
    Draw a sector portion between angle1 and angle2, of the
    interior of a circle centered at (x, y) with a radius r.
    """
    global _surface
    _make_sure_window_created()
    x = float(x)
    y = float(y)
    r = float(r)
    line_width = _line_width_pixels()
    angle1 = float(angle1)
    angle2 = float(angle2)
    while (angle2 - angle1) < 0:
        angle2 += 360
    circle_points = 4 * (_factor_x(r) + _factor_y(r))
    num_points = circle_points * ((angle2 - angle1) / 360)
    xvals = [x]
    yvals = [y]
    for i in range(0, int(num_points) + 1):
        angle = angle1 + (i * 360 / circle_points)
        angle = angle * math.pi / 180
        x0 = (math.cos(angle) * r) + x
        y0 = (math.sin(angle) * r) + y
        xvals.append(x0)
        yvals.append(y0)
    xvals.append((math.cos(angle2 * math.pi / 180) * r) + x)
    yvals.append((math.sin(angle2 * math.pi / 180) * r) + y)
    xvals.append(x)
    yvals.append(y)
    points = []
    for i in range(1, len(xvals)):
        line(xvals[i-1], yvals[i-1], xvals[i], yvals[i])


def filled_sector(x: float, y: float, r: float, angle1: float, angle2: float):
    """
    Draw a filled sector portion between angle1 and angle2, of the
    interior of a circle centered at (x, y) with a radius r.
    """
    global _surface
    _make_sure_window_created()
    x = float(x)
    y = float(y)
    r = float(r)
    angle1 = float(angle1)
    angle2 = float(angle2)
    while (angle2 - angle1) < 0:
        angle2 += 360
    circle_points = 4 * (_factor_x(r) + _factor_y(r))
    num_points = circle_points * ((angle2 - angle1) / 360)
    xvals = [x]
    yvals = [y]
    for i in range(0, int(num_points) + 1):
        angle = angle1 + (i * 360 / circle_points)
        angle = angle * math.pi / 180
        x0 = (math.cos(angle) * r) + x
        y0 = (math.sin(angle) * r) + y
        xvals.append(x0)
        yvals.append(y0)
    xvals.append((math.cos(angle2 * math.pi / 180) * r) + x)
    yvals.append((math.sin(angle2 * math.pi / 180) * r) + y)
    xvals.append(x)
    yvals.append(y)
    points = []
    for i in range(len(xvals)):
        points.append((_scale_x(xvals[i]), _scale_y(yvals[i])))
    pygame.draw.polygon(_surface, _pygame_color(_pen_color), points, 0)


def elliptical_sector(x: float, y: float, half_width: float, half_height: float, angle1: float, angle2: float):
    """
    Draw a sector portion between angle1 and angle2, of the
    interior of an ellipse centered at (x, y) with a width
    of half_width, and a height of 2.0 * half_height.
    """
    global _surface
    _make_sure_window_created()
    x = float(x)
    y = float(y)
    half_width = float(half_width)
    half_height = float(half_height)
    line_width = _line_width_pixels()
    angle1 = float(angle1)
    angle2 = float(angle2)
    while (angle2 - angle1) < 0:
        angle2 += 360
    circle_points = 4 * (_factor_x(half_width) + _factor_y(half_height))
    num_points = circle_points * ((angle2 - angle1) / 360)
    xvals = [x]
    yvals = [y]
    for i in range(0, int(num_points) + 1):
        angle = angle1 + (i * 360 / circle_points)
        angle = angle * math.pi / 180
        x0 = (math.cos(angle) * half_width) + x
        y0 = (math.sin(angle) * half_height) + y
        xvals.append(x0)
        yvals.append(y0)
    xvals.append((math.cos(angle2 * math.pi / 180) * half_width) + x)
    yvals.append((math.sin(angle2 * math.pi / 180) * half_height) + y)
    xvals.append(x)
    yvals.append(y)
    points = []
    for i in range(len(xvals)):
        points.append((_scale_x(xvals[i]), _scale_y(yvals[i])))
    pygame.draw.polygon(_surface, _pygame_color(_pen_color), points, int(round(line_width)))


def filled_elliptical_sector(
    x: float, y: float, half_width: float, half_height: float, angle1: float, angle2: float
):
    """
    Draw a filled sector portion between angle1 and angle2, of
    the interior of an ellipse centered at (x, y) with a width
    of half_width, and a height of 2.0 * half_height.
    """
    global _surface
    _make_sure_window_created()
    x = float(x)
    y = float(y)
    half_width = float(half_width)
    half_height = float(half_height)
    angle1 = float(angle1)
    angle2 = float(angle2)
    while (angle2 - angle1) < 0:
        angle2 += 360
    circle_points = 4 * (_factor_x(half_width) + _factor_y(half_height))
    num_points = circle_points * ((angle2 - angle1) / 360)
    xvals = [x]
    yvals = [y]
    for i in range(0, int(num_points) + 1):
        angle = angle1 + (i * 360 / circle_points)
        angle = angle * math.pi / 180
        x0 = (math.cos(angle) * half_width) + x
        y0 = (math.sin(angle) * half_height) + y
        xvals.append(x0)
        yvals.append(y0)
    xvals.append((math.cos(angle2 * math.pi / 180) * half_width) + x)
    yvals.append((math.sin(angle2 * math.pi / 180) * half_height) + y)
    xvals.append(x)
    yvals.append(y)
    points = []
    for i in range(len(xvals)):
        points.append((_scale_x(xvals[i]), _scale_y(yvals[i])))
    pygame.draw.polygon(_surface, _pygame_color(_pen_color), points, 0)


def annulus(x: float, y: float, r1: float, r2: float):
    """
    Draw an annulus centered at (x, y) with outer
    radius r1, and inner radius r2.
    """
    _make_sure_window_created()
    circle(x, y, r1)
    circle(x, y, r2)


def filled_annulus(x: float, y: float, r1: float, r2: float):
    """
    Draw a filled annulus centered at (x, y) with outer
    radius r1, and inner radius r2.
    """
    global _surface
    _make_sure_window_created()
    x = float(x)
    y = float(y)
    r1 = float(r1)
    r2 = float(r2)
    circle1_points = 4 * (_factor_x(r1) + _factor_y(r1))
    circle2_points = 4 * (_factor_x(r2) + _factor_y(r2))
    xvals = []
    yvals = []
    for i in range(0, int(circle1_points) + 1):
        angle = i * 360 / circle1_points
        angle = angle * math.pi / 180
        x0 = (math.cos(angle) * r1) + x
        y0 = (math.sin(angle) * r1) + y
        xvals.append(x0)
        yvals.append(y0)
    xvals.append(x + r1)
    yvals.append(y)
    xvals.append(x + r2)
    yvals.append(y)
    for i in range(int(circle2_points), -1, -1):
        angle = i * 360 / circle2_points
        angle = angle * math.pi / 180
        x0 = (math.cos(angle) * r2) + x
        y0 = (math.sin(angle) * r2) + y
        xvals.append(x0)
        yvals.append(y0)
    xvals.append(x + r2)
    yvals.append(y)
    xvals.append(x + r1)
    yvals.append(y)
    points = []
    for i in range(len(xvals)):
        points.append((_scale_x(xvals[i]), _scale_y(yvals[i])))
    pygame.draw.polygon(_surface, _pygame_color(_pen_color), points, 0)


def text(x: float, y: float, s: str):
    """
    Draw string s on the background canvas centered at (x, y).
    """
    _make_sure_window_created()
    x = float(x)
    y = float(y)
    xs = _scale_x(x)
    ys = _scale_y(y)
    font = pygame.font.SysFont(_font_family, _font_size)
    text = font.render(s, 1, _pygame_color(_pen_color))
    textpos = text.get_rect(center=(xs, ys))
    _surface.blit(text, textpos)


def picture(pic_path: str, x: float = None, y: float = None):
    """
    Draw pic on the background canvas centered at (x, y).  pic is an
    object of class picture.Picture. x and y default to the midpoint
    of the background canvas.
    """
    global _surface
    _make_sure_window_created()
    # By default, draw pic at the middle of the surface.
    if x is None:
        x = (_xmax + _xmin) / 2.0
    if y is None:
        y = (_ymax + _ymin) / 2.0
    x = float(x)
    y = float(y)
    xs = _scale_x(x)
    ys = _scale_y(y)
    pic = pygame.image.load(pic_path)
    ws = pic.get_width()
    hs = pic.get_height()
    _surface.blit(pic, [xs - ws / 2.0, ys - hs / 2.0, ws, hs])


def clear(c: Color = WHITE):
    """
    Clear the background canvas to color c, where c is an
    object of class Color. c defaults to dudraw.WHITE.
    """
    _make_sure_window_created()
    _surface.fill(_pygame_color(c))


def clear_rgb(r: float = 255, g: float = 255, b: float = 255):
    """
    Clear the background canvas to color c, where c is an
    object of class Color. c defaults to dudraw.WHITE.
    """
    c = Color(r, g, b)
    _make_sure_window_created()
    _surface.fill(_pygame_color(c))


def save(f: str):
    """
    Save the window canvas to file f.
    """
    _make_sure_window_created()
    if f.split(".")[-1].lower() != "jpg":
        f += ".jpg"
    pygame.image.save(_surface, f)


# -----------------------------------------------------------------------


def _show():
    """
    Copy the background canvas to the window canvas.
    """
    _background.blit(_surface, (0, 0))
    pygame.display.flip()
    _check_for_events()


def _show_and_wait_forever():
    """
    Copy the background canvas to the window canvas. Then wait
    forever, that is, until the user closes the dudraw window.
    """
    _make_sure_window_created()
    _show()
    QUANTUM = 0.1
    while True:
        time.sleep(QUANTUM)
        _check_for_events()


def show(msec: float = 0.0):
    """
    Copy the background canvas to the window canvas, and
    then wait for msec milliseconds. msec defaults to infinity.
    """
    if msec == float("inf"):
        _show_and_wait_forever()

    _make_sure_window_created()
    _show()
    _check_for_events()

    # Sleep for the required time, but check for events every
    # QUANTUM seconds.
    QUANTUM = 0.1
    sec = msec / 1000.0
    if sec < QUANTUM:
        time.sleep(sec)
        return
    seconds_waited = 0.0
    while seconds_waited < sec:
        time.sleep(QUANTUM)
        seconds_waited += QUANTUM
        _check_for_events()


# -----------------------------------------------------------------------


def _check_for_events():
    """
    Check if any new event has occured (such as a key typed or button
    pressed).  If a key has been typed, then put that key in a queue.
    """
    global _surface
    global _keys_typed

    # -------------------------------------------------------------------
    # Begin added by Alan J. Broder
    # -------------------------------------------------------------------
    global _mouse_pos
    global _mouse_pressed
    # -------------------------------------------------------------------
    # End added by Alan J. Broder
    # -------------------------------------------------------------------

    _make_sure_window_created()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            _keys_typed = [event.unicode] + _keys_typed
        # elif (event.type == pygame.MOUSEBUTTONUP) and \
        #         (event.button == 3):
        #     _save_to_file()

        # ---------------------------------------------------------------
        # Begin added by Alan J. Broder
        # ---------------------------------------------------------------
        # Every time the mouse button is pressed, remember
        # the mouse position as of that press.
        elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):
            _mouse_pressed = True
            _mouse_pos = event.pos
            # ---------------------------------------------------------------
        # End added by Alan J. Broder
        # ---------------------------------------------------------------


# -----------------------------------------------------------------------

# Functions for retrieving keys


def has_next_key_typed() -> bool:
    """
    Return True if the queue of keys the user typed is not empty.
    Otherwise return False.
    """
    global _keys_typed
    return _keys_typed != []


def next_key_typed() -> str:
    """
    Remove the first key from the queue of keys that the the user typed,
    and return that key.
    """
    global _keys_typed
    return _keys_typed.pop()


# -----------------------------------------------------------------------
# Begin added by Alan J. Broder
# -----------------------------------------------------------------------

# Functions for dealing with mouse clicks


def mouse_pressed() -> bool:
    """
    Return True if the mouse has been left-clicked since the
    last time mousePressed was called, and False otherwise.
    """
    global _mouse_pressed
    if _mouse_pressed:
        _mouse_pressed = False
        return True
    return False


def mouse_x() -> float:
    """
    Return the x coordinate in user space of the location at
    which the mouse was most recently left-clicked. If a left-click
    hasn't happened yet, raise an exception, since mouseX() shouldn't
    be called until mousePressed() returns True.
    """
    global _mouse_pos
    if _mouse_pos:
        return _user_x(_mouse_pos[0])
    raise Exception("Can't determine mouse position if a click hasn't happened")


def mouse_y() -> float:
    """
    Return the y coordinate in user space of the location at
    which the mouse was most recently left-clicked. If a left-click
    hasn't happened yet, raise an exception, since mouseY() shouldn't
    be called until mousePressed() returns True.
    """
    global _mouse_pos
    if _mouse_pos:
        return _user_y(_mouse_pos[1])
    raise Exception("Can't determine mouse position if a click hasn't happened")


# -----------------------------------------------------------------------
# End added by Alan J. Broder
# -----------------------------------------------------------------------

# -----------------------------------------------------------------------

# Initialize the x scale, the y scale, and the pen radius.

set_x_scale()
set_y_scale()
set_pen_width()
pygame.font.init()


# -----------------------------------------------------------------------


def _regression_test():
    """
    Perform regression testing.
    """

    clear()

    print(_canvas_width, ", ", _canvas_height)

    set_pen_color(MAGENTA)
    set_pen_width(1)
    line(0.47, 0.25, 0.47, 0.75)
    set_pen_width(2)
    line(0.5, 0.25, 0.5, 0.75)
    set_pen_width(3)
    line(0.53, 0.25, 0.53, 0.75)
    show(0.0)

    set_pen_color(CYAN)
    set_pen_width(1)
    line(0.25, 0.47, 0.75, 0.47)
    set_pen_width(2)
    line(0.25, 0.5, 0.75, 0.5)
    set_pen_width(3)
    line(0.25, 0.53, 0.75, 0.53)
    show(0.0)

    set_pen_width(0.5)
    set_pen_color(ORANGE)
    point(0.5, 0.5)
    show(0.0)

    set_pen_width(0.25)
    set_pen_color(BLUE)
    point(0.5, 0.5)
    show(0.0)

    set_pen_width(0.02)
    set_pen_color(RED)
    point(0.25, 0.25)
    show(0.0)

    set_pen_width(0.01)
    set_pen_color(GREEN)
    point(0.25, 0.25)
    show(0.0)

    set_pen_width(0)
    set_pen_color(BLACK)
    point(0.25, 0.25)
    show(0.0)

    set_pen_width(0.1)
    set_pen_color(RED)
    point(0.75, 0.75)
    show(0.0)

    set_pen_width(0)
    set_pen_color(CYAN)
    for i in range(0, 100):
        point(i / 512.0, 0.5)
        point(0.5, i / 512.0)
    show(0.0)

    set_pen_width(0)
    set_pen_color(MAGENTA)
    line(0.1, 0.1, 0.3, 0.3)
    line(0.1, 0.2, 0.3, 0.2)
    line(0.2, 0.1, 0.2, 0.3)
    show(0.0)

    set_pen_width(0.05)
    set_pen_color(MAGENTA)
    line(0.7, 0.5, 0.8, 0.9)
    show(0.0)

    set_pen_width(0.01)
    set_pen_color(YELLOW)
    circle(0.75, 0.25, 0.2)
    show(0.0)

    set_pen_width(0.01)
    set_pen_color(YELLOW)
    filled_circle(0.75, 0.25, 0.1)
    show(0.0)

    set_pen_width(0.01)
    set_pen_color(PINK)
    rectangle(0.25, 0.75, 0.1, 0.2)
    show(0.0)

    set_pen_width(0.01)
    set_pen_color(PINK)
    filled_rectangle(0.25, 0.75, 0.05, 0.1)
    show(0.0)

    set_pen_width(0.01)
    set_pen_color(DARK_RED)
    square(0.5, 0.5, 0.1)
    show(0.0)

    set_pen_width(0.01)
    set_pen_color(DARK_RED)
    filled_square(0.5, 0.5, 0.05)
    show(0.0)

    set_pen_width(0.01)
    set_pen_color(DARK_BLUE)
    polygon([0.4, 0.5, 0.6], [0.7, 0.8, 0.7])
    show(0.0)

    set_pen_width(0.01)
    set_pen_color(DARK_GREEN)
    set_font_size(24)
    text(0.2, 0.4, "hello, world")
    show(0.0)

    triangle(0.1, 0.1, 0.3, 0.1, 0.2, 0.3)
    quadrilateral(0.9, 0.9, 0.7, 0.9, 0.6, 0.7, 0.8, 0.7)
    show(0.0)

    elliptical_sector(0.8, 0.2, 0.1, 0.2, 220, 90)
    filled_ellipse(0.5, 0.5, 0.2, 0.1)
    show(0.0)

    # import picture as p
    # pic = p.Picture('saveIcon.png')
    # picture(pic, .5, .85)
    # show(0.0)

    # Test handling of mouse and keyboard events.
    set_pen_color(BLACK)
    print("Left click with the mouse or type a key")
    while True:
        if mouse_pressed():
            filled_circle(mouse_x(), mouse_y(), 0.02)
        if has_next_key_typed():
            print(next_key_typed())
        show(0.0)

    # Never get here.
    show()


# -----------------------------------------------------------------------


def _main():
    """
    Dispatch to a function that does regression testing, or to a
    dialog-box-handling function.
    """
    _regression_test()


if __name__ == "__main__":
    _main()
