from ..strokes import *

nib = Nib(width=30, angle=35)
nw = nib.width
sw = nib.stem_width

cl = nw / 2  # "Length" of the club
xh = nw * 4  # X-height
ac = nw * 2  # Ascender
de = nw * 2  # Descender

cy = cl * math.tan(nib.angle)  # Vertical offset of the start of the club
cm = nib.height + cy  # Vertical offset of the middle of the club
sh = xh - cy - cl # Height of the stem starting from the base of the club
club = Stroke(l(cl, cl))

tail = q(5, 10, 20, 5)

short_stem_without_club = Stroke(v(xh), tail)
descender_stem_without_club = Stroke(v(xh + de), tail)

n_curve = Stroke(c(sw, -cl, 2*sw, -cl, 2*sw, cl), v(sh), tail)
o_lower_curve = Stroke(c(-nw, nw, 0, sh + cy + nw, 3*sw, sh))
q_upper_curve = Stroke(
    c(1.5*nw, -nw, sw*4 - nw, -cm, sw*4, -cm)
)

short_stem = (Letter()
    .add(short_stem_without_club)
    .add(club, (-cl - 0.5, cy)))
letter_n = short_stem.add_relative(n_curve, (cl + sw, 0))
letter_m = letter_n.add_relative(n_curve, (3 * sw, 0))
letter_q = (Letter()
    .add(o_lower_curve, (0, cm))
    .add_relative(q_upper_curve, (0, 0))
    .add(descender_stem_without_club, (sw * 4, 0)))

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
