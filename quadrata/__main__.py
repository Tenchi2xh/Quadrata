import svgwrite
import math

from . import util
from .strokes import Nib
from .hands import foundational

nib = foundational.nib

dwg = svgwrite.Drawing()

group = foundational.letter_m.form(dwg, nib)
group["transform"] = "translate(50, 50)"
print(group.tostring())

dwg.add(group)

xml = dwg.tostring()
util.preview(xml)
