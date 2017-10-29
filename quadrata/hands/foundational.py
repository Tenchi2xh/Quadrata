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

tail = c(0, 7, 15, 10, 20, 5)

n_curve = Stroke(c(sw, -cl, 2*sw, -cl, 2*sw, cl), v(sh), tail)
u_curve = Stroke(c(0, cl, 1.5*sw, cl, 2.5*sw, 0))
o_lower_curve = Stroke(c(-nw, nw, 0, sh + cy + nw, 3*sw, sh))
q_upper_curve = Stroke(c(1.5*nw, -nw, sw*4 - nw, -cm, sw*4, -cm))

short_stem_without_club = Stroke(v(xh), tail)
short_stem_without_club_long_tail = Stroke(v(xh), u_curve)
descender_stem_without_club = Stroke(v(xh + de), tail)

short_stem = (Letter()
    .add(short_stem_without_club)
    .add(club, (-cl - 0.5, cy)))
short_stem_long_tail = (Letter()
    .add(short_stem_without_club_long_tail)
    .add(club, (-cl - 0.5, cy)))
letter_n = short_stem.add_relative(n_curve, (cl + sw, 0))
letter_m = letter_n.add_relative(n_curve, (3 * sw, 0))
letter_q = (Letter()
    .add(o_lower_curve, (0, cm))
    .add_relative(q_upper_curve, (0, 0))
    .add(descender_stem_without_club, (sw * 4, 0)))
letter_u = short_stem_long_tail.add(short_stem, (3.5 * sw, 0))

foundational = Hand(name="Foundational Hand",
                    nib=nib,
                    x_height=xh,
                    ascender_height=ac,
                    descender_height=de,
                    em=sw * 6)

foundational.glyphs = {
    "m": letter_m,
    "n": letter_n,
    "q": letter_q,
    "u": letter_u
}
