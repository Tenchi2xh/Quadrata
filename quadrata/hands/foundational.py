from ..strokes import *

nib = Nib(width=30, angle=30)
nw = nib.width
sw = nib.stem_width

cl = nw / 2  # "Length" of the club
xh = nw * 4  # X-height
ac = nw * 2  # Ascender
de = nw * 2  # Descender

cy = cl * math.tan(nib.angle)  # Vertical offset of the start of the club
sh = xh - cy - cl # Height of the stem starting from the base of the club
club = Stroke(l(cl, cl))

tail = q(5, 10, 20, 5)

short_stem_without_club = Stroke(v(xh), tail)
descender_stem_without_club = Stroke(v(xh), tail)

n_curve = Stroke(c(sw, -cl, 2*sw, -cl, 2*sw, cl), v(sh), tail)

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

letter_n = short_stem.add_relative(n_curve, (cl + sw, 0))
letter_m = letter_n.add_relative(n_curve, (3 * sw, 0))

foundational = Hand(name="Foundational Hand",
                    nib=nib,
                    xheight=xh,
                    ascender=ac,
                    descender=de,
                    em=sw * 6)

foundational.glyphs = {
    "n": letter_n,
    "m": letter_m
}
