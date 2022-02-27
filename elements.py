#!/usr/bin/env python3

class Element():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"{self.type}@{self.x},{self.y}"
    def __eq__(self, other):
        return self.type == other.type and self.x == other.x and self.y == other.y

class Block(Element):
    def __init__(self, x, y, x2, y2):
        self.type = "block"
        self.x2 = x2
        self.y2 = y2
        super().__init__(x, y)
    def __repr__(self):
        return f"Block@{self.x},{self.y}; {self.x2},{self.y2}"
    def __eq__(self, other):
        if self.type != other.type:
            return False
        if self.x == other.x and self.y == other.y and self.x2 == other.x2 and self.y2 == other.y2:
            return True
        return self.x == other.x2 and self.y == other.y2 and self.x2 == other.x and self.y2 == other.y

class Square(Element):
    def __init__(self, x, y, color):
        self.type = "square"
        self.color = color
        super().__init__(x, y)
    def __repr__(self):
        return f"{self.color} {self.type}@{self.x},{self.y}"

class Hex(Element):
    "color is b, c, or o"
    def __init__(self, x, y, color='b'):
        self.type = "hex"
        super().__init__(x, y)
        self.color = color
        self.c = None
    def __repr__(self):
        return f"{self.type}@{self.x},{self.y} {self.color}"

class EdgeHex(Element):
    def __init__(self, x1, y1, x2, y2):
        self.type = "edgehex"
        super().__init__(x1, y1)
        self.x2 = x2
        self.y2 = y2
        self.c1 = None
        self.c2 = None
    def __repr__(self):
        return f"EdgeHex@{self.x},{self.y}; {self.x2},{self.y2}"
    def __eq__(self, other):
        return self.type == other.type and self.x == other.x and self.y == other.y and self.x2 == other.x2 and self.y2 == other.y2

class Star(Element):
    def __init__(self, x, y, color='w'):
        self.type = "star"
        self.color = color
        super().__init__(x, y)

class Null(Element):
    def __init__(self, x, y, color = "w"):
        self.type = "null"
        super().__init__(x, y)

class Tetris(Element):
    def __init__(self, x, y, shape, rotating=False, negative=False):
        if not (0, 0) in shape:
            raise Exception("Tetris shape must contain (0, 0)")
        self.type = "tetris"
        self.shape = shape
        self.rotating = rotating
        self.negative = negative
        super().__init__(x, y)

class Triangle(Element):
    def __init__(self, x, y, count):
        self.type = "triangle"
        self.count = count
        super().__init__(x, y)
    def __repr__(self):
        return f"{self.type}@{self.x},{self.y}x{self.count}"
