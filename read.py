#!/usr/bin/env python3

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors
from skimage import segmentation
from skimage import feature
from scipy.ndimage import measurements
import board, elements, data
import math

DEBUG = 0

BASETHRESHOLD = 40
BLACKTHRESHOLD = 20
BOARDERTHRESHOLD = 30
STARTHRESH = 0.75
SQUARETHRESH = 0.75
HEXTHRESH = 15

BDJ = 8 #Block Delta maJor
BDN = 2 #Block Delta miNor
BLOCKTHRESHOLD = 0.95

TETRAD = 13
TETSPRD = 3
TETTHRESH = 0.5

def find_centers(image, dim, boardData):
    shape = boardData.blurshape
    if dim:
        shape = shape[::-1]
    res = image.astype(int)
    for i in range(shape[0]):
        res = res[:-1 * 2**i] + res[2**i:]
    
    for i in range(shape[1]):
        res = res[:, :-1 * 2**i] + res[:, 2**i:]
    
    clipped = (res > (2**sum(shape))*0.8).astype(int)
    clipped[0,:] = 0
    clipped[-1,:] = 0
    clipped[:,0] = 0
    clipped[:,-1] = 0
    
    if DEBUG >= 2:
        plt.imshow(clipped, cmap='gray')
        plt.show()
        #plt.imshow((res > 100), cmap='gray')
        #plt.show()
    
    arr = np.sum(clipped, dim)
    arr = np.greater(arr, boardData.linethresh)
    arr = np.diff(arr.astype(int))
    starts = np.argwhere(arr==1)
    ends = np.argwhere(arr==-1)
    ret = np.concatenate((starts, ends), 1)
    ret = ret[ret[:,1]-ret[:,0] > boardData.minspread]
    return np.average(ret, 1).astype(int) + 2**(min(shape)-1)
    

def get_linemap(image, boardData):
    #image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    if boardData.name == "four":
        findline = segmentation.flood(image, boardData.startcoords, tolerance=40)
    elif boardData.name == "eleven":
        findline = segmentation.flood(image[:,:,2], boardData.startcoords, tolerance=10)
    else:
        image = cv.cvtColor(image, cv.COLOR_BGR2Lab)
        findline = segmentation.flood(image[:,:,1], boardData.startcoords, tolerance=10)
    if boardData.bordercoords:
        findboarder = segmentation.flood(image[:,:,1], boardData.bordercoords, tolerance=3)
        findline = np.invert(findboarder) & findline
    findline[0,:] = False
    findline[-1,:] = False
    findline[:,0] = False
    findline[:,-1] = False
    if DEBUG >= 2:
        plt.imshow(findline, cmap='gray')
        plt.show()
    return findline

def clean_hexes(image, boardData):
    template = cv.imread("images/fourhex.png")[:,:,2]
    image = image[:,:,2]
    
    locs = []
    res = cv.matchTemplate(image, template, cv.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv.minMaxLoc(res)
    while max_val > 0.8:
        locs.append((max_loc[1]+7, max_loc[0]+7))
        
        if DEBUG >= 3:
            demo = np.copy(image)
            demo[locs[-1][0],:] = 0
            demo[:,locs[-1][1]] = 0
            plt.imshow(demo)
            plt.show()
            
        image = segmentation.flood_fill(image, locs[-1], image[boardData.startcoords], tolerance=40)
        res = cv.matchTemplate(image, template, cv.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv.minMaxLoc(res)
        
    if DEBUG >= 2:
        plt.imshow(image)
        print(np.max(res))
        plt.show()
    return image, locs

def get_blocks(vert_centers, horiz_centers, linemap):
    linemap = linemap.astype(float)
    elts = []
    for x in range(vert_centers.shape[0]-1):
        for y in range(horiz_centers.shape[0]):
            centerx = (vert_centers[x] + vert_centers[x+1]) // 2
            transy = horiz_centers[y]
            dn = 0
            if y == 7 and x == 0:
                dn = 2 # Something special to help out two
            if np.sum(linemap[transy-BDN-dn:transy+BDN+dn, centerx-BDJ:centerx+BDJ]) < (BDN+dn)*BDJ*4*BLOCKTHRESHOLD:
                elts.append(elements.Block(x, y, x+1, y))
                if DEBUG >= 1:
                    linemap[transy-BDN-dn:transy+BDN+dn, centerx-BDJ:centerx+BDJ] += 0.5
            elif DEBUG >= 1:
                linemap[transy-BDN-dn:transy+BDN+dn, centerx-BDJ:centerx+BDJ] -= 0.5
    
    for x in range(vert_centers.shape[0]):
        for y in range(horiz_centers.shape[0]-1):
            transx = vert_centers[x]
            centery = (horiz_centers[y] + horiz_centers[y+1]) // 2
            dn = 0
            if x == 0 and y == 6:
                dn = 2 # Something special to help out two
            if np.sum(linemap[centery-BDJ:centery+BDJ, transx-BDN-dn:transx+BDN+dn]) < (BDN+dn)*BDJ*4*BLOCKTHRESHOLD:
                elts.append(elements.Block(x, y, x, y+1))
                if DEBUG >= 1:
                    linemap[centery-BDJ:centery+BDJ, transx-BDN-dn:transx+BDN+dn] += 0.5
            elif DEBUG >= 1:
                linemap[centery-BDJ:centery+BDJ, transx-BDN-dn:transx+BDN+dn] -= 0.5
    
    if DEBUG >= 1:
        plt.imshow(linemap, cmap='gray')
        plt.show()
    return elts

def find_target(target, image, vert_centers, horiz_centers, threshold):
        res = cv.matchTemplate(image, target, cv.TM_SQDIFF_NORMED)
        locs = np.argwhere(res <= threshold)
        if DEBUG >= 2:
            plt.subplot(121),plt.imshow(res, cmap='gray')
            plt.subplot(122),plt.imshow(res <= threshold, cmap='gray')
            plt.show()
        
        hist = np.histogram2d(locs[:,0], locs[:,1], bins=[horiz_centers, vert_centers])[0]
        return np.argwhere(hist > 0)

def add_edgeHexes(elts, vert_centers, horiz_centers, hexes):
    vert_centers = np.array(vert_centers)
    horiz_centers = np.array(horiz_centers)
    for y, x in hexes:
        diff = np.abs(horiz_centers-y)
        if np.min(diff) < 6:
            iy = np.argmin(diff)
            ix = np.sum((vert_centers - x) < 0)
            
            target = elements.Block(ix, iy, ix-1, iy)
            for e in elts:
                if e == target:
                    elts.remove(e)
                    
            elts.append(elements.EdgeHex(ix, iy, ix-1, iy))
            
        else:
            diff = np.abs(vert_centers-x)
            assert(np.min(diff) < 6)
            ix = np.argmin(diff)
            iy = np.sum((horiz_centers - y) < 0)
            
            target = elements.Block(ix, iy, ix, iy-1)
            for e in elts:
                if e == target:
                    elts.remove(e)
                    
            elts.append(elements.EdgeHex(ix, iy, ix, iy-1))

def get_hexes(image, linemap, vert_centers, horiz_centers, boardData):
    if not boardData.hexes or not ((len(vert_centers) == 5 and len(horiz_centers) == 5)\
    or (len(vert_centers) == 7 and len(horiz_centers) == 7)):
        return []
    
    if len(vert_centers) == 7:
        image2 = cv.cvtColor(image, cv.COLOR_BGR2HSV)[:,:,2]
        delta = 11
        if DEBUG >= 2:
            plt.imshow(image[:,:,0])
            plt.show()
    else:
        image2 = image[:,:,1]
        delta = 10
    
    elts = []
    for iy, y in enumerate(horiz_centers):
        for ix, x in enumerate(vert_centers):
            center = image2[y,x]
            if linemap[y,x] or len(vert_centers) == 7:
                edge = None
                for coords in [(y+delta, x), (y-delta, x)]:
                    if linemap[coords]:
                        edge = image2[coords]
                        if DEBUG >= 2:
                            image2[y:coords[0], x] = 255
                            image2[coords[0]:y, x] = 255
                        break
                
                if DEBUG >= 3:
                    print(f"{ix}, {iy} hex: ctr {center}, edg {edge}")
                if edge is None:
                    continue
                if edge > center and edge - center > HEXTHRESH:
                    elts.append(elements.Hex(ix, iy))
                if len(vert_centers) == 7 and center > edge and center - edge > 80:
                    if image[y,x][2] > 200:
                        elts.append(elements.Hex(ix, iy, 'o'))
                    else:
                        elts.append(elements.Hex(ix, iy, 'c'))
    
    if DEBUG >= 2:
        plt.imshow(image2)
        plt.show()
    return elts

def map_tetris(locsquare, currloc, currxy, foundxy):
    for delta in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        newxy = (currxy[0]+delta[1], currxy[1]+delta[0])
        if newxy in foundxy:
            continue
        
        newfocus = locsquare[max(0, currloc[0]+TETRAD*delta[0]-TETSPRD):max(0, currloc[0]+TETRAD*delta[0]+TETSPRD),
                             max(0, currloc[1]+TETRAD*delta[1]-TETSPRD):max(0, currloc[1]+TETRAD*delta[1]+TETSPRD)]
        if newfocus.shape[0] and newfocus.shape[1] and np.max(newfocus) > TETTHRESH:
            newloc = np.unravel_index(np.argmax(newfocus), newfocus.shape)
            newloc = (currloc[0]+TETRAD*delta[0]-TETSPRD+newloc[0],
                      currloc[1]+TETRAD*delta[1]-TETSPRD+newloc[1])
            foundxy.append(newxy)
            map_tetris(locsquare, newloc, newxy, foundxy)
    
    return foundxy

def get_cell_objects(vert_centers, horiz_centers, frame, boardData):
    if not (boardData.stars or boardData.squares or boardData.colorsquares or boardData.triangles) or\
        len(vert_centers) != 5 or len(horiz_centers) != 5:
        return []
    
    elts = []
    startemplate = np.load("images/star.npy", "r")
            
    tetris = np.zeros((13, 13))
    tetris[0,:] = 1
    tetris[-1,:] = 1
    tetris[:,0] = 1
    tetris[:,-1] = 1
    
    for x in range(len(horiz_centers)-1):
        for y in range(len(vert_centers)-1):
            square = frame[horiz_centers[y]+6:horiz_centers[y+1]-6, vert_centers[x]+6:vert_centers[x+1]-6]
            if boardData.triangles:
                important = (square[:,:,2] == 255) * 255
            else:
                tolerance = 16
                if boardData.squares:
                    tolerance = 30
                
                if boardData.colorsquares:
                    important = square[:,:,2]
                else:
                    important = square[:,:,0]
                
                # Shade in centers
                if not boardData.triangles and square[important.shape[0]//2, important.shape[1]//2, 2] > 100:
                    important = segmentation.flood_fill(important, (important.shape[0]//2, important.shape[1]//2), 0, tolerance=1)
                
                # Shade out edges
                delta = important.shape[0]//8
                for start in [(delta, delta), (important.shape[0]-delta, delta), (delta, important.shape[1]-delta), (important.shape[0]-delta, important.shape[1]-delta)]:
                    important = segmentation.flood_fill(important, start, 255, tolerance=tolerance)
                important = (important == 255) * 255
            
            if DEBUG >= 2:
                plt.subplot(4, 4, x+1 + y*4),plt.imshow(important, norm=colors.Normalize(0, 255))
            
            if boardData.triangles:
                labels = measurements.label(important)[0]
                
                count = np.max(labels)
                if count > 0:
                    for i in range(1, count+1):
                        if np.count_nonzero(labels == i) < 20:
                            count -= 1
                    elts.append(elements.Triangle(x, y, count))
                continue
            
            if boardData.colorsquares:
                if important[important.shape[0]//2, important.shape[1]//2] == 255:
                    continue
                
                center = square[important.shape[0]//2, important.shape[1]//2, 2]
                if DEBUG >= 3:
                    print(f"Sq {x}, {y}: {center}")
                if center < 110:
                    if square[important.shape[0]//2, important.shape[1]//2, 0] > 110:
                        elts.append(elements.Square(x, y, 'b'))
                    else:
                        elts.append(elements.Square(x, y, 'g'))
                elif center < 220:
                    elts.append(elements.Square(x, y, 'w'))
                continue
            
            if boardData.squares:
                if important[important.shape[0]//2, important.shape[1]//2] == 255:
                    continue
                
                center = square[important.shape[0]//2, important.shape[1]//2, 0]
                if DEBUG >= 3:
                    print(f"Sq {x}, {y}: {center}")
                if center < 100:
                    elts.append(elements.Square(x, y, 'b'))
                elif center < 220:
                    elts.append(elements.Square(x, y, 'w'))
                continue
            
            if boardData.stars:
                star = feature.match_template((important == 255).astype(int), startemplate)
                if DEBUG >= 3:
                    print(f"{x}, {y} star: {np.max(star)}")
                
                if np.max(star) > STARTHRESH:
                    elts.append(elements.Star(x, y))
                    continue
                
                loctetris = feature.match_template((important == 255).astype(int), tetris)
                
                # Do again with a different tolerance because tetrises are finicky
                important = square[:,:,0]
                for start in [(delta, delta), (important.shape[0]-delta, delta), (delta, important.shape[1]-delta), (important.shape[0]-delta, important.shape[1]-delta)]:
                    important = segmentation.flood_fill(important, start, 255, tolerance=10)
                important = (important == 255) * 255
                
                loctetris2 = feature.match_template((important == 255).astype(int), tetris)
                
                if np.max(loctetris) > TETTHRESH or np.max(loctetris2) > TETTHRESH:
                    tetrismap = tetrismap2 = None
                    if np.max(loctetris) > TETTHRESH:
                        tetrismap = map_tetris(loctetris, np.unravel_index(np.argmax(loctetris), loctetris.shape), (0, 0), [(0, 0)])
                    
                    if np.max(loctetris2) > TETTHRESH:
                        tetrismap2 = map_tetris(loctetris2, np.unravel_index(np.argmax(loctetris2), loctetris2.shape), (0, 0), [(0, 0)])
                    if tetrismap is None or (tetrismap2 is not None and len(tetrismap2) > len(tetrismap)):
                        tetrismap = tetrismap2
                        if DEBUG >= 2:
                            plt.subplot(4, 4, x+1 + y*4),plt.imshow(important, norm=colors.Normalize(0, 255))
                    
                    elts.append(elements.Tetris(x, y, tetrismap))
    
    if DEBUG >= 2:
        plt.show()
    return elts

def readBoard(image, boardData):
    frame = image[boardData.region[1]:boardData.region[3], boardData.region[0]:boardData.region[2]]
    
    if boardData.edgeHexes:
        sanitized, hexes = clean_hexes(frame, boardData)
        linemap = get_linemap(sanitized, boardData)
    else:
        linemap = get_linemap(frame, boardData)
    
    horiz_centers = find_centers(linemap, 1, boardData)
    
    vert_centers = find_centers(linemap, 0, boardData)
    
    if DEBUG >= 1:
        print(horiz_centers)
        print(vert_centers)
    if not horiz_centers.shape == vert_centers.shape:
        print(f"WARNING: Unequal shapes {horiz_centers.shape[0]} horizontal, {vert_centers.shape[0]} vertical")
    
    elts = []
    
    if not boardData.colorsquares and not boardData.triangles:
        elts.extend(get_blocks(vert_centers, horiz_centers, linemap))
    
    if boardData.edgeHexes:
        assert(len(hexes) == 2)
        add_edgeHexes(elts, vert_centers, horiz_centers, hexes)
    
    elts.extend(get_cell_objects(vert_centers, horiz_centers, frame, boardData))
    
    elts.extend(get_hexes(frame, linemap, vert_centers, horiz_centers, boardData))
    
    if DEBUG >= 1:
        print(elts)
    if boardData.name == "fsse" and len(vert_centers) == 7:
        b = board.Board(vert_centers+boardData.region[0], horiz_centers+boardData.region[1], elts, [(0, 6), (6, 0)], [(0, 0), (6, 6)], symmetry='rot')
    else:
        b = board.Board(vert_centers+boardData.region[0], horiz_centers+boardData.region[1], elts, [(0, horiz_centers.shape[0]-1)], [(vert_centers.shape[0]-1, 0)])
    return b

def readCylinder(images, boardData):
    CYLHORIZ = list(np.array(data.CYLHORIZ)-boardData.region[1])
    assert(len(images) == 3)
    
    elts = []
    starts = []
    ends = []
    xes = [0] * 6
    centerVert = (boardData.region[2] - boardData.region[0]) / 2
    centerPosGoal = -1
    for iimg, image in enumerate(images):
        frame = image[boardData.region[1]:boardData.region[3], boardData.region[0]:boardData.region[2]]
        
        if boardData.squares:
            findline = segmentation.flood(frame[:,:,2], boardData.startcoords, tolerance=35)
        else:
            findline = frame[:,:,2] > 150
        if DEBUG >= 2:
            plt.imshow(findline, cmap='gray')
            plt.show()
        
        vert_centers = list(find_centers(findline, 0, boardData))
        if DEBUG >= 1:
            print(vert_centers)
        
        centerPos = np.argmin(np.abs(np.array(vert_centers)-centerVert))
        centerVert = vert_centers[centerPos]
        if centerPosGoal == -1:
            centerPosGoal = centerPos
        
        for ix, x in enumerate(vert_centers):
            ix = (2*iimg + ix - centerPos)%6
            if not xes[ix]:
                xes[ix] = x
            
            y = int(math.sqrt((1 - ((x-90)**2) / (150**2)) * 115**2) + 460)
            start = findline[y+10,x]
            end = findline[y+20,x]
            
            if start:
                if end:
                    appendTo = ends
                else:
                    appendTo = starts
                new = (ix, 6)
                if not new in appendTo:
                    appendTo.append(new)
            
            y = int(-1 * math.sqrt((1 - ((x-90)**2) / (150**2)) * 115**2) + 156)
            start = findline[y-10,x]
            end = findline[y-20,x]
            
            if start:
                if end:
                    appendTo = ends
                else:
                    appendTo = starts
                new = (ix, 0)
                if not new in appendTo:
                    appendTo.append(new)
        
        if boardData.squares:
            if len(vert_centers) == 2:
                if centerPos == 0:
                    vert_centers.insert(0, max(vert_centers[0]-75, vert_centers[0] * -1 + 20))
                else:
                    vert_centers.append(min(vert_centers[1]+75, 2*(boardData.region[2] - boardData.region[0]) - vert_centers[1] - 20))
            else:
                assert(centerPos==1)
                
            if DEBUG >= 1:
                print(vert_centers)
            
            for iy in range(len(CYLHORIZ)-1):
                y = (CYLHORIZ[iy] + CYLHORIZ[iy+1])//2
                for ix in range(len(vert_centers)-1):
                    x = (vert_centers[ix] + vert_centers[ix+1])//2
                    cellx = (iimg * 2 + ix  - 1)%6
                    
                    red = frame[y,x,2]
                    if red < 60:
                        elts.append(elements.Square(cellx, iy, 'b'))
                    if red > 200:
                        elts.append(elements.Square(cellx, iy, 'w'))
                    if DEBUG >= 3:
                        print(f"sq@{ix},{iy}: {red}")
                    
        if boardData.edgeHexes:
            for iy in range(6):
                for ix in range(len(vert_centers)):
                    linex = (2*iimg + ix - centerPos)%6
                    value = np.min(frame[CYLHORIZ[iy]:CYLHORIZ[iy+1],vert_centers[ix],2])
                    if DEBUG >= 3:
                        print(f"hex@{ix},{iy}:: {value}")
                    if value < 75:
                        new = elements.EdgeHex(linex, iy, linex, iy + 1)
                        if not new in elts:
                            elts.append(new)
            
            if len(vert_centers) == 2:
                if centerPos == 0:
                    vert_centers.insert(0, 8)
                else:
                    vert_centers.append(boardData.region[2] - boardData.region[0] - 8)
            else:
                assert(centerPos==1)
            
            for iy in range(7):
                for ix in range(len(vert_centers) - 1):
                    linex = (2*iimg + ix - 1)%6
                    value = np.min(frame[CYLHORIZ[iy],vert_centers[ix]:vert_centers[ix+1],2])
                    if DEBUG >= 3:
                        print(f"hex@{ix}:,{iy}: {value}")
                    if value < 75:
                        new = elements.EdgeHex(linex, iy, (linex + 1)%6, iy)
                        if not new in elts:
                            elts.append(new)

    if DEBUG >= 3:
        print(f"starts:{starts}")
        print(f"ends:{ends}")
    
    assert(len(starts) == 2)
    assert(len(ends) == 2)
    xdiff = (starts[0][0] - starts[1][0])%6
    if starts[0][1] == 0 or starts[1][1] == 0:
        if starts[0][1] == 0:
            starts.reverse()
        if xdiff == 1 or xdiff == 5:
            symmetry = 'rot'
        else:
            symmetry = 'rotparallel'
    
    elif xdiff == 1 or xdiff == 5:
        symmetry = 'mirror'
        if xdiff == 5:
            starts.reverse()
    else:
        assert(xdiff == 3)
        symmetry = 'parallel'
    
    if not starts[0][0] == 0:
        subx = starts[0][0]
        starts[0] = (0, starts[0][1])
        starts[1] = ((starts[1][0]-subx)%6, starts[1][1])
        ends[0] = ((ends[0][0]-subx)%6, ends[0][1])
        ends[1] = ((ends[1][0]-subx)%6, ends[1][1])
        for elt in elts:
            elt.x = (elt.x - subx)%6
            if hasattr(elt, "x2"):
                elt.x2 = (elt.x2 - subx)%6
        xes = xes[subx:] + xes[:subx]

    if DEBUG >= 3:
        print(f"starts:{starts}")
        print(f"ends:{ends}")
            
    if DEBUG >= 1:
        print(elts)
    
    return board.Board(xes, data.CYLHORIZ, elts, starts, ends, symmetry=symmetry, cylinder=True)















