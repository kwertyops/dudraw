"""
dudraw.py

The dudraw module defines functions that allow the user to create a
simple 2-dimensional drawing.  A drawing appears on the canvas.  The canvas appears
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

# Has the left mouse button been clicked since last check?
_mouse_clicked = False

# Has the left mouse button been released since last check?
_mouse_released = False

# Is the left mouse button being held??
_mouse_is_pressed = False

# Is the mouse being click-and-dragged?
_mouse_dragged = False

# The position of the mouse
_mouse_pos = (0.0, 0.0)


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


def _ccw(a,b,c):
    return (c[1]-a[1]) * (b[0]-a[0]) > (b[1]-a[1]) * (c[0]-a[0])


def _intersect(a, b, c, d):
    return _ccw(a, c, d) != _ccw(b, c, d) and _ccw(a, b, c) != _ccw(a, b, d)


# -----------------------------------------------------------------------

# Private functions to scale and factor X and Y values.


def _scale_x(x: float) -> float:
    return _canvas_width * (x - _xmin) / (_xmax - _xmin)


def _scale_y(y: float) -> float:
    return _canvas_height * (_ymax - y) / (_ymax - _ymin)


def _scale_point(p: Sequence[float]) -> Sequence[float]:
    return (_scale_x(p[0]), _scale_y(p[1]))


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
    """Set the size of the canvas to w pixels wide and h pixels high.
    
    Calling this function is optional. If you call it, you must do
    so before calling any drawing function.

    @param w: width of canvas in pixels, defaults to 512
    @param h: height of canvas in pixels, defaults to 512
    @raises Exception: error if the dudraw window was already created
    @raises Exception: error if width or height values are non-positive
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
    """Return the width of the current canvas.


    @return: the canvas width in pixels
    """
    return abs(_xmax - _xmin)


def get_canvas_height() -> float:
    """Return the height of the current canvas.

    @return: the canvas height in pixels
    """
    return abs(_ymax - _ymin)


def get_pixel_color(x: float, y: float) -> Color:
    """Return the color of the pixel at the given user coordinates.

    @param x: the x-coordinate of the pixel
    @param y: the y-coordinate of the pixel
    @return: the color of the pixel at (x, y)
    """
    _make_sure_window_created()
    c = _surface.get_at((int(_scale_x(x)), int(_scale_y(y))))
    return Color(c[0], c[1], c[2])


def set_x_scale(min: float = _DEFAULT_XMIN, max: float = _DEFAULT_XMAX):
    """Set the x-scale of the canvas such that the minimum y value
    is min and the maximum y value is max.

    The value of max must be greater than the value of min

    @param min: the minimum value of the x-scale, defaults to 0.0 if no value is passed
    @param max: the maximum value of the x-scale, defaults to 1.0 if no value is passed
    @raises Exception: error if the min value is greater or equal to the max value
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
    """ Set the y-scale of the canvas such that the minimum y value
    is min and the maximum y value is max.

    The value of max must be greater than the value of min

    @param min: the minimum value of the y-scale, defaults to 0.0 if no value is passed
    @param max: the maximum value of the y-scale, defaults to 1.0 if no value is passed
    @raises Exception: error if the min value is greater or equal to the max value
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


def set_scale(min: float, max: float):
    """Set the x-scale and y-scale of the canvas to the same range for
    both directions.

    The value of max must be greater than the value of min

    @param min: the minimum value of the x-scale and y-scale, defaults to 0.0 if no value is passed
    @param max: the maximum value of the x-scale and y-scale, defaults to 1.0 if no value is passed
    @raises Exception: error if the min value is greater or equal to the max value
    """
    set_x_scale(min, max)
    set_y_scale(min, max)


def set_pen_width(w: float = _DEFAULT_PEN_WIDTH):
    """Set the pen width/radius to w 
    
    This affects the subsequent drawing
    of points and lines. If w is 0.0, then points will be drawn with
    the minimum possible width and lines with the minimum possible
    width.
    @arg w: new value for the pen radius in pixels. This value must be non-negative, defaults to 0.0

    @raises Exception: error thrown if the value of w is negative
    """
    global _pen_width
    w = float(w)
    if w < 0.0:
        raise Exception("Argument to set_pen_width() must be non-neg")
    # _penRadius = r * float(_DEFAULT_CANVAS_SIZE)
    _pen_width = w


def set_pen_color(c: Color = _DEFAULT_PEN_COLOR):
    """Set the pen color to c, where c is an object of class Color.
    c defaults to dudraw.BLACK.

    @param c: the new pen color, defaults to black if no value is passed
    """
    global _pen_color
    _pen_color = c


def set_pen_color_rgb(r: int = 255, g: int = 255, b: int = 255):
    """Set the pen color using red, green, and blue values.
    Defaults to black.

    @param r: red color value. 0 for minimum red and 255 for maximum red, defaults to 255
    @param g: green color value. 0 for minimum red and 255 for maximum green, defaults to 255
    @param b: blue color value. 0 for minimum red and 255 for maximum blue, defaults to 255
    """
    c = Color(r, g, b)
    global _pen_color
    _pen_color = c


def get_pen_color():
    """Return the pen color as an object of class Color.


    @return: the current value of pen color. This is an object of class Color
    """
    return _pen_color


def set_font_family(f: str = _DEFAULT_FONT_FAMILY):
    """Set the font family to f (e.g. 'Helvetica' or 'Courier').

    This changes the font used to draw text on the canvas.

    @param f: the new font used for text on canvas, defaults to "Helvetica" if no font is specified
    """
    global _font_family
    _font_family = f


def set_font_size(s: int = _DEFAULT_FONT_SIZE):
    """Set the font size to s (e.g. 12, 14, 16..etc).

    the value of the font size is measured in point. A point is equivalent to about 1.33 pixels


    @param s: new font size in point, defaults to 12 if no value is specified
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

# Functions to draw shapes, text, and images on the canvas.


def _pixel(x: float, y: float):
    """
    Draw on the canvas a pixel at (x, y).
    """
    _make_sure_window_created()
    xs = _scale_x(x)
    xy = _scale_y(y)
    pygame.gfxdraw.pixel(_surface, int(round(xs)), int(round(xy)), _pygame_color(_pen_color))


def point(x: float, y: float):
    """Draw on the canvas a point at coordinates (x, y).

    The placement of the point on the canvas will depend on the values of (x, y) as well as the x-scale and y-scale. Note that if the coordinates are outside the range of min and max x-scale or y-scale then the point won't appear on the canvas

    @param x: the x-coordinate of the point
    @param y: the y-coordinate of the point
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


def line(x0: float, y0: float, x1: float, y1: float):
    """Draw on the canvas a line from (x0, y0) to (x1, y1).

    The placement of the line on the canvas will depend on the values of (x1, y1), (x2, y2) as well as the x-scale and y-scale. Note that if the coordinates are outside the range of min and max x-scale or y-scale then the point won't appear on the canvas

    @param x0: x-coordinate of the first point of the line segment
    @param y0: y-coordinate of the first point of the line segment
    @param x1: x-coordinate of the second point of the line segment
    @param y1: y-coordinate of the second point of the line segment
    """
    _make_sure_window_created()
    x0 = float(x0)
    y0 = float(y0)
    x1 = float(x1)
    y1 = float(y1)

    if _pen_width_pixels() < 2.0:
        x0s = _scale_x(x0)
        y0s = _scale_y(y0)
        x1s = _scale_x(x1)
        y1s = _scale_y(y1)
        pygame.draw.line(_surface, _pygame_color(_pen_color), (x0s, y0s), (x1s, y1s), int(_line_width_pixels()))
    else:
        polyline((x0, x1), (y0, y1))


def circle(x: float, y: float, r: float):
    """Draw on the canvas a circle of radius r centered on
    (x, y).

    @param x: x-coordinate of the center of the circle
    @param y: y-coordinate of the center of the circle
    @param r: radius of the circle
    """
    _make_sure_window_created()
    x = float(x)
    y = float(y)
    r = float(r)
    line_width = _line_width_pixels()
    ws = _factor_x(2.0 * r) + line_width # fudge factor because pygame stroke is inner
    hs = _factor_y(2.0 * r) + line_width
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
    """Draw on the canvas a filled circle of radius r
    centered on (x, y).

    @param x: x-coordinate of the center of the circle
    @param y: y-coordinate of the center of the circle
    @param r: radius of the circle
    """
    _make_sure_window_created()
    x = float(x)
    y = float(y)
    r = float(r)
    ws = _factor_x(r)
    hs = _factor_y(r)
    # If the radius is too small, then simply draw a pixel.
    if (ws <= 1.0) and (hs <= 1.0):
        _pixel(x, y)
    else:
        xs = _scale_x(x)
        ys = _scale_y(y)

        pygame.gfxdraw.filled_ellipse(_surface, int(xs), int(ys), int(ws), int(hs), _pygame_color(_pen_color))
        pygame.gfxdraw.aaellipse(_surface, int(xs), int(ys), int(ws), int(hs), _pygame_color(_pen_color))


def ellipse(x: float, y: float, half_width: float, half_height: float):
    """   Draw on the canvas an ellipse centered at (x, y) with
    a width of 2.0 * half_width, and a height of 2.0 * half_height.

    @param x: x-coordinate of the center of the ellipse
    @param y: y-coordinate of the center of the ellipse
    @param half_width: half the width of the ellipse. Width is the maximum horizontal distance between two points on the surface of the ellipse 
    @param half_height: half the height of the ellipse. Height is the maximum vertical distance between two points on the surface of the ellipse 
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
    """Draw on the canvas a filled ellipse centered at (x, y)
    with a width of 2.0 * half_width, and a height of 2.0 * half_height.

    @param x: x-coordinate of the center of the ellipse
    @param y: y-coordinate of the center of the ellipse
    @param half_width: half the width of the ellipse. Width is the maximum horizontal distance between two points on the surface of the ellipse 
    @param half_height: half the height of the ellipse. Height is the maximum vertical distance between two points on the surface of the ellipse 
    """
    _make_sure_window_created()
    x = float(x)
    y = float(y)
    half_width = float(half_width)
    half_height = float(half_height)
    ws = _factor_x(half_width)
    hs = _factor_y(half_height)
    if (ws <= 1.0) and (hs <= 1.0):
        # If the radius is too small, then simply draw a pixel.
        _pixel(x, y)
    else:
        xs = _scale_x(x)
        ys = _scale_y(y)

        pygame.gfxdraw.filled_ellipse(_surface, int(xs), int(ys), int(ws), int(hs), _pygame_color(_pen_color))
        pygame.gfxdraw.aaellipse(_surface, int(xs), int(ys), int(ws), int(hs), _pygame_color(_pen_color))


def rectangle(x: float, y: float, half_width: float, half_height: float):
    """Draw on the canvas a rectangle of width (2 * halfWidth
    and height (2 * halfHeight) centered at point (x, y).

    @param x: x-coordinate of the center of the rectangle
    @param y: y-coordinate of the center of the rectangle
    @param half_width: half the width of the rectangle
    @param half_height: half the height of the rectangle
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
    """Draw on the canvas a rectangle of width (2 * halfWidth
    and height (2 * halfHeight) centered at point (x, y).

    @param x: x-coordinate of the center of the rectangle
    @param y: y-coordinate of the center of the rectangle
    @param half_width: half the width of the rectangle
    @param half_height: half the height of the rectangle
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
    """Draw on the canvas a square whose sides are of length
    2r, centered on (x, y).

    @param x: x-coordinate of the center of the square
    @param y: y-coordinate of the center of the square
    @param r: half the width of the square
    """
    _make_sure_window_created()
    rectangle(x, y, r, r)


def filled_square(x: float, y: float, r: float):
    """Draw on the canvas a filled square whose sides are of
    length 2r, centered on (x, y).

    @param x: x-coordinate of the center of the square
    @param y: y-coordinate of the center of the square
    @param r: half the width of the square
    """
    _make_sure_window_created()

    filled_rectangle(x, y, r, r )


def polyline(x: Sequence[float], y: Sequence[float]):
    """Draw on the canvas a polyline with coordinates
    (x[i], y[i]).

    The lists x and y must contain the same number of values. The two lists correspond to x-coordinates and y-coordinates of points (x[0], y[0]), (x[1], y[1]), (x[2], y[2]),..., (x[-1], y[-1]) on the polyline. Each point on the polyline connects to the point that follows it so (x_0, x_0) connects to (x[1], y[1]) with a straight line, then (x[1], y[1]) connects to (x[2], y[2]) and so on.
    @param x: a list of x-coordinates of the points on the polyline 
    @param y: a list of y-coordinates of the points on the polyline
    """
    global _surface
    _make_sure_window_created()
    inner_points = []
    outer_points = []

    for i in range(len(x)):
        a = (x[i-1], y[i-1])
        b = (x[i], y[i])
        c = (x[(i+1)%len(x)], y[(i+1)%len(x)])
        if a == b:
            a = (x[i-2], y[i-2])
        if b == c:
            c = (x[(i+2)%len(x)], y[(i+2)%len(x)])
        if i == 0:
            bc = pygame.math.Vector2(c[0] - b[0], c[1] - b[1]).normalize()
            w = bc.rotate(90).normalize()
            w.scale_to_length(_pen_width/2.0)
            inner_points.append((b[0] + w.x, b[1] + w.y))
            outer_points.append((b[0] - w.x, b[1] - w.y))
        elif i == len(x) - 1:
            ba = pygame.math.Vector2(a[0] - b[0], a[1] - b[1]).normalize()
            w = ba.rotate(90).normalize()
            w.scale_to_length(_pen_width/2.0)
            if _intersect(inner_points[-1],
                          (b[0] + w.x, b[1] + w.y), 
                          outer_points[-1], 
                          (b[0] - w.x, b[1] - w.y)):
                outer_points.append((b[0] + w.x, b[1] + w.y))
                inner_points.append((b[0] - w.x, b[1] - w.y))
            else:
                inner_points.append((b[0] + w.x, b[1] + w.y))
                outer_points.append((b[0] - w.x, b[1] - w.y))
        else:
            ba = pygame.math.Vector2(a[0] - b[0], a[1] - b[1]).normalize()
            bc = pygame.math.Vector2(c[0] - b[0], c[1] - b[1]).normalize()
            angle = math.acos(ba.dot(bc))
            turn = ba.rotate(90).dot(bc) < 0.0
            ba.scale_to_length(_pen_width / (2.0 * math.sin(angle)))
            bc.scale_to_length(_pen_width / (2.0 * math.sin(angle)))
            if turn:
                inner_points.append((b[0] + ba.x + bc.x, b[1] + ba.y + bc.y))
                outer_points.append((b[0] - ba.x - bc.x, b[1] - ba.y - bc.y))
            else:
                outer_points.append((b[0] + ba.x + bc.x, b[1] + ba.y + bc.y))
                inner_points.append((b[0] - ba.x - bc.x, b[1] - ba.y - bc.y))

    for i in range(len(inner_points)-1):
        points = (
            _scale_point(inner_points[i]),
            _scale_point(inner_points[i+1]),
            _scale_point(outer_points[i+1]),
            _scale_point(outer_points[i]))

        pygame.gfxdraw.filled_polygon(_surface, points, _pygame_color(_pen_color))
        pygame.gfxdraw.aapolygon(_surface, points, _pygame_color(_pen_color))

def polygon(x: Sequence[float], y: Sequence[float]):
    """Draw on the canvas a polygon with coordinates
    (x[i], y[i]).

    The lists x and y must contain the same number of values. The two lists correspond to x-coordinates and y-coordinates of points (x[0], y[0]), (x[1], y[1]), (x[2], y[2]),..., (x[-1], y[-1]) on the polygon. Each point on the polygon connects to the point that follows it so (x_0, x_0) connects to (x[1], y[1]) with a straight line, then (x[1], y[1]) connects to (x[2], y[2]) and so on until (x[-1], y[-1]) connects to (x[0], y[0]).
    @param x: a list of x-coordinates of the points on the polygon 
    @param y: a list of y-coordinates of the points on the polygon
    """
    global _surface
    _make_sure_window_created()
    inner_points = []
    outer_points = []

    for i in range(len(x)):
        a = (x[i-1], y[i-1])
        b = (x[i], y[i])
        c = (x[(i+1)%len(x)], y[(i+1)%len(x)])
        if a == b:
            a = (x[i-2], y[i-2])
        if b == c:
            c = (x[(i+2)%len(x)], y[(i+2)%len(x)])
        ba = pygame.math.Vector2(a[0] - b[0], a[1] - b[1]).normalize()
        bc = pygame.math.Vector2(c[0] - b[0], c[1] - b[1]).normalize()
        angle = math.acos(ba.dot(bc))
        turn = ba.rotate(90).dot(bc) < 0.0
        ba.scale_to_length(_pen_width / (2.0 * math.sin(angle)))
        bc.scale_to_length(_pen_width / (2.0 * math.sin(angle)))
        if turn:
            inner_points.append((b[0] + ba.x + bc.x, b[1] + ba.y + bc.y))
            outer_points.append((b[0] - ba.x - bc.x, b[1] - ba.y - bc.y))
        else:
            outer_points.append((b[0] + ba.x + bc.x, b[1] + ba.y + bc.y))
            inner_points.append((b[0] - ba.x - bc.x, b[1] - ba.y - bc.y))

    for i in range(-1, len(inner_points)-1):
        points = (
            _scale_point(inner_points[i]),
            _scale_point(inner_points[i+1]),
            _scale_point(outer_points[i+1]),
            _scale_point(outer_points[i]))

        pygame.gfxdraw.filled_polygon(_surface, points, _pygame_color(_pen_color))
        pygame.gfxdraw.aapolygon(_surface, points, _pygame_color(_pen_color))

def filled_polygon(x: Sequence[float], y: Sequence[float]):
    """Draw on the canvas a filled polygon with coordinates
    (x[i], y[i]).

    The lists x and y must contain the same number of values. The two lists correspond to x-coordinates and y-coordinates of points (x[0], y[0]), (x[1], y[1]), (x[2], y[2]),..., (x[-1], y[-1]) on the polygon. Each point on the polygon connects to the point that follows it so (x_0, x_0) connects to (x[1], y[1]) with a straight line, then (x[1], y[1]) connects to (x[2], y[2]) and so on until (x[-1], y[-1]) connects to (x[0], y[0]).
   
    @param x: a list of x-coordinates of the points on the polygon 
    @param y: a list of y-coordinates of the points on the polygon
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

    pygame.gfxdraw.filled_polygon(_surface, points, _pygame_color(_pen_color))
    pygame.gfxdraw.aapolygon(_surface, points, _pygame_color(_pen_color))


def triangle(x0: float, y0: float, x1: float, y1: float, x2: float, y2: float):
    """Draw a triangle on the canvas with corners at (x0, y0),
    (x1, y1), and (x2, y2).

    @param x0: x-coordinate of the first point of the triangle
    @param y0: y-coordinate of the first point of the triangle
    @param x1: x-coordinate of the second point of the triangle
    @param y1: y-coordinate of the second point of the triangle
    @param x2: x-coordinate of the third point of the triangle
    @param y2: y-coordinate of the third point of the triangle
    """
    _make_sure_window_created()
    polygon([x0, x1, x2], [y0, y1, y2])


def filled_triangle(x0: float, y0: float, x1: float, y1: float, x2: float, y2: float):
    """Draw a filled triangle on the canvas with corners at
    (x0, y0), (x1, y1), and (x2, y2).

    @param x0: x-coordinate of the first point of the triangle
    @param y0: y-coordinate of the first point of the triangle
    @param x1: x-coordinate of the second point of the triangle
    @param y1: y-coordinate of the second point of the triangle
    @param x2: x-coordinate of the third point of the triangle
    @param y2: y-coordinate of the third point of the triangle
    """
    _make_sure_window_created()
    filled_polygon([x0, x1, x2], [y0, y1, y2])


def quadrilateral(x0: float, y0: float, x1: float, y1: float, x2: float, y2: float, x3: float, y3: float):
    """Draw a quadrilateral on the canvas with corners at (x0, y0),
    (x1, y1), (x2, y2), and (x3, y3).

    @param x0: x-coordinate of the first point of the quadrilateral
    @param y0: y-coordinate of the first point of the quadrilateral
    @param x1: x-coordinate of the second point of the quadrilateral
    @param y1: y-coordinate of the second point of the quadrilateral
    @param x2: x-coordinate of the third point of the quadrilateral
    @param y2: y-coordinate of the third point of the quadrilateral
    @param x3: x-coordinate of the fourth point of the quadrilateral
    @param y3: y-coordinate of the fourth point of the quadrilateral
    """
    _make_sure_window_created()
    polygon([x0, x1, x2, x3], [y0, y1, y2, y3])


def filled_quadrilateral(x0: float, y0: float, x1: float, y1: float, x2: float, y2: float, x3: float, y3: float):
    """Draw a filled quadrilateral on the canvas with corners at
    (x0, y0), (x1, y1), (x2, y2), and (x3, y3).

    @param x0: x-coordinate of the first point of the quadrilateral
    @param y0: y-coordinate of the first point of the quadrilateral
    @param x1: x-coordinate of the second point of the quadrilateral
    @param y1: y-coordinate of the second point of the quadrilateral
    @param x2: x-coordinate of the third point of the quadrilateral
    @param y2: y-coordinate of the third point of the quadrilateral
    @param x3: x-coordinate of the fourth point of the quadrilateral
    @param y3: y-coordinate of the fourth point of the quadrilateral
    """
    _make_sure_window_created()
    filled_polygon([x0, x1, x2, x3], [y0, y1, y2, y3])


def arc(x: float, y: float, r: float, angle1: float, angle2: float):
    """Draw an arc portion between angle1 and angle2, of the
    circumference of a circle centered at (x, y) with a radius r.

    An arc is a contiguous portion of a circle between angle1 and angle2. Note that the line of arc starts at angle1 and goes to angle2 in counter clock-wise direction.

    @param x: x-coordinate of the center of the circle 
    @param y: y-coordinate of the center of the circle 
    @param r: the radius of the circle
    @param angle1: the starting angle of the arc 
    @param angle2: the ending angle of the arc
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
    xs = []
    ys = []
    for i in range(0, int(num_points) + 1):
        angle_in = angle1 + (i * 360 / circle_points)
        angle_in = angle_in * math.pi / 180
        x0 = (math.cos(angle_in) * r) + x
        y0 = (math.sin(angle_in) * r) + y
        xs.append(x0)
        ys.append(y0)
    polyline(xs, ys)


def elliptical_arc(x: float, y: float, half_width: float, half_height: float, angle1: float, angle2: float):
    """Draw an arc portion between angle1 and angle2, of the
    circumference of an ellipse centered at (x, y) with a width
    of half_width, and a height of 2.0 * half_height.

    An arc is a contiguous portion of the ellipse between angle1 and angle2. Note that the line of arc starts at angle1 and goes to angle2 in counter clock-wise direction.

    @param x: x-coordinate of the center of the ellipse
    @param y: y-coordinate of the center of the ellipse
    @param half_width: half the width of the ellipse. Width is the maximum horizontal distance between two points on the surface of the ellipse 
    @param half_height: half the height of the ellipse. Height is the maximum vertical distance between two points on the surface of the ellipse 
    @param angle1: the starting angle of the arc 
    @param angle2: the ending angle of the arc
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
    xs = []
    ys = []
    for i in range(0, int(num_points) + 1):
        angle_in = angle1 + (i * 360 / circle_points)
        angle_in = angle_in * math.pi / 180
        x0 = (math.cos(angle_in) * half_width) + x
        y0 = (math.sin(angle_in) * half_height) + y
        xs.append(x0)
        ys.append(y0)
    polyline(xs, ys)


def sector(x: float, y: float, r: float, angle1: float, angle2: float):
    """Draw a sector portion between angle1 and angle2, of the
    interior of a circle centered at (x, y) with a radius r.

    This is like a slice of circle shaped pizza. Note that the line of the arc of the sector starts at angle1 and goes to angle2 in counter clock-wise direction.
    
    @param x: x-coordinate of the center of the circle 
    @param y: y-coordinate of the center of the circle 
    @param r: the radius of the circle
    @param angle1: the starting angle of the arc 
    @param angle2: the ending angle of the arc
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
    polygon(xvals[:-1], yvals[:-1])


def filled_sector(x: float, y: float, r: float, angle1: float, angle2: float):
    """Draw a filled sector portion between angle1 and angle2, of the
    interior of a circle centered at (x, y) with a radius r.

    This is like a slice of circle shaped pizza. Note that the line of the arc of the sector starts at angle1 and goes to angle2 in counter clock-wise direction.

    @param x: x-coordinate of the center of the circle 
    @param y: y-coordinate of the center of the circle 
    @param r: the radius of the circle
    @param angle1: the starting angle of the arc 
    @param angle2: the ending angle of the arc
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
    """Draw a sector portion between angle1 and angle2, of the
    interior of an ellipse centered at (x, y) with a width
    of half_width, and a height of 2.0 * half_height.

    This is like a slice of an elliptical shaped pizza. Note that the line of the arc of the sector starts at angle1 and goes to angle2 in counter clock-wise direction.

    @param x: x-coordinate of the center of the ellipse
    @param y: y-coordinate of the center of the ellipse
    @param half_width: half the width of the ellipse. Width is the maximum horizontal distance between two points on the surface of the ellipse 
    @param half_height: half the height of the ellipse. Height is the maximum vertical distance between two points on the surface of the ellipse 
    @param angle1: the starting angle of the arc 
    @param angle2: the ending angle of the arc
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
    polygon(xvals[:-1], yvals[:-1])


def filled_elliptical_sector(
    x: float, y: float, half_width: float, half_height: float, angle1: float, angle2: float
):
    """Draw a filled sector portion between angle1 and angle2, of
    the interior of an ellipse centered at (x, y) with a width
    of half_width, and a height of 2.0 * half_height.

    This is like a slice of an elliptical shaped pizza. Note that the line of the arc of the sector starts at angle1 and goes to angle2 in counter clock-wise direction.

    @param x: x-coordinate of the center of the ellipse
    @param y: y-coordinate of the center of the ellipse
    @param half_width: half the width of the ellipse. Width is the maximum horizontal distance between two points on the surface of the ellipse 
    @param half_height: half the height of the ellipse. Height is the maximum vertical distance between two points on the surface of the ellipse 
    @param angle1: the starting angle of the arc 
    @param angle2: the ending angle of the arc
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
    """Draw an annulus centered at (x, y) with outer
    radius r1, and inner radius r2.

    An annulus is a ring shape region between two circles centered at the same point but the outer circle r1 has larger radius than the inner circle r2

    @param x: x-coordinate of the center of the two circles
    @param y: x-coordinate of the center of the two circles
    @param r1: radius of of the outer circle (larger radius) 
    @param r2: radius of of the inner circle (smaller radius)
    """
    _make_sure_window_created()
    circle(x, y, r1)
    circle(x, y, r2)


def filled_annulus(x: float, y: float, r1: float, r2: float):
    """Draw a filled annulus centered at (x, y) with outer
    radius r1, and inner radius r2.

    An annulus is a ring shape region between two circles centered at the same point but the outer circle r1 has larger radius than the inner circle r2

    @param x: x-coordinate of the center of the two circles
    @param y: x-coordinate of the center of the two circles
    @param r1: radius of of the outer circle (larger radius) 
    @param r2: radius of of the inner circle (smaller radius)
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
    """Draw a line of string on the canvas centered at (x, y).

    The string will appear on a single line. Note that (x, y) is the center of the rectangle that bounds the string. The string uses the current font and font size. Font and font size can be modified using the methods: set_font_family and set_font_size

    @param x: x-coordinate of the center of the text
    @param y: y-coordinate of the center of the text
    @param s: the string that will be draw on the canvas
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


def picture(filepath: str, x: float = None, y: float = None):
    """Draw pic on the canvas centered at (x, y). 
    
    The file can be of type .jpg, .png, .gif or .bmp.  Filepath is specified as a string, and (x, y) defaults to the midpoint of the canvas. 

    @param filepath: a string representing the path of the image file
    @param x: x-coordinate of the center of the image, defaults to x-coordinate of the center of the canvas
    @param y: y-coordinate of the center of the image, defaults to y-coordinate of the center of the canvas 
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
    pic = pygame.image.load(filepath)
    ws = pic.get_width()
    hs = pic.get_height()
    _surface.blit(pic, [xs - ws / 2.0, ys - hs / 2.0, ws, hs])


def clear(c: Color = WHITE):
    """Clear the canvas to color c, where c is an
    object of class Color. c defaults to dudraw.WHITE.

    @param c: the color to be used to clear the background, defaults to white
    """
    _make_sure_window_created()
    _surface.fill(_pygame_color(c))


def clear_rgb(r: float = 255, g: float = 255, b: float = 255):
    """Clear the canvas to color defined by
    r, g, and b. Defaults to white (255, 255, 255).

    @param r: red color value. 0 for minimum red and 255 for maximum red, defaults to 255
    @param g: green color value. 0 for minimum red and 255 for maximum green, defaults to 255
    @param b: blue color value. 0 for minimum red and 255 for maximum blue, defaults to 255   
    """
    c = Color(r, g, b)
    _make_sure_window_created()
    _surface.fill(_pygame_color(c))


def save(filepath: str):
    """Save the window canvas as a .jpg to filepath specified.

    @param filepath: the path of a folder to which the image will be saved
    """
    _make_sure_window_created()
    if not filepath.lower().endswith(".jpg"):
        filepath += ".jpg"
    pygame.image.save(_surface, filepath)


# -----------------------------------------------------------------------


def _show():
    """
    Copy the canvas to the window canvas.
    """
    _background.blit(_surface, (0, 0))
    pygame.display.flip()
    _check_for_events()


def _show_and_wait_forever():
    """
    Copy the canvas to the window canvas. Then wait
    forever, that is, until the user closes the dudraw window.
    """
    _make_sure_window_created()
    _show()
    QUANTUM = 0.1
    while True:
        time.sleep(QUANTUM)
        _check_for_events()


def show(msec: float = 0.0):
    """Copy the canvas to the window canvas, and
    then wait for msec milliseconds. msec defaults to 0.0.

    Note that everything we draw is on the canvas so won't show on the screen until we call show

    @param msec: amount of milliseconds to wait after show, defaults to 0.0
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
    global _mouse_clicked
    global _mouse_is_pressed
    global _mouse_dragged
    global _mouse_released
    # -------------------------------------------------------------------
    # End added by Alan J. Broder
    # -------------------------------------------------------------------

    _make_sure_window_created()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            _keys_typed = [event.unicode] + _keys_typed
        elif event.type == pygame.MOUSEMOTION:
            _mouse_pos = event.pos
            _mouse_dragged = event.buttons[0] == 1

        # ---------------------------------------------------------------
        # Begin added by Alan J. Broder
        # ---------------------------------------------------------------
        # Every time the mouse button is pressed, remember
        # the mouse position as of that press.
        elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):
            _mouse_is_pressed = True
            _mouse_clicked = True
        # ---------------------------------------------------------------
        # End added by Alan J. Broder
        # ---------------------------------------------------------------
        elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
            _mouse_is_pressed = False
            _mouse_dragged = False
            _mouse_released = True
# -----------------------------------------------------------------------

# Functions for retrieving keys


def has_next_key_typed() -> bool:
    """Return True if the queue of keys the user typed is not empty.
    Otherwise return False.

    @return: True if a keyboard key is in the queue; False otherwise
    """

    global _keys_typed
    return _keys_typed != []


def next_key_typed() -> str:
    """Remove the first key from the queue of keys that the the user typed,
    and return that key.

    @return: a string representing the next key in the queue
    """
    global _keys_typed
    return _keys_typed.pop()


# -----------------------------------------------------------------------
# Begin added by Alan J. Broder
# -----------------------------------------------------------------------

# Functions for dealing with mouse clicks


def mouse_clicked() -> bool:
    """Return True if the left mouse button has been pressed since the last check,
    and False otherwise.

    @return: True if the left mouse button has been pressed since last check; False otherwise
    """
    global _mouse_clicked
    if _mouse_clicked:
        _mouse_clicked = False
        return True
    return False

def mouse_released() -> bool:
    """Return True if the left mouse button has been released since the last check,
    and False otherwise.

    @return: True if the left mouse button has been released since last check; False otherwise
    """
    global _mouse_released
    if _mouse_released:
        _mouse_released = False
        return True
    return False

def mouse_is_pressed() -> bool:
    """Return True if the left mouse button is currently being held down,
    and False otherwise.

    @return: True if the left mouse button is pressed; False otherwise
    """
    global _mouse_is_pressed
    return _mouse_is_pressed


def mouse_dragged() -> bool:
    """Return True if the mouse is being click-and-dragged on the canvas,
    and False otherwise.

    @return: True if the mouse has moved while held; False otherwise
    """
    global _mouse_dragged
    return _mouse_dragged


def mouse_x() -> float:
    """Return the x coordinate in user space of the location at
    which the mouse was most recently left-clicked. 
    
    If a left-click hasn't happened yet, raise an exception, since mouseX() shouldn't
    be called until mousePressed() returns True.

    @raises Exception: error if mouse has not been clicked yet
    @return: the x-coordinate of the location of the mouse
    """
    global _mouse_pos
    return _user_x(_mouse_pos[0])


def mouse_y() -> float:
    """Return the y coordinate in user space of the location at
    which the mouse was most recently left-clicked. 
    
    If a left-click hasn't happened yet, raise an exception, since mouseY() shouldn't be called until mousePressed() returns True.

    @raises Exception: error if mouse has not been clicked yet
    @return: the y-coordinate of the location of the mouse 
    """
    global _mouse_pos
    return _user_y(_mouse_pos[1])


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
    show(10000000)

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
        if mouse_is_pressed():
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
