#!/usr/bin/env python3

import itertools
import elements as boardElements

class Corner():
    def __init__(self, x, y, pixel):
        self.x = x
        self.y = y
        self.pixel = pixel
        self.edges = []
        self.end = False
        self.elements = []
        
        self.friend = None
        self.alt = False # Whether this corner is a part of the symmetrical line

        self.to = None
        self.best = None
    
    def store(self):
        self.best = self.to
    
    def restore(self):
        self.to = self.best
    
    def __str__(self):
        return f"Corner@{self.x},{self.y}"
    
    def __repr__(self):
        return f"Corner@{self.x},{self.y}"

class Cell():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.connections = [] #(cell, (corner, corner))
        self.element = None
    
    def __str__(self):
        return f'Cell@{self.x},{self.y}'
    
    def __repr__(self):
        return f'Cell@{self.x},{self.y}'
    
    def getNeighbors(self):
        neighbors = []
        for neighbor, corners in self.connections:
            if neighbor is not None and corners[0].to != corners[1] and corners[1].to != corners[0]:
                neighbors.append(neighbor)
        return neighbors

def dfs(startnode, best, depth):
    if startnode.end:
        yield "Found"
    
    if best[0] and depth > best[0]:
        return

    for i in range(len(startnode.edges)):
        if not startnode.edges[i].to and (not startnode.friend or\
            (startnode.edges[i] != startnode.friend.edges[i] and startnode != startnode.friend.edges[i])):
            startnode.to = startnode.edges[i]
            if startnode.friend:
                #assert(not startnode.friend.edges[i].to)
                #assert(len(startnode.friend.edges) == len(startnode.edges))
                startnode.friend.to = startnode.friend.edges[i]
                startnode.friend.alt = True
                startnode.friend.to.alt = True
            for sln in dfs(startnode.edges[i], best, depth+1):
                yield sln
            if startnode.friend:
                startnode.friend.to.alt = False
    startnode.to = None
    if startnode.friend:
        startnode.friend.to = None
        startnode.friend.alt = False

def getGroups(cells):
    cells = cells[:]
    groups = []
    while len(cells):
        group = []
        start = cells[0]
        group.append(start)
        i = 0
        while i < len(group):
            neighbors = group[i].getNeighbors()
            for n in neighbors:
                if not n in group:
                    group.append(n)
            i += 1
        for c in group:
            cells.remove(c)
        groups.append(group)
    return groups

def fitTetris(groupCoords, tetris, dims, negCoords=set(), negTetris=[]):
    if len(tetris) == 0:
        if negTetris:
            return fitTetris(negCoords, negTetris, dims)
    
        return True

    t = tetris.pop()
    base = set([(x, y) for x, y in t.shape])
    if t.rotating:
        allBases = [base, [(y, -x) for x, y in base],
                         [(-x, -y) for x, y in base], [(-y, x) for x, y in base]]
    else:
        allBases = [base]
    for base in allBases:
        for dx, dy in itertools.product(list(range(dims[0])), list(range(dims[1]))):
            translated = set([(x+dx, y+dy) for x, y in base])
            if not any([x < 0 or x >= dims[0] or y < 0 or y >= dims[1] for x, y in translated]):
                if not negTetris:
                    if groupCoords.issuperset(translated):
                        groupCoords.difference_update(translated)
                        if fitTetris(groupCoords, tetris, dims):
                            return True
                        groupCoords.update(translated)
                else:
                    newNegs = translated - groupCoords
                    removing = groupCoords.intersection(translated)
                    if not any([n in negCoords for n in newNegs]):
                        groupCoords.difference_update(removing)
                        negCoords.update(newNegs)
                        if fitTetris(groupCoords, tetris, dims, negCoords, negTetris):
                            return True
                        groupCoords.update(removing)
                        negCoords.difference_update(newNegs)
    tetris.append(t)
    return False

def checkTetris(tetris, g, dims):
    if len(tetris) == 0:
        return True
    cellcount = sum([len(t.shape) * (t.negative * -2 + 1) for t in tetris])
    if cellcount == 0:
        return True
    if cellcount != len(g):
        return False
    groupCoords = set([(c.x, c.y) for c in g])
    neg = []
    pos = []
    for t in tetris:
        if t.negative:
            neg.append(t)
        else:
            pos.append(t)
    return fitTetris(groupCoords, pos, dims, set(), neg)

def validateGroups(groups, dims, cornermap):
    for g in groups:
        elements = []
        hexes = []
        for c in g:
            if c.element:
                elements.append(c.element)
            for conn in c.connections:
                hexes.extend(conn[1][0].elements)
                hexes.extend(conn[1][1].elements)
        
        temp = []
        for h in hexes:
            if not h in temp:
                temp.append(h)
        hexes = temp
        
        nulls = len(list(filter(lambda e: e.type == "null", elements)))
        mistakes = 0
        
        for h in hexes:
            if h.type == "hex":
                if not (h.c.to or any([d.to == h.c for r in cornermap for d in r])):
                    mistakes += 1
                elif (h.color == 'c' and h.c.alt) or (h.color == 'o' and not h.c.alt):
                    mistakes += 1
            elif h.type == "edgehex":
                if not (h.c1.to == h.c2 or h.c2.to == h.c1):
                    mistakes += 1
        
        if mistakes > nulls:
            return False
        
        triangles = list(filter(lambda e: e.type == "triangle", elements))
        for tri in triangles:
            adj = len(list(filter(lambda c: c[1][0].to == c[1][1] or c[1][1].to == c[1][0], tri.cell.connections)))
            if adj != tri.count:
                mistakes += 1
    
        if mistakes > nulls:
            return False
        
        squares = [e.color for e in filter(lambda e: e.type == "square", elements)]
        if not all([s == squares[0] for s in squares]):
            # ToDo: Handle case where the majority should be nulled (unlikely to be an issue)
            mistakes += min([len(list(filter(lambda e: e == i, elements))) for i in elements])
        
        if mistakes > nulls:
            return False
        
        stars = list(filter(lambda e: e.type == "star", elements))
        while len(stars) > 0:
            color = stars[0].color
            starcount = len(list(filter(lambda s: s.color == color, stars)))
            othercount = len(list(filter(lambda s: s == color, squares)))#ToDo:  Handle colored nulls, tetri
            if starcount + othercount != 2:
                mistakes += abs(min(othercount-2, 0) + starcount)
            stars = list(filter(lambda s: s.color != color, stars))
        
        tetris = list(filter(lambda e: e.type == "tetris", elements))
        if mistakes > nulls or mistakes + len(tetris) < nulls:
            return False
        
        for t in itertools.combinations(tetris, len(tetris) - nulls + mistakes):
            if not checkTetris(t, g, dims):
                return False
    
    return True

def getSlnLength(startnode):
    ret = 0
    on = startnode
    while on.to:
        on = on.to
        ret += 1
    return ret

class Board():
    def __init__(self, vertLines, horizLines, elements, starts, ends, symmetry=None, cylinder=False):
        self.width = len(vertLines)-1
        self.height = len(horizLines)-1
        self.vertLines = vertLines
        self.horizLines = horizLines
        self.elements = elements
        self.starts = starts
        self.ends = ends
        self.symmetry = symmetry #mirror, parallel, rot, or rotparallel
        self.cylinder = cylinder
        if self.symmetry is not None:
            assert(len(starts) == 2)
        self.cornermap = None
        self.cellmap = None
        self.startnode = None

    def __str__(self):
        if not self.cornermap:
            return "No solution found"
        image = [list(" ".join(["." for c in row])) for row in self.cornermap]
        for row in self.cornermap:
            for corner in row:
                if corner.to:
                    if corner.x == corner.to.x:
                        x = corner.x * 2
                        y = max(corner.y, corner.to.y)
                        image[y][x] = "|"
                    else:
                        y = corner.y
                        if self.cylinder and (corner.x == 0 and corner.to.x != 1) or (corner.to.x == 0 and corner.x != 1):
                            image[y] += "_"
                        else:
                            x = corner.x + corner.to.x
                            image[y][x] = "_"
        return "\n".join(["".join(r) for r in image])
    
    def getSlnCoords(self):
        ret = []
        on = self.startnode
        ret.append(on.pixel)
        while on.to:
            on = on.to
            ret.append(on.pixel)
        if self.symmetry == 'rot':
            if on.x == 0:
                ret.append((on.pixel[0]-20, on.pixel[1]))
            else:
                ret.append((on.pixel[0]+20, on.pixel[1]))
        else:
            ret.append((on.pixel[0], on.pixel[1]-50))
        
# =============================================================================
#         i = 1
#         while i < len(ret)-1:
#             if ret[i][0] == ret[i-1][0] == ret[i+1][0] or ret[i][1] == ret[i-1][1] == ret[i+1][1]:
#                 ret.pop(i)
#             else:
#                 i += 1
# =============================================================================
        return ret
    
    def solve(self, optimal=False):
        cornermap = []
        for y in range(self.height + 1):
            row = []
            for x in range(self.width + 1):
                row.append(Corner(x, y, (self.vertLines[x], self.horizLines[y])))
            cornermap.append(row)
        
        if self.symmetry is not None:
            mx = self.starts[1][0]
            my = len(cornermap)-1
            for y in range(self.height + 1):
                for x in range(self.width + 1):
                    if not cornermap[y][x].edges:
                        if self.symmetry == 'rot':
                            friend = cornermap[my-y][(mx-x)%len(cornermap[0])]
                        elif self.symmetry == 'mirror':
                            friend = cornermap[y][(mx-x)%len(cornermap[0])]
                        elif self.symmetry == 'parallel':
                            friend = cornermap[y][(mx+x)%len(cornermap[0])]
                        elif self.symmetry == 'rotparallel':
                            friend = cornermap[my-y][(mx+x)%len(cornermap[0])]
                        cornermap[y][x].friend = friend
                        friend.friend = cornermap[y][x]
                        for x2, y2 in [(x+1, y), (x, y-1), (x, y+1), (x-1, y)]:
                            if y2 >= 0 and y2 < len(cornermap) and (self.cylinder or (x2 >= 0 and x2 < len(cornermap[0]))):
                                cornermap[y][x].edges.append(cornermap[y2][x2%len(cornermap[0])])
                                if self.symmetry == 'rot':
                                    friend.edges.append(cornermap[my-y2][(mx-x2)%len(cornermap[0])])
                                elif self.symmetry == 'mirror':
                                    friend.edges.append(cornermap[y2][(mx-x2)%len(cornermap[0])])
                                elif self.symmetry == 'parallel':
                                    friend.edges.append(cornermap[y2][(mx+x2)%len(cornermap[0])])
                                elif self.symmetry == 'rotparallel':
                                    friend.edges.append(cornermap[my-y2][(mx+x2)%len(cornermap[0])])
        else:
            for y in range(self.height + 1):
                for x in range(self.width + 1):
                    for x2, y2 in [(x+1, y), (x, y-1), (x, y+1), (x-1, y)]:
                        if y2 >= 0 and y2 < len(cornermap) and x2 >= 0 and x2 < len(cornermap[0]):
                            cornermap[y][x].edges.append(cornermap[y2][x2])
            
        for x, y in self.ends:
            cornermap[y][x].end = True
        
        cellmap = []
        for y in range(self.height):
            row = []
            for x in range(self.width + self.cylinder):
                row.append(Cell(x, y))
            cellmap.append(row)

        for y in range(self.height):
            for x in range(self.width + self.cylinder):
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    if dx:
                        cx1 = cx2 = int(x + dx * 0.5 + 0.5)
                        cy1 = y
                        cy2 = y + 1
                    else:
                        cy1 = cy2 = int(y + dy * 0.5 + 0.5)
                        cx1 = x
                        cx2 = x + 1
                    if y + dy >= 0 and y + dy < len(cellmap) and (self.cylinder or (x + dx >= 0 and x + dx < len(cellmap[0]))):
                        cellmap[y][x].connections.append((cellmap[y + dy][(x + dx)%len(cornermap[0])], (cornermap[cy1][cx1%len(cornermap[0])], cornermap[cy2][cx2%len(cornermap[0])])))
                    else:
                        cellmap[y][x].connections.append((None, (cornermap[cy1][cx1%len(cornermap[0])], cornermap[cy2][cx2%len(cornermap[0])])))
        
        for e in self.elements:
            if e.type == "block":
                if self.symmetry is not None:
                    pos = cornermap[e.y][e.x].edges.index(cornermap[e.y2][e.x2])
                    cornermap[e.y][e.x].edges.pop(pos)
                    cornermap[e.y][e.x].friend.edges.pop(pos)
                    pos = cornermap[e.y2][e.x2].edges.index(cornermap[e.y][e.x])
                    cornermap[e.y2][e.x2].edges.pop(pos)
                    cornermap[e.y2][e.x2].friend.edges.pop(pos)
                else:
                    cornermap[e.y][e.x].edges.remove(cornermap[e.y2][e.x2])
                    cornermap[e.y2][e.x2].edges.remove(cornermap[e.y][e.x])
            elif e.type == "hex":
                e.c = cornermap[e.y][e.x]
                cornermap[e.y][e.x].elements.append(e)
            elif e.type == "edgehex":
                e.c1 = cornermap[e.y][e.x%(len(cornermap[0]))]
                e.c2 = cornermap[e.y2][e.x2%(len(cornermap[0]))]
                cornermap[e.y][e.x%(len(cornermap[0]))].elements.append(e)
                cornermap[e.y2][e.x2%(len(cornermap[0]))].elements.append(e)
            elif e.type in ["square", "star", "null", "tetris", "triangle"]:
                cellmap[e.y][e.x].element = e
                e.cell = cellmap[e.y][e.x]
        
        #flatCorners = [c for r in cornermap for c in r]
        flatCells = [c for r in cellmap for c in r]
        
        best = [0]
        for xs, ys in self.starts:
            startnode = cornermap[ys][xs]
            for sln in dfs(startnode, best, 0):
# =============================================================================
#                 sln = \
# """._._. . ._.
# . . |_. | .
# . . . | | .
# . ._. |_| .
# . | | . . .
# . | |_. . .
# ._| . |_._."""
#                 self.cornermap = cornermap
#                 #print(self)
#                 if self.__str__() == sln:
#                     print("here")
#                 else:
#                     del self.cornermap
# =============================================================================
                groups = getGroups(flatCells)
                length = getSlnLength(startnode)
                if not best[0] or length < best[0]:
                    if validateGroups(groups, (self.width, self.height), cornermap):
                        self.startnode = startnode
                        self.cornermap = cornermap
                        self.cellmap = cellmap
                        if not optimal:
                            return True
                        best[0] = length
                        [c.store() for r in cornermap for c in r]
        
        if best[0]:
            [c.restore() for r in cornermap for c in r]
            return True
        return False

if __name__ == "__main__":
# =============================================================================
#     elts = [boardElements.Square(1, 2, 'w'), boardElements.Square(2, 4, 'b'),
#             boardElements.Square(3, 3, 'b'), boardElements.Square(4, 5, 'w'),
#             boardElements.Square(5, 5, 'b'), boardElements.Square(5, 0, 'w')]
#     b = Board([0]*6, [0]*7, elts, [(0, 6), (5, 0)], [(5, 6), (0, 0)], symmetry='rot', cylinder=True)
#     print(b.solve())
#     print(b)
# =============================================================================

# =============================================================================
#     elts = [boardElements.Square(0, 4, 'b'), boardElements.Square(1, 2, 'w'),
#             boardElements.Square(2, 2, 'w'), boardElements.Square(3, 1, 'b'),
#             boardElements.Square(3, 2, 'b'), boardElements.Square(4, 0, 'w')]
#     b = Board([0]*6, [0]*7, elts, [(0, 6), (3, 6)], [(0, 0), (3, 0)], symmetry='parallel', cylinder=True)
#     print(b.solve())
#     print(b)
# =============================================================================

# =============================================================================
#     elts = [boardElements.EdgeHex(1, 6, 2, 6), boardElements.EdgeHex(2, 0, 2, 1),
#             boardElements.EdgeHex(2, 3, 2, 4), boardElements.EdgeHex(3, 0, 4, 0),
#             boardElements.EdgeHex(3, 6, 4, 6), boardElements.EdgeHex(4, 2, 5, 2),
#             boardElements.EdgeHex(5, 2, 5, 3), boardElements.EdgeHex(5, 4, 5, 5)]
#     b = Board([0]*6, [0]*7, elts, [(0, 6), (5, 6)], [(0, 0), (5, 0)], symmetry='mirror', cylinder=True)
#     print(b.solve())
#     print(b)
# =============================================================================

    elts = [boardElements.EdgeHex(1, 5, 1, 6), boardElements.EdgeHex(1, 5, 2, 5),
            boardElements.EdgeHex(1, 6, 2, 6), boardElements.EdgeHex(2, 4, 2, 5),
            boardElements.EdgeHex(2, 2, 3, 2), boardElements.EdgeHex(4, 4, 5, 4),
            boardElements.EdgeHex(5, 3, 6, 3)]
    b = Board([0]*6, [0]*7, elts, [(0, 6), (3, 6)], [(0, 0), (3, 0)], symmetry='parallel', cylinder=True)
    print(b.solve())
    print(b)
    