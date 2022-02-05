#!/usr/bin/env python3

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors
from skimage import segmentation
from skimage import feature
import board, elements

DEBUG = 0

BASETHRESHOLD = 40
BLACKTHRESHOLD = 20
BOARDERTHRESHOLD = 30
STARTHRESH = 0.7
SQUARETHRESH = 0.75
HEXTHRESH = 15

MINSPREAD = 5
BDJ = 8 #Block Delta maJor
BDN = 2 #Block Delta miNor
BLOCKTHRESHOLD = 0.95

TETRAD = 13
TETSPRD = 3
TETTHRESH = 0.6


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
    
    if DEBUG >= 2:
        plt.imshow(clipped, cmap='gray')
        plt.show()
        #plt.imshow((res > 100), cmap='gray')
        #plt.show()
    
    arr = np.sum(clipped, dim)
    arr = np.greater(arr, 15)
    arr = np.diff(arr.astype(int))
    starts = np.argwhere(arr==1)
    ends = np.argwhere(arr==-1)
    ret = np.concatenate((starts, ends), 1)
    ret = ret[ret[:,1]-ret[:,0] > MINSPREAD]
    return np.average(ret, 1).astype(int) + 2**(min(shape)-1)
    

def get_linemap(image, boardData):
    #image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    if boardData.name == "four":
        findline = segmentation.flood(image, boardData.startcoords, tolerance=20)
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
    while max_val > 0.9:
        locs.append((max_loc[1]+7, max_loc[0]+7))
        
        if DEBUG >= 3:
            demo = np.copy(image)
            demo[locs[-1][0],:] = 0
            demo[:,locs[-1][1]] = 0
            plt.imshow(demo)
            plt.show()
            
        image = segmentation.flood_fill(image, locs[-1], image[boardData.startcoords], tolerance=30)
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
                if DEBUG >= 2:
                    linemap[transy-BDN-dn:transy+BDN+dn, centerx-BDJ:centerx+BDJ] += 0.5
            elif DEBUG >= 2:
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
                if DEBUG >= 2:
                    linemap[centery-BDJ:centery+BDJ, transx-BDN-dn:transx+BDN+dn] += 0.5
            elif DEBUG >= 2:
                linemap[centery-BDJ:centery+BDJ, transx-BDN-dn:transx+BDN+dn] -= 0.5
    
    if DEBUG >= 2:
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
        if np.min(diff) < 3:
            iy = np.argmin(diff)
            ix = np.sum((vert_centers - x) < 0)
            
            target = elements.Block(ix, iy, ix-1, iy)
            for e in elts:
                if e == target:
                    elts.remove(e)
                    
            elts.append(elements.EdgeHex(ix, iy, ix-1, iy))
            
        else:
            diff = np.abs(vert_centers-x)
            assert(np.min(diff) < 3)
            ix = np.argmin(diff)
            iy = np.sum((horiz_centers - y) < 0)
            
            target = elements.Block(ix, iy, ix, iy-1)
            for e in elts:
                if e == target:
                    elts.remove(e)
                    
            elts.append(elements.EdgeHex(ix, iy, ix, iy-1))

def get_hexes(image, linemap, vert_centers, horiz_centers, boardData):
    if not boardData.hexes or (len(vert_centers) != 5 and len(vert_centers) != 7):
        return []
    
    if len(vert_centers) == 7:
        image2 = cv.cvtColor(image, cv.COLOR_BGR2HSV)[:,:,2]
        delta = 13
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
                if edge > center and edge - center > HEXTHRESH:
                    elts.append(elements.Hex(ix, iy))
                if len(vert_centers) == 7 and center > edge and center - edge > 80:
                    if image[coords][1] > image[y,x,0]:
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
    if not (boardData.stars or boardData.squares) or len(vert_centers) != 5:
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
            important = frame[vert_centers[y]+6:vert_centers[y+1]-6, horiz_centers[x]+6:horiz_centers[x+1]-6][:,:,0]
            tolerance = 12
            if boardData.squares:
                tolerance = 25
            for start in [(10, 10), (-10, 10), (10, -10), (-10, -10)]:
                important = segmentation.flood_fill(important, start, 255, tolerance=tolerance)
            
            if DEBUG >= 2:
                plt.subplot(4, 4, x+1 + y*4),plt.imshow(important, norm=colors.Normalize(0, 255))
            
            if boardData.squares:
                center = important[important.shape[0]//2, important.shape[1]//2]
                if DEBUG >= 3:
                    print(f"Sq {x}, {y}: {center}")
                if center < 20:
                    elts.append(elements.Square(x, y, 'b'))
                elif center < 200:
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
                if np.max(loctetris) > TETTHRESH:
                    tetrismap = map_tetris(loctetris, np.unravel_index(np.argmax(loctetris), loctetris.shape), (0, 0), [(0, 0)])
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
