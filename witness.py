#!/usr/bin/env python3

import time, math, os, mss, traceback
import pydirectinput as guilib
import read, data
import numpy as np
import cv2 as cv
from skimage import transform
from matplotlib import pyplot as plt

#REGION = (1680, 0, 1920, 1080) #Game window region
REGION = (0, 0, 1920, 1080) #Game window region
FOURREGION = (600, 400, 700, 350)
NINECREGION = (830, 380, 1080, 600)
NINELREGION = (250, 410, 460, 610)
NINERREGION = (1520, 290, 1730, 500)
TENCREGION = (800, 485, 940, 615)
TENLREGION = (255, 520, 420, 680)
TENRREGION = (1320, 440, 1500, 610)

SENS = (1, 1)
SENS3D = (1, 1)
FOV = 100 * math.pi / 180
MONITOR = 1

DEBUG = 0

sct = mss.mss()

# Override pydirectinput's method to allow for inputting floats
def f(x=0, y=0):
    display_width, display_height = guilib.size()
    
    windows_x = int((x * 65536) // display_width) + 1
    windows_y = int((y * 65536) // display_height) + 1
    
    return windows_x, windows_y

guilib._to_windows_coordinates = f
guilib.PAUSE = 0.02

class WitnessGUI:
    def __init__(self, walking = True):
        self.CENTER = (sct.monitors[MONITOR]["width"]//2, sct.monitors[MONITOR]["height"]//2)
        self.mousecoords = self.CENTER
        self.clicked = False
        self.clickedsens = 1
        self.walking = walking
        self.nexttime = 0
    
    def startstop_solve(self):
        guilib.press("space")
        self.walking = not self.walking
        if not self.walking:
            self.mousecoords = self.CENTER
    
    def click(self):
        assert(not self.walking)
        guilib.click(None, None)
        self.clicked = not self.clicked
    
    def moveBy(self, x, y):
        if self.walking:
            sens = SENS3D
        else:
            sens = SENS
            if self.clicked:
                sens = (sens[0] * self.clickedsens, sens[1] * self.clickedsens)
        
        adjx = x * sens[0]
        adjx = adjx if adjx else 0.001
        adjy = y * sens[1]
        adjy = adjy if adjy else 0.001
        # I don't know why this works, but it does
        guilib.moveTo(adjx, adjy)
        self.mousecoords = (self.mousecoords[0] + x, self.mousecoords[1] + y)
    
    def moveTo(self, x, y):
        if self.walking:
            self.moveBy(x-self.CENTER[0], y-self.CENTER[1])
        else:
            self.moveBy(x-self.mousecoords[0], y-self.mousecoords[1])
            self.mousecoords = (x, y)
    
    def schedule(self, t):
        self.nexttime = time.time() + t
    
    def execute(self):
        t = self.nexttime - time.time()
        if t > 0:
            time.sleep(t)
        else:
            print(f"WARN: time exceeded by {-1*t}")

def get_screenshot(region=None):
    arr = np.array(sct.grab(sct.monitors[MONITOR]))[:,:,:3]
    if region:
        return arr[region[1]:region[1]+region[3], region[0]:region[0]+region[2]]
    return arr

def solveBoard(boardData, gui, i=""):
    image = get_screenshot()
    cv.imwrite(f"{boardData.name}{i}.png", image)
    
    b = read.readBoard(image, boardData)
    
    if not b.solve():
        raise Exception("No solution found")
    print(b)
    
    coords = b.getSlnCoords()
    
    if boardData == data.FSSE:
        if b.width == 7:
            gui.clickedsens = boardData.clickedsens[0]
        elif b.width == 4:
            gui.clickedsens = boardData.clickedsens[1]
        else:
            gui.clickedsens = boardData.clickedsens[2]
    
    else:
        gui.clickedsens = boardData.clickedsens
    
    gui.moveTo(*coords[0])
    gui.click()
    
    for c in coords[1:]:
        gui.moveTo(*c)
    gui.click()

def warpBoard4(image):
    flooded = (image[:,:,2] > 105) & (image[:,:,2] < 115) & (image[:,:,1] > 80) & (image[:,:,1] < 85)
    if DEBUG:
        plt.imshow(flooded)
        plt.show()
    locs = np.argwhere(flooded)[:,::-1]
    
    summed = locs[:,0] + locs[:,1]*2
    tl = locs[np.argmin(summed)] + np.array([0, -5])
    br = locs[np.argmax(summed)] + np.array([0, 10])
    summed = locs[:,0]*2 - locs[:,1]
    bl = locs[np.argmin(summed)] + np.array([-23, 5])
    tr = locs[np.argmax(summed)] + np.array([5, -7])
    
    src = np.array([tr, br, tl, bl])
    dest = np.array([[0, 0], [350, 0], [0, 275], [350, 275]])
    
    warpfn = transform.ProjectiveTransform()
    warpfn.estimate(dest, src)
    image = transform.warp(image, warpfn, output_shape=(275, 350))
    image = (image*255).astype(np.uint8)
    if DEBUG >= 1:
        plt.imshow(image)
        plt.show()
    return image, warpfn

def solveBoard4(gui):
    image = get_screenshot(FOURREGION)
    cv.imwrite("four.png", image)
    image, warpfn = warpBoard4(image)
    
    gui.startstop_solve()
    b = read.readBoard(image, data.FOUR)
    
    if not b.solve():
        raise Exception("No solution found")
    print(b)
    
    coords = b.getSlnCoords()
    
    gui.clickedsens = data.FOUR.clickedsens
    gui.moveTo(FOURREGION[0] + warpfn(coords[0])[0][0], FOURREGION[1] + warpfn(coords[0])[0][1])
    gui.click()
    
    for c in coords[1:]:
        gui.moveTo(FOURREGION[0] + warpfn(c)[0][0], FOURREGION[1] + warpfn(c)[0][1])
    gui.click()

def waitForPuzzle(x, y, x2, y2):
    loaded = False
    while not loaded:
        image = get_screenshot((x, y, x2-x, y2-y))
        blue = np.average(image[:,:,0])
        green = np.average(image[:,:,1])
        red = np.average(image[:,:,2])
        loaded = red < 60 and green > 85 and blue < green * 0.92 and blue > green * 0.5

def detectPuzzle(x, y, x2, y2, easy = False, image = None):
    if not image:
        image = get_screenshot()
    if DEBUG == 2:
        plt.imshow(image)
        plt.show()
    
    image = image[y:y2,x:x2]
    if DEBUG >= 1:
        plt.imshow(image)
        plt.show()
    if easy:
        image = (image[:,:,1] > 80) & (image[:,:,2] < 70)
    else:
        image = (image[:,:,1] > 140) & (image[:,:,2] < 100)
    if DEBUG == 3:
        plt.imshow(image)
        plt.show()
    return np.any(image)

def findimage(template, image=None):
    if image is None:
        image = get_screenshot()
    res = cv.matchTemplate(image, template, cv.TM_CCOEFF)
    _, maxval, _, maxloc = cv.minMaxLoc(res)
    if DEBUG:
        image[maxloc[1], :, :] = 255
        image[:, maxloc[0], :] = 255
        plt.imshow(image)
        plt.show()
    return maxloc

def calibrate(gui):
    global SENS3D, SENS
    SENS3D = (1, 1)
    SENS = (1, 1)
    
    if os.path.exists("sensitivity.txt"):
        f = open("sensitivity.txt", 'r')
        s = f.readline().split(' ')
        SENS3D = (float(s[0]), float(s[1]))
        s = f.readline().split(' ')
        SENS = (float(s[0]), float(s[1]))
        f.close()
        return
    
    music = cv.imread('images/record.png')
    maxloc = findimage(music)
    
    gui.moveBy(1, 1)
    maxloc2 = findimage(music)
    SENS3D = (1 / (maxloc[0] - maxloc2[0]), 1 / (maxloc[1] - maxloc2[1]))
    
    print(SENS3D)
    if SENS3D[0] < 0 or SENS3D[1] < 0:
        raise Exception("Error while calibrating sensitivity. Please turn down in-game sensitivity or calibrate manually")
    
    # Recalibrate x to be more presise
    for _ in range(3):
        gui.moveTo(maxloc2[0], maxloc2[1])
        maxloc = findimage(music)
        gui.moveBy(5200, 0)
        maxloc2 = findimage(music)
        SENS3D = (SENS3D[0] * 5200 / (maxloc[0] - maxloc2[0] + 5200), SENS3D[1])
        
        print(SENS3D)
        if SENS3D[0] < 0 or SENS3D[1] < 0:
            raise Exception("Error while calibrating sensitivity. Please turn down in-game sensitivity or calibrate manually")
        
    gui.moveTo(maxloc2[0] - 1200, maxloc2[1] - 400)
    gui.startstop_solve()
    time.sleep(1)
    
    cursor = cv.imread('images/cursor.png')
    maxloc = findimage(cursor)
    gui.moveBy(7, 3)
    maxloc2 = findimage(cursor)
    SENS = (7 / (maxloc2[0] - maxloc[0]), 3 / (maxloc2[1] - maxloc[1]))
    
    print(SENS)
    if SENS[0] < 0 or SENS[1] < 0:
        raise Exception("Error while calibrating sensitivity. Please turn down in-game sensitivity or calibrate manually")
    
    gui.startstop_solve()
    gui.moveBy(1200, 400)
    
    f = open("sensitivity.txt", 'w')
    f.write(f"{SENS3D[0]} {SENS3D[1]}\n{SENS[0]} {SENS[1]}")
    f.close()

def navigateFSSE(current, solved, gui):
    if current == 'start':
        gui.moveBy(1900, -300)
        guilib.keyDown('w')
        time.sleep(2)
        guilib.keyDown('a')
        guilib.keyUp('w')
        gui.schedule(0.4)
        front = detectPuzzle(600, 0, 1000, 200)
        gui.execute()
        
        if front:
            time.sleep(0.6)
            gui.moveBy(700, 0)
            guilib.keyUp('a')
            guilib.keyDown('w')
            time.sleep(1)
            guilib.keyUp('w')
            gui.startstop_solve()
            return 'front'
        
        guilib.keyUp('a')
        guilib.keyDown('d')
        gui.schedule(0.3)
        under = detectPuzzle(1000, 450, 1300, 650)
        gui.execute()
        
        if under:
            guilib.keyUp('d')
            gui.moveBy(-200, 0)
            guilib.keyDown('w')
            time.sleep(1)
            gui.moveBy(1400, 0)
            guilib.keyUp('w')
            gui.startstop_solve()
            return 'under'
        
        gui.moveBy(-300, 0)
        time.sleep(0.3)
        gui.moveBy(-500, 0)
        time.sleep(0.4)
        guilib.keyUp('d')
        gui.schedule(0.15)
        back = detectPuzzle(1000, 200, 1200, 500)
        gui.execute()
        
        if back:
            gui.moveBy(400, 0)
            guilib.keyDown('w')
            time.sleep(0.6)
            guilib.keyUp('w')
            gui.moveBy(-1400, 0)
            gui.startstop_solve()
            return 'back'
        
        guilib.keyDown('a')
        time.sleep(0.8)
        gui.moveBy(500, 0)
        guilib.keyUp('a')
        guilib.keyDown('w')
        time.sleep(1.5)
        gui.moveBy(800, 0)
        time.sleep(0.4)
        gui.moveBy(1500, 0)
        time.sleep(0.2)
        guilib.keyUp('w')
        gui.startstop_solve()
        return 'behind'
    
    ###########################################################################
    if current == 'front':
        if solved['behind'] and solved['under']:
            guilib.keyDown('a')
            time.sleep(0.7)
            guilib.keyDown('w')
            time.sleep(0.3)
            guilib.keyUp('a')
            time.sleep(0.3)
            gui.moveBy(1300, 0)
            time.sleep(0.6)
            gui.moveBy(1200, 0)
            gui.startstop_solve()
            guilib.keyUp('w')
            return 'back'
            
        guilib.keyDown('s')
        time.sleep(0.9)
        guilib.keyUp('s')
        guilib.keyDown('a')
        time.sleep(0.7)
        guilib.keyUp('a')
        guilib.keyDown('w')
        gui.schedule(0.65)
        under = not solved['under'] and detectPuzzle(1400, 500, 1650, 600)
        gui.execute()
        
        if under:
            guilib.keyDown('d')
            guilib.keyUp('w')
            time.sleep(0.5)
            gui.startstop_solve()
            guilib.keyUp('d')
            return 'under'
        
        if not solved['behind']:
            time.sleep(0.35)
            guilib.keyUp('w')
            gui.moveBy(1200, 0)
            gui.schedule(0.1)
            behind = detectPuzzle(600, 400, 900, 700)
            gui.execute()
            
            if behind:
                guilib.keyDown('w')
                time.sleep(0.3)
                guilib.keyUp('w')
                gui.startstop_solve()
                return 'behind'
        
            guilib.keyDown('d')
            guilib.keyDown('s')
            time.sleep(0.3)
            guilib.keyUp('s')
            time.sleep(0.2)
            guilib.keyUp('d')
            gui.moveBy(150, 0)
            guilib.keyDown('w')
            time.sleep(0.1)
        else:
            gui.moveBy(1250, 0)
        
        time.sleep(1.4)
        gui.moveBy(-1400, 0)
        time.sleep(0.6)
        gui.moveBy(-1400, 0)
        time.sleep(0.4)
        guilib.keyUp('w')
        gui.moveBy(-1400, 0)
        gui.startstop_solve()
        return 'back'
    
    ###########################################################################
    if current == 'back':
        guilib.keyDown('a')
        time.sleep(1)
        gui.moveBy(1600, -200)
        time.sleep(0.5)
        gui.schedule(0.2)
        front = not solved['front'] and detectPuzzle(900, 50, 1150, 200)
        gui.execute()
        
        if front:
            guilib.keyDown('s')
            guilib.keyUp('a')
            time.sleep(0.2)
            guilib.keyDown('a')
            guilib.keyUp('s')
            time.sleep(0.5)
            gui.moveBy(800, 0)
            guilib.keyDown('w')
            time.sleep(0.3)
            guilib.keyUp('a')
            time.sleep(0.6)
            guilib.keyUp('w')
            gui.startstop_solve()
            return 'front'
        
        guilib.keyUp('a')
        guilib.keyDown('w')
        gui.schedule(0.6)
        under = not solved['under'] and detectPuzzle(1100, 650, 1500, 900)
        gui.execute()
        
        if under:
            gui.moveBy(1400, 200)
            guilib.keyUp('w')
            gui.startstop_solve()
            return 'under'
        
        time.sleep(0.8)
        gui.moveBy(1100, 200)
        time.sleep(0.4)
        gui.moveBy(1400, 0)
        time.sleep(0.3)
        guilib.keyUp('w')
        gui.startstop_solve()
        return 'behind'
        
    ###########################################################################
    if current == 'behind':
        guilib.keyDown('s')
        time.sleep(0.4)
        guilib.keyUp('s')
        guilib.keyDown('d')
        time.sleep(0.6)
        gui.schedule(0.1)
        under = not solved['under'] and detectPuzzle(500, 300, 1000, 600, True)
        gui.execute()
        
        if under:
            guilib.keyUp('d')
            guilib.keyDown('w')
            gui.moveBy(-300, 0)
            time.sleep(0.5)
            gui.moveBy(-1200, 0)
            gui.startstop_solve()
            guilib.keyUp('w')
            return 'under'
        
        time.sleep(0.4)
        guilib.keyUp('d')
        guilib.keyDown('w')
        time.sleep(0.5)
        gui.moveBy(-1300, -200)
        gui.schedule(0.1)
        front = not solved['front'] and detectPuzzle(1000, 300, 1500, 500)
        gui.execute()
        
        if front:
            gui.moveBy(300, 200)
            time.sleep(0.3)
            guilib.keyUp('w')
            gui.startstop_solve()
            return 'front'
        
        time.sleep(0.3)
        guilib.keyDown('a')
        time.sleep(0.6)
        guilib.keyUp('a')
        gui.moveBy(400, 200)
        time.sleep(0.2)
        gui.moveBy(1000, 0)
        time.sleep(0.5)
        gui.moveBy(1400, 0)
        gui.startstop_solve()
        guilib.keyUp('w')
        return 'back'
    
    ###########################################################################
    if current == 'under':
        guilib.keyDown('s')
        time.sleep(0.3)
        guilib.keyUp('s')
        guilib.keyDown('a')
        time.sleep(0.5)
        
        if not solved['behind']:
            time.sleep(0.2)
            guilib.keyUp('a')
            guilib.keyDown('w')
            time.sleep(0.2)
            guilib.keyUp('w')
            gui.moveBy(1000, 0)
            gui.schedule(0.1)
            behind = detectPuzzle(500, 450, 1000, 750)
            gui.execute()
            
            if behind:
                guilib.keyDown('w')
                time.sleep(0.2)
                guilib.keyUp('w')
                gui.startstop_solve()
                return 'behind'
            
            gui.moveBy(-1000, 0)
            guilib.keyDown('s')
            time.sleep(0.5)
            guilib.keyUp('s')
            guilib.keyDown('d')
            time.sleep(0.1)
            guilib.keyUp('d')
        
        guilib.keyDown('s')
        guilib.keyUp('a')
        time.sleep(0.5)
        guilib.keyUp('s')
        guilib.keyDown('d')
        time.sleep(0.45)
        guilib.keyUp('d')
        guilib.keyDown('w')
        gui.schedule(0.1)
        front = not solved['front'] and detectPuzzle(900, 200, 1300, 400)
        gui.execute()
        
        if front:
            gui.moveBy(200, 0)
            time.sleep(0.5)
            gui.startstop_solve()
            guilib.keyUp('w')
            return 'front'
        
        time.sleep(0.15)
        gui.moveBy(-700, 0)
        time.sleep(0.5)
        gui.moveBy(700, 0)
        time.sleep(0.5)
        gui.moveBy(1400, 0)
        time.sleep(0.5)
        gui.moveBy(1200, 0)
        gui.startstop_solve()
        guilib.keyUp('w')
        return 'back'

def walkToNine(current, gui):
    if current == 'behind':
        gui.moveBy(-2350, 0)
        guilib.keyDown('w')
        time.sleep(1.4)
        gui.moveBy(-1350, 0)
        time.sleep(0.75)
        guilib.keyUp('w')
    
    elif current == 'under':
        gui.moveBy(-1400, 0)
        guilib.keyDown('a')
        guilib.keyDown('w')
        time.sleep(0.2)
        guilib.keyUp('a')
        time.sleep(0.6)
        gui.moveBy(800, 0)
        time.sleep(1)
        gui.moveBy(-1200, 0)
        time.sleep(0.4)
        gui.moveBy(-800, 0)
        time.sleep(0.7)
        guilib.keyUp('w')
    
    elif current == 'front':
        guilib.keyDown('s')
        time.sleep(0.9)
        guilib.keyUp('s')
        guilib.keyDown('a')
        time.sleep(0.7)
        guilib.keyUp('a')
        guilib.keyDown('w')
        time.sleep(0.7)
        gui.moveBy(-300, 0)
        time.sleep(1)
        gui.moveBy(-1200, 0)
        time.sleep(0.5)
        gui.moveBy(-900, 0)
        time.sleep(0.7)
        guilib.keyUp('w')
    
    elif current == 'back':
        guilib.keyDown('a')
        time.sleep(1)
        guilib.keyDown('w')
        guilib.keyUp('a')
        time.sleep(0.4)
        gui.moveBy(1300, 0)
        time.sleep(1.3)
        gui.moveBy(800, 0)
        time.sleep(1.2)
        gui.moveBy(-1000, 0)
        time.sleep(0.3)
        gui.moveBy(-850, 0)
        time.sleep(0.6)
        guilib.keyUp('w')
        
    guilib.keyDown('w')
    time.sleep(0.3)
    guilib.keyUp('w')
    gui.startstop_solve()
    time.sleep(0.5)
    gui.startstop_solve()
    guilib.keyDown('s')
    time.sleep(0.4)
    guilib.keyUp('s')
    time.sleep(0.4)

def resize(image, x, y, x2, y2):
    image = image[y:y2,x:x2]
    board = (image[:,:,1] > 90) & (image[:,:,2] < 40)
    if DEBUG:
        plt.imshow(board)
        plt.show()
    locs = np.argwhere(board)[:,::-1]
    
# =============================================================================
#     maxx = np.max(locs[:,0])
#     minx = np.min(locs[:,0])
#     maxy = np.max(locs[:,1])
#     miny = np.min(locs[:,1])
#     tl = [minx, miny]
#     br = [maxx, maxy]
#     bl = [minx, maxy]
#     tr = [maxx, miny]
# =============================================================================

    summed = locs[:,0] + locs[:,1]
    tl = locs[np.argmin(summed)]
    br = locs[np.argmax(summed)]
    summed = locs[:,0] - locs[:,1]
    bl = locs[np.argmin(summed)]
    tr = locs[np.argmax(summed)]
    
    src = np.array([tr, br, tl, bl])
    dest = np.array([[200, 0], [200, 200], [0, 0], [0, 200]])
    
    warpfn = transform.ProjectiveTransform()
    warpfn.estimate(dest, src)
    image = transform.warp(image, warpfn, output_shape=(200, 200))
    image = (image*255).astype(np.uint8)
    if DEBUG >= 1:
        plt.imshow(image)
        plt.show()
    return image, warpfn

def solveNine(gui):
    print("Trying center")
    image = get_screenshot()
    cv.imwrite("ninec.png", image)
    region = NINECREGION
    warped, warpfn = resize(image, *region)
    b = read.readBoard(warped, data.NINE)
    gui.clickedsens = data.NINE.clickedsens[1]
    
    if not b.solve():
        print("Trying left")
        # Make sure left is visible
        region = NINELREGION
        waitForPuzzle(region[0]+20, region[1]+20, region[2]-20, region[3]-20)
        # Make sure it's close to full brightness
        #time.sleep(0.5)
        image = get_screenshot()
        cv.imwrite("ninel.png", image)
        warped, warpfn = resize(image, *region)
        b = read.readBoard(warped, data.NINE)
        gui.clickedsens = data.NINE.clickedsens[0]
        
        if not b.solve():
            print("Trying right")
            region = NINERREGION
            waitForPuzzle(region[0]+20, region[1]+20, region[2]-20, region[3]-20)
            #time.sleep(0.5)
            image = get_screenshot()
            cv.imwrite("niner.png", image)
            warped, warpfn = resize(image, *region)
            b = read.readBoard(warped, data.NINE)
            assert(b.solve())
            gui.clickedsens = data.NINE.clickedsens[2]
    
    print(b)
    gui.startstop_solve()
    coords = b.getSlnCoords()
    
    gui.moveTo(region[0] + warpfn(coords[0])[0][0], region[1] + warpfn(coords[0])[0][1])
    gui.click()
    
    for c in coords[1:]:
        gui.moveTo(region[0] + warpfn(c)[0][0], region[1] + warpfn(c)[0][1])
    gui.click()
    gui.startstop_solve()

def solveTen(gui):
    print("Trying center")
    region = TENCREGION
    waitForPuzzle(region[0]+20, region[1]+20, region[2]-20, region[3]-20)
    image = get_screenshot()
    cv.imwrite("tenc.png", image)
    warped, warpfn = resize(image, *region)
    b = read.readBoard(warped, data.TEN)
    gui.clickedsens = data.TEN.clickedsens[1]
    
    if not b.solve():
        print("Trying right")
        region = TENRREGION
        waitForPuzzle(region[0]+20, region[1]+20, region[2]-20, region[3]-20)
        #time.sleep(0.2)
        image = get_screenshot()
        cv.imwrite("tenr.png", image)
        warped, warpfn = resize(image, *region)
        b = read.readBoard(warped, data.TEN)
        gui.clickedsens = data.TEN.clickedsens[2]
        
        if not b.solve():
            print("Trying left")
            # Make sure left is visible
            region = TENLREGION
            waitForPuzzle(region[0]+20, region[1]+20, region[2]-20, region[3]-20)
            # Make sure it's close to full brightness
            #time.sleep(0.2)
            image = get_screenshot()
            cv.imwrite("tenl.png", image)
            warped, warpfn = resize(image, *region)
            b = read.readBoard(warped, data.TEN)
            gui.clickedsens = data.TEN.clickedsens[0]
            assert(b.solve())
    
    print(b)
    gui.startstop_solve()
    coords = b.getSlnCoords()
    
    gui.moveTo(region[0] + warpfn(coords[0])[0][0], region[1] + warpfn(coords[0])[0][1])
    gui.click()
    
    for c in coords[1:]:
        gui.moveTo(region[0] + warpfn(c)[0][0], region[1] + warpfn(c)[0][1])
    gui.click()
    gui.startstop_solve()

def main():
    escape = cv.imread('images/escape.png')
    music = cv.imread('images/record.png')
    music2 = cv.imread('images/recordc.png')
    
    time.sleep(3)
    
    # Look for the escape screen
    ready = False
    while not ready:
        image = get_screenshot()
        res = cv.matchTemplate(image, escape, cv.TM_SQDIFF_NORMED)
        print(np.min(res))
        if np.min(res) < 0.05:
            ready = True
    guilib.press("escape")
    time.sleep(0.5)
    
    gui = WitnessGUI(True)
    guilib.keyUp('shift')
    guilib.keyDown('shift')
    calibrate(gui)
    
    while True:
        # Look for the music box
        maxloc = findimage(music)
        gui.moveTo(maxloc[0] - 100, maxloc[1] + 300)
        
        # Walk to the music box
        guilib.keyDown('w')
        time.sleep(1)
        guilib.keyUp('w')
        
        # Solve the music box
        gui.startstop_solve()
        time.sleep(0.3)
        
        maxloc = findimage(music2)
        gui.moveTo(maxloc[0]+10, maxloc[1]+10)
        
        gui.click()
        gui.moveBy(-100, 0)
        gui.moveBy(0, 50)
        gui.click()
        gui.startstop_solve()
        
        # Walk to puzzle one
        gui.moveBy(-80, -200)
        guilib.keyDown('w')
        time.sleep(2.1)
        guilib.keyUp('w')
        
        gui.startstop_solve()
        
        # Solve puzzles 1-3
        waitForPuzzle(775, 350, 1130, 710)
        
        gui = WitnessGUI(False)
        solveBoard(data.ONE, gui)
        
        guilib.press('d')
        time.sleep(0.4)
        
        solveBoard(data.TWO, gui)
        
        guilib.press('d')
        time.sleep(0.4)
        
        solveBoard(data.THREE, gui)
        gui.startstop_solve()
        
        # Go to 4
        guilib.keyDown('d')
        time.sleep(0.1)
        guilib.keyDown('w')
        time.sleep(0.7)
        guilib.keyUp('d')
        time.sleep(0.68)
        guilib.keyUp('w')
        gui.moveBy(-1250, 250)
        
        time.sleep(0.5)
        solveBoard4(gui)
        gui.startstop_solve()
        
        # Go through FSSE
        try:
            current = 'start'
            solved = {'front': False, 'back': False, 'under': False, 'behind': False}
            
            for i in range(4):
                current = navigateFSSE(current, solved, gui)
                assert(not solved[current])
                time.sleep(0.9)
                solveBoard(data.FSSE, gui, i)
                gui.startstop_solve()
                solved[current] = True
        
        except Exception:
            traceback.print_exc()
            print("Pausing for 60 seconds, just for fun")
            time.sleep(60)
            print("Pausing for 10 more seconds")
            time.sleep(10)
        
            if not gui.walking:
                gui.startstop_solve()
            walkToNine(current, gui)
            
            # Walk to the start from Ten
            print("Recovering from failure")
            guilib.keyDown('w')
            time.sleep(0.5)
            guilib.keyUp('w')
            gui.startstop_solve()
            time.sleep(1)
            gui.startstop_solve()
            gui.moveBy(-2700, 0)
            guilib.keyDown('w')
            time.sleep(1.2)
            gui.moveBy(800, 0)
            time.sleep(0.4)
            gui.moveBy(1100, 0)
            time.sleep(1)
            gui.moveBy(-700, 0)
            time.sleep(2)
            gui.moveBy(400, 0)
            time.sleep(1.2)
            gui.moveBy(-800, 0)
            time.sleep(1.1)
            gui.moveBy(600, 0)
            time.sleep(2)
            gui.moveBy(-300, 0)
            time.sleep(2)
            guilib.keyUp('w')
            gui.moveBy(-2400, 0)
            guilib.press('escape')
            time.sleep(0.5)
            guilib.press('escape')
            time.sleep(2)
        
        walkToNine(current, gui)
        
        # Solve Nine
        solveNine(gui)
        
        guilib.keyDown('w')
        guilib.keyDown('a')
        time.sleep(0.4)
        guilib.keyUp('a')
        time.sleep(0.3)
        guilib.keyDown('d')
        time.sleep(0.1)
        guilib.keyUp('d')
        guilib.keyUp('w')
        time.sleep(0.3)
        
        solveTen(gui)
        
        # Walk to the start from Ten
        guilib.keyDown('w')
        time.sleep(0.7)
        guilib.keyUp('w')
        gui.startstop_solve()
        time.sleep(1)
        gui.startstop_solve()
        gui.moveBy(-2700, 0)
        guilib.keyDown('w')
        guilib.keyDown('d')
        time.sleep(0.4)
        guilib.keyUp('d')
        time.sleep(0.7)
        guilib.keyDown('a')
        time.sleep(0.15)
        guilib.keyUp('a')
        time.sleep(1)
        gui.moveBy(800, 0)
        time.sleep(0.4)
        gui.moveBy(1100, 0)
        time.sleep(1)
        gui.moveBy(-700, 0)
        time.sleep(2)
        gui.moveBy(400, 0)
        time.sleep(1.2)
        gui.moveBy(-800, 0)
        time.sleep(1.1)
        gui.moveBy(600, 0)
        time.sleep(2)
        gui.moveBy(-300, 0)
        time.sleep(2)
        guilib.keyUp('w')
        gui.moveBy(-2400, 0)
        guilib.press('escape')
        time.sleep(0.5)
        guilib.press('escape')
        time.sleep(2)

    guilib.keyUp('shift')
    raise Exception('NYI')

if __name__ == "__main__":
    main()