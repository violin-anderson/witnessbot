#!/usr/bin/env python3

class boardData:
    def __init__(self, name, region, startcoords, clickedsens,
                 bordercoords=None, blurshape=(5,2), linethresh=15, minspread=5,
                 squares=False, stars=False, hexes=False, edgeHexes=False,
                 colorsquares=False, triangles=False):
        self.name = name
        self.region = region
        self.startcoords = (startcoords[0] - region[1], startcoords[1] - region[0])
        self.clickedsens = clickedsens
        self.bordercoords = None
        if bordercoords:
            self.bordercoords = (bordercoords[0] - region[1], bordercoords[1] - region[0])
        self.blurshape = blurshape
        self.linethresh = linethresh
        self.minspread = minspread
        self.squares = squares
        self.stars = stars
        self.hexes = hexes
        self.edgeHexes = edgeHexes
        self.colorsquares = colorsquares
        self.triangles = triangles

ONE = boardData("one", (715, 295, 1190, 755), (750, 750), 1.2, blurshape=(6,2))

TWO = boardData("two", (715, 295, 1200, 775), (730, 760), 2, (360, 840))

THREE = boardData("three", (715, 295, 1200, 765), (730, 760), 1.1, (300, 950), blurshape=(6,2), squares=True)

FOUR = boardData("four", (0, 0, 350, 275), (255, 20), 1.4, linethresh=0, edgeHexes=True)

FSSE = boardData("fsse", (770, 350, 1145, 725), (695, 805), [2, 1.1, 1.7], stars=True, hexes=True)

NINE = boardData("nine", (0, 0, 200, 200), (180, 20), [1.115, 1.115, 1.115], squares=True) 

TEN = boardData("ten", (0, 0, 200, 200), (180, 20), [1.115, 1.115, 1.115], colorsquares=True) 

ELEVEN = boardData("eleven", (0, 0, 600, 600), (550, 50), 1.12, blurshape=(6,2), triangles=True)

THIRTEEN = boardData("thirteen", (870, 200, 1050, 800), (760, 970), 1.75, blurshape=(6,2), minspread=10, squares=True)

FOURTEEN = boardData("fourteen", (870, 200, 1050, 800), (760, 970), 1.75, blurshape=(6,2), minspread=10, edgeHexes=True)

#COLDRAW = boardData("coldraw", (855, 220, 1060, 860), (760, 970), 1.65, blurshape=(1,1), linethresh=400, minspread=2)
COLDRAW = boardData("coldraw", (870, 200, 1050, 800), (760, 970), 1.75, blurshape=(1,1), linethresh=400, minspread=2)
CYLHORIZ = [265, 350, 430, 510, 590, 670, 750]
