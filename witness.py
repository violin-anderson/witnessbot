#!/usr/bin/env python3

import time, math, os, mss
import pydirectinput as guilib
import read, data
import numpy as np
import cv2 as cv
from skimage import transform
from matplotlib import pyplot as plt

#REGION = (1680, 0, 1920, 1080) #Game window region
REGION = (0, 0, 1920, 1080) #Game window region
FOURREGION = (600, 400, 700, 350)
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
    bl = locs[np.argmin(summed)] + np.array([-18, 5])
    tr = locs[np.argmax(summed)] + np.array([5, -7])
    print(tl)
    
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
        loaded = red < 60 and green > 90 and blue < green * 0.85 and blue > green * 0.5

def detectPuzzle(x, y, x2, y2):
    image = get_screenshot()
    if DEBUG >= 2:
        plt.imshow(image)
        plt.show()
    
    image = image[y:y2,x:x2]
    if DEBUG >= 1:
        plt.imshow(image)
        plt.show()
    
    return np.any(image[:,:,1] > 190)

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
    
    gui.moveBy(2, 2)
    maxloc2 = findimage(music)
    SENS3D = (2 / (maxloc[0] - maxloc2[0]), 2 / (maxloc[1] - maxloc2[1]))
    
    print(SENS3D)
    if SENS3D[0] < 0 or SENS3D[1] < 0:
        raise Exception("Error while calibrating sensitivity. Please turn down in-game sensitivity or calibrate manually")
        
    gui.moveTo(maxloc2[0] - 1200, maxloc2[1] - 400)
    gui.startstop_solve()
    time.sleep(1)
    
    cursor = cv.imread('images/cursor.png')
    maxloc = findimage(cursor)
    gui.moveBy(2, 2)
    maxloc2 = findimage(cursor)
    SENS = (2 / (maxloc2[0] - maxloc[0]), 2 / (maxloc2[1] - maxloc[1]))
    
    print(SENS)
    if SENS[0] < 0 or SENS[1] < 0:
        raise Exception("Error while calibrating sensitivity. Please turn down in-game sensitivity or calibrate manually")
    
    gui.startstop_solve()
    gui.moveBy(1200, 400)
    
    f = open("sensitivity.txt", 'w')
    f.write(f"{SENS3D[0]} {SENS3D[1]}\n{SENS[0]} {SENS[1]}")
    f.close()

        #cv.imwrite('fssenav2.png', get_screenshot())
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
        time.sleep(0.3)
        guilib.keyUp('d')
        gui.schedule(0.15)
        back = detectPuzzle(1100, 200, 1200, 400)
        gui.execute()
        
        if back:
            gui.moveBy(500, 0)
            guilib.keyDown('w')
            time.sleep(0.6)
            guilib.keyUp('w')
            gui.moveBy(-1400, 0)
            gui.startstop_solve()
            return 'back'
        
        guilib.keyDown('a')
        time.sleep(0.7)
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
            behind = True
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
            time.sleep(0.25)
            guilib.keyUp('d')
            gui.moveBy(150, 0)
            guilib.keyDown('w')
        else:
            gui.moveBy(1200, 0)
        
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
    if current == 'under':
        raise Exception("NYI")
        
    if current == 'behind':
        raise Exception("NYI")

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
        if np.min(res) < 0.01:
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
        gui.moveTo(maxloc[0]+8, maxloc[1]+8)
        
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
        current = 'start'
        solved = {'front': False, 'back': False, 'under': False, 'behind': False}
        
        for i in range(4):
            current = navigateFSSE(current, solved, gui)
            time.sleep(0.8)
            solveBoard(data.FSSE, gui, i)
            gui.startstop_solve()
            solved[current] = True
        
        guilib.keyUp('shift')
        raise Exception('NYI')

if __name__ == "__main__":
    main()