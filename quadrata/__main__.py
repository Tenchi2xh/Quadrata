import svgwrite

from . import util
from .strokes import *

nib = Nib(width=30, angle=30)

i_d = d(l(50, 30),
        v(150),
        l(50, 30))

i2_d = d(q(20, -10, 25, 10),
         v(100),
         q(5, 20, 25, 10))

to_draw = i2_d.stroke(nib)

dwg = svgwrite.Drawing()
print(to_draw)
path = dwg.path(d=to_draw,
                stroke="black",
                stroke_width=0,
                fill="black")
shape = dwg.add(path)

xml = dwg.tostring()
util.preview(xml)
