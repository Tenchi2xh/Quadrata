import math


class Nib(object):
    def __init__(self, width, angle):
        self.width = width
        self.angle = math.radians(angle)
        self.offset_x = int(width * math.cos(self.angle))
        self.offset_y = int(width * -math.sin(self.angle))

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
        else:
            return Command(self.command, *(-value for value in self.values))

    def __str__(self):
        values = ", ".join([str(value) for value in self.values])
        return "%s %s" % (self.command, values)


class Data(object):
    def __init__(self, *commands):
        self.commands = commands

    def reverse(self):
        return Data(*(command.reverse() for command in reversed(self.commands)))

    def __str__(self):
        return " ".join([str(command) for command in self.commands])

    def stroke(self, nib):
        parts = [
            "M %d, %d" % (nib.offset_x, -nib.offset_y),
            str(self),
            nib.offsets(-1),
            str(self.reverse()),
            nib.offsets()
        ]

        return " ".join(parts)


short = lambda command: lambda *values: Command(command, *values)
l, h, v, q = short("l"), short("h"), short("v"), short("q")
d = Data
