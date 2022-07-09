import sys
import os
sys.path.append(os.getcwd())
import src.dudraw as dudraw

dudraw.set_canvas_size(500,250)
dudraw.set_font_family("Courier")
dudraw.set_font_size(40)
dudraw.text(0.5, .2, "Courier 40 point")
dudraw.set_font_family("Helvetica")
dudraw.set_font_size(24)
dudraw.text(0.5,0.4, "Helvetica 24 point")
dudraw.set_font_family("Times New Roman")
dudraw.set_font_size(12)
dudraw.text(0.5, 0.6, "Times New Roman 12 point")
dudraw.set_font_family("Arial")
dudraw.set_font_size(6)
dudraw.text(0.5, 0.8, "Arial 6 point")

dudraw.show()
dudraw.save("test_test.bmp")