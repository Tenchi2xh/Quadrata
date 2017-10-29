import math

default_style = {
    "stroke": "black",
    "stroke_width": 2,
    "fill": "black"
}


class Nib(object):
    def __init__(self, width, angle):
        self.width = width
        self.angle = math.radians(angle)
        self.offset_x = int(width * math.cos(self.angle))
        self.offset_y = int(width * -math.sin(self.angle))
        self.stem_width = width / math.cos(self.angle)  # cos(a) = stem / width

    def offsets(self, sign=1):
        return "l %d, %d" % (sign * self.offset_x, sign * self.offset_y)


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
            nib.offsets(-1),
            str(self.reverse()),
            nib.offsets()
        ]

        return " ".join(parts)


class Letter(object):
    def __init__(self, strokes, offset_pairs):
        self.strokes = strokes
        self.offset_pairs = offset_pairs

    def form(self, drawing, nib, style=default_style):
        group = drawing.g()
        for stroke, offsets in zip(self.strokes, self.offset_pairs):
            path = drawing.path(d=stroke.path(nib, offsets=offsets), **style)
            group.add(path)
        return group

    def combine(self, other):
        return Letter(self.strokes + other.strokes,
                      self.offset_pairs + other.offset_pairs)

    def add(self, stroke, offset_pair):
        return Letter(self.strokes + [stroke],
                      self.offset_pairs + [offset_pair])


_short = lambda command: lambda *values: Command(command, *values)
l = _short("l")
h = _short("h")
v = _short("v")
q = _short("q")
c = _short("c")
