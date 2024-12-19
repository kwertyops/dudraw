"""
color.py

The color module defines the Color class and some popular Color
objects.
"""

#-----------------------------------------------------------------------

class Color:
    """
    A Color object models an RGB with Alpha Transparency color.
    """

    #-------------------------------------------------------------------

    def __init__(self, r:int=0, g:int=0, b:int=0, a:int=255):
        """
        Construct self such that it has the given red (r),
        green (g), blue (b), and alpha (a) components.
        alpha (a) defaults to 255 which is non-transparent solid color.
        """
        self._r = r  # Red component
        self._g = g  # Green component
        self._b = b  # Blue component
        self._a = a  # Alpha Transparency component

    #-------------------------------------------------------------------

    def get_red(self) -> int:
        """
        Return the red component of self.
        """
        return self._r

    #-------------------------------------------------------------------

    def get_green(self) -> int:
        """
        Return the green component of self.
        """
        return self._g

    #-------------------------------------------------------------------

    def get_blue(self) -> int:
        """
        Return the blue component of self.
        """
        return self._b

    #-------------------------------------------------------------------

    def get_alpha(self) -> int:
        """
        Return the alpha transparency component of self.
        """
        return self._a

    #-------------------------------------------------------------------


    def __str__(self):
        """
        Return the string equivalent of self, that is, a
        string of the form '(r, g, b)'.
        """
        #return '#%02x%02x%02x' % (self._r, self._g, self._b)
        return '(' + str(self._r) + ', ' + str(self._g) + ', ' + \
            str(self._b) + ')'

#-----------------------------------------------------------------------

# Some predefined Color objects:

WHITE      = Color(255, 255, 255)
BLACK      = Color(  0,   0,   0)

RED        = Color(255,   0,   0)
GREEN      = Color(  0, 255,   0)
BLUE       = Color(  0,   0, 255)

CYAN       = Color(  0, 255, 255)
MAGENTA    = Color(255,   0, 255)
YELLOW     = Color(255, 255,   0)

DARK_RED   = Color(128,   0,   0)
DARK_GREEN = Color(  0, 128,   0)
DARK_BLUE  = Color(  0,   0, 128)

GRAY       = Color(128, 128, 128)
DARK_GRAY  = Color( 64,  64,  64)
LIGHT_GRAY = Color(192, 192, 192)

ORANGE     = Color(255, 200,   0)
VIOLET     = Color(238, 130, 238)
PINK       = Color(255, 175, 175)

# Shade of blue used in Introduction to Programming in Java.
# It is Pantone 300U. The RGB values are approximately (9, 90, 166).
BOOK_BLUE  = Color(  9,  90, 166)
BOOK_LIGHT_BLUE = Color(103, 198, 243)

# Shade of red used in Algorithms 4th edition
BOOK_RED   = Color(150,  35,  31)

#-----------------------------------------------------------------------

def _main():
    """
    For testing:
    """
    c1 = Color(128, 128, 128)
    print(c1)
    print(c1.get_red())
    print(c1.get_green())
    print(c1.get_blue())

    c2 = Color( 128, 64, 32, 16 )
    print(c2)
    print(c2.get_red())
    print(c2.get_green())
    print(c2.get_blue())
    print(c2.get_alpha())

if __name__ == '__main__':
    _main()
