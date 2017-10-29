from ..strokes import *

nib = Nib(width=30, angle=30)

cl = 15   # "Length" of the club
xh = 105  # X-height
sw = nib.stem_width
cy = cl * math.tan(nib.angle)  # Vertical offset of the start of the club
sh = xh - cy - cl # Height of the stem starting from the base of the club

tail = q(5, 10, 20, 5)

short_stem_without_club = Stroke(v(xh), tail)
club = Stroke(l(cl, cl))
n_curve = Stroke(c(sw, -cl, 1.5*sw, -cl, 1.5*sw, cl), v(sh), tail)

short_stem = Letter(
    strokes=[
        short_stem_without_club,
        club
    ],
    offset_pairs = [
        (0, 0),
        (-cl - 0.5, cy)
    ]
)

letter_n = short_stem.add(n_curve, (sw - cl, cy))
letter_m = letter_n.add(n_curve, (3*sw - cl, cy))
