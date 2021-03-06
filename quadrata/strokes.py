import math

default_style = {
    "stroke": "black",
    "stroke_width": 1,
    "fill": "none"
}


class Nib(object):
    def __init__(self, width, angle, thickness=1):
        self.width = width
        self.angle = math.radians(angle)
        self.thickness = thickness

        self.offset_x = int(width * math.cos(self.angle))
        self.offset_y = int(width * -math.sin(self.angle))
        self.stem_width = width * math.cos(self.angle)  # cos(a) = stem / width
        self.height = width * math.sin(self.angle)

    def _format_offsets(self, angle, width, sign):
        return "l %s, %s" % (str(sign * width * math.cos(angle)),
                             str(sign * width * -math.sin(angle)))

    def offsets(self, sign=1):
        return self._format_offsets(self.angle, self.width, sign)

    def thickness_offsets(self, sign=1):
        rotated = self.angle - math.pi / 2
        return self._format_offsets(rotated, self.thickness, sign)


class Command(object):
    def __init__(self, command, *values):
        self.command = command
        self.values = values

    def reverse(self):
        if self.command == "q":
            a, b, c, d = self.values
            A, B = a - c, b - d
            C, D = -c, -d
            return Command(self.command, A, B, C, D)
        elif self.command == "c":
            a, b, c, d, e, f = self.values
            A, B = c - e, d - f
            C, D = a - e, b - f
            E, F = -e, -f
            return Command(self.command, A, B, C, D, E, F)
        else:
            return Command(self.command, *(-value for value in self.values))

    def __str__(self):
        values = ", ".join([str(value) for value in self.values])
        return "%s %s" % (self.command, values)


class Stroke(object):
    def __init__(self, *commands):
        self.commands = commands

    def reverse(self):
        return Stroke(*(command.reverse() for command in reversed(self.commands)))

    def __str__(self):
        return " ".join([str(command) for command in self.commands])

    def path(self, nib, offsets=None):
        if not offsets:
            offsets = (nib.offset_x, -nib.offset_y)

        parts = [
            "M %s, %s" % (str(offsets[0]), str(offsets[1])),
            str(self),
            nib.thickness_offsets(1),
            nib.offsets(-1),
            str(self.reverse()),
            nib.thickness_offsets(-1),
            "Z"
        ]

        return " ".join(parts)


class Letter(object):
    def __init__(self, strokes=None, offset_pairs=None):
        self.strokes = strokes or []
        self.offset_pairs = offset_pairs or []

    def form(self, drawing, nib, style=default_style):
        group = drawing.g()
        for stroke, offsets in zip(self.strokes, self.offset_pairs):
            path = drawing.path(d=stroke.path(nib, offsets=offsets), **style)
            group.add(path)
        return group

    def path(self, nib):
        paths = []
        for stroke, offsets in zip(self.strokes, self.offset_pairs):
            paths.append(stroke.path(nib, offsets=offsets))
        return " ".join(paths)

    def _add(self, other, offset_pair, base_offset):
        if isinstance(other, Stroke):
            new_offset = (base_offset[0] + offset_pair[0],
                          base_offset[1] + offset_pair[1])
            return Letter(self.strokes + [other],
                          self.offset_pairs + [new_offset])
        elif isinstance(other, Letter):
            other_offsets = [(base_offset[0] + offset[0] + offset_pair[0],
                              base_offset[1] + offset[1] + offset_pair[1])
                             for offset in other.offset_pairs]
            return Letter(self.strokes + other.strokes,
                          self.offset_pairs + other_offsets)

    def add(self, other, offset_pair=(0, 0)):
        return self._add(other, offset_pair, (0, 0))

    def add_relative(self, other, offset_pair):
        base_offset = self.offset_pairs[-1][0], self.offset_pairs[-1][1]
        return self._add(other, offset_pair, base_offset)


class Hand(object):
    def __init__(self, name, nib,
                 x_height, ascender_height, descender_height, em, glyphs=None):
        self.name = name
        self.nib = nib
        self.x_height = x_height + nib.height
        self.ascender = self.x_height + ascender_height
        self.descender = -descender_height
        self.em = em
        self.glyphs = glyphs or {}


_short = lambda command: lambda *values: Command(command, *values)
l = _short("l")
h = _short("h")
v = _short("v")
q = _short("q")
c = _short("c")
