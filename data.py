#!/usr/bin/env python3

class boardData:
    def __init__(self, name, region, basecoords, startcoords, clickedsens,
                 bordercoords=None, blurshape=(5,2),
                 squares=False, stars=False, hexes=False, edgeHexes=False):
        self.name = name
        self.region = region
        #self.basecoords = (basecoords[0] - region[1], basecoords[1] - region[0])
        self.startcoords = (startcoords[0] - region[1], startcoords[1] - region[0])
        self.clickedsens = clickedsens
        self.bordercoords = None
        if bordercoords:
            self.bordercoords = (bordercoords[0] - region[1], bordercoords[1] - region[0])
        self.blurshape = blurshape
        self.squares = squares
        self.stars = stars
        self.hexes = hexes
        self.edgeHexes = edgeHexes

ONE = boardData("one", (715, 295, 1190, 755), (400, 950), (750, 750), 1.2, blurshape=(6,2))

TWO = boardData("two", (715, 295, 1200, 775), (480, 960), (730, 760), 2, (360, 840))

THREE = boardData("three", (715, 295, 1200, 765), (490, 935), (730, 760), 1.1, (300, 950), blurshape=(6,2), squares=True)

FOUR = boardData("four", (0, 0, 350, 275), (490, 935), (255, 30), 1.4, edgeHexes=True)

FSSE = boardData("fsse", (770, 350, 1145, 725), (400, 820), (695, 805), [2, 1.1, 1.7], stars=True, hexes=True)

NITE = boardData("nite", (775, 355, 1140, 725), (0, 0), (680, 810), 1.1, stars=True)