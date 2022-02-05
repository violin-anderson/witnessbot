#!/usr/bin/env python3

import pyautogui, time, math
import read, data
import numpy as np
import cv2 as cv
from skimage import transform
from matplotlib import pyplot as plt

REGION = (1680, 0, 1920, 1080) #Game window region
FOURREGION = (460, 585, 770, 350)
SENS = 1.92
#SENS3D = 0.575
SENS3D = 0.677
FOV = 100 * math.pi / 180

DEBUG = 0

class WitnessGUI:
    def __init__(self, walking = True):
        self.CENTER = (REGION[2]//2, REGION[3]//2)
        self.mousecoords = self.CENTER
        self.clicked = False
        self.clickedsens = 1
        self.walking = walking
        self.nexttime = 0
    
    def startstop_solve(self):
        pyautogui.press("space")
        self.walking = not self.walking
        if not self.walking:
            self.mousecoords = self.CENTER
    
    def click(self):
        assert(not self.walking)
        pyautogui.click(0, 0)
        self.clicked = not self.clicked
    
    def moveBy(self, x, y):
        if self.walking:
            sens = SENS3D
        else:
            sens = SENS
            if self.clicked:
                sens *= self.clickedsens
        
        # I don't know why this works, but it does
        pyautogui.moveTo(x * sens, y * sens)
        self.mousecoords = (self.mousecoords[0] + x, self.mousecoords[1] + y)
    
    def moveTo(self, x, y):
        if self.walking:
            self.moveBy(x-self.CENTER[0], y-self.CENTER[1])
            # These formulas aren't right but I can't figure out the right ones
            # Account for perspective warp at edges of screen
            #c = math.tan(FOV/2)/(REGION[3]/2)
            #x = math.atan((x-self.CENTER[0])*c)/FOV*REGION[3]
            # Same formula applies to y, assuming xFOV and yFOV are proportional to pixels
            #y = math.atan((y-self.CENTER[1])*c)/FOV*REGION[3]
            #self.moveBy(x, y)
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

def get_screenshot(region=REGION):
    return cv.cvtColor(np.array(pyautogui.screenshot(region=region)), cv.COLOR_RGB2BGR)

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

tlimg4 = cv.imread('images/fourtl.png')
trimg4 = cv.imread('images/fourtr.png')
blimg4 = cv.imread('images/fourbl.png')
brimg4 = cv.imread('images/fourbr.png')

def warpBoard4(image):
    #tl = np.array(findimage(tlimg4, np.copy(image))) + np.array([30, 20])
    tl = np.array([290, 35])
    #bl = np.array(findimage(blimg4, np.copy(image))) + np.array([20, 35])
    bl = tl + np.array([-180, 255])
    #tr = np.array(findimage(trimg4, np.copy(image))) + np.array([30, 15])
    tr = tl + np.array([330, 5])
    #br = np.array(findimage(brimg4, np.copy(image))) + np.array([50, 40])
    br = tl + np.array([390, 275])
    
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
    image = get_screenshot((REGION[0]+FOURREGION[0], REGION[1]+FOURREGION[1],
                            FOURREGION[2], FOURREGION[3]))
    cv.imwrite(f"four.png", image)
    image, warpfn = warpBoard4(image)
    
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
        image = get_screenshot((REGION[0]+x, REGION[1]+y, x2-x, y2-y))
        blue = np.average(image[:,:,0])
        green = np.average(image[:,:,1])
        red = np.average(image[:,:,2])
        loaded = red < 60 and green > 90 and blue < green * 0.85 and blue > green * 0.5

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

def main():
    escape = cv.imread('images/escape.png')
    music = cv.imread('images/record.png')
    music2 = cv.imread('images/recordc.png')
    
    time.sleep(3)
    pyautogui.PAUSE = 0.02
    
    # Look for the escape screen
    ready = False
    while not ready:
        image = get_screenshot()
        res = cv.matchTemplate(image, escape, cv.TM_SQDIFF_NORMED)
        if np.min(res) < 0.01:
            ready = True
    pyautogui.press("escape")
    time.sleep(0.5)
    
    gui = WitnessGUI(True)
    
    while True:
        # Look for the music box
        maxloc = findimage(music)
        gui.moveTo(maxloc[0] - 100, maxloc[1] + 300)
        
        # Walk to the music box
        pyautogui.keyUp('shift')
        pyautogui.keyDown('shift')
        pyautogui.keyDown('w')
        time.sleep(1)
        pyautogui.keyUp('w')
        
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
        pyautogui.keyDown('w')
        time.sleep(2.1)
        pyautogui.keyUp('w')
        
        gui.startstop_solve()
        
        # Solve puzzles 1-3
        waitForPuzzle(775, 350, 1130, 710)
        
        gui = WitnessGUI(False)
        solveBoard(data.ONE, gui)
        
        pyautogui.press('d')
        time.sleep(0.4)
        
        solveBoard(data.TWO, gui)
        
        pyautogui.press('d')
        time.sleep(0.4)
        
        solveBoard(data.THREE, gui)
        gui.startstop_solve()
        
        # Go to 4
        pyautogui.keyDown('d')
        time.sleep(0.1)
        pyautogui.keyDown('w')
        time.sleep(0.7)
        pyautogui.keyUp('d')
        time.sleep(0.71)
        pyautogui.keyUp('w')
        
        gui.moveBy(-1000, 180)
        gui.startstop_solve()
        
        time.sleep(0.5)
        #pyautogui.PAUSE = 1
        solveBoard4(gui)
        gui.startstop_solve()
        
        # Go to FSSE
        pyautogui.PAUSE = 0
        gui.moveBy(1600, -200)
        pyautogui.keyDown('w')
        time.sleep(0.3)
        gui.moveBy(200, 0)
        time.sleep(0.3)
        gui.moveBy(-100, 0)
        
        time.sleep(0.8)
        gui.schedule(0.4)
        image1 = np.array(pyautogui.screenshot(region=REGION))
        gui.execute()
        pyautogui.keyDown('a')
        pyautogui.keyUp('w')
        gui.moveBy(50, 0)
        
        gui.schedule(0.2)
        gui.execute()
        pyautogui.keyUp('a')
        pyautogui.keyDown('d')
        gui.schedule(0.5)
        image2 = np.array(pyautogui.screenshot(region=REGION))
        gui.execute()
        pyautogui.keyUp('d')
        
        cv.imwrite('trans1.png', image1)
        cv.imwrite('trans2.png', image2)
        
        pyautogui.keyUp('shift')
        raise Exception('NYI')
        
        # Go back to the start from 3
        gui.moveBy(-2150, 0)
        pyautogui.keyDown('w')
        time.sleep(3.5)
        pyautogui.keyUp('w')
        gui.moveBy(-2500, -50)
        
        pyautogui.press('escape')
        time.sleep(0.1)
        pyautogui.press('escape')
    
    #read.DEBUG = 2
    #pyautogui.PAUSE = 0.5
    #time.sleep(20)
    
    for i in range(4):
        waitForPuzzle(775, 375, 1140, 730)
        time.sleep(0.5)
        
        gui = WitnessGUI(False)
        solveBoard(data.FSSE, gui, i)
        time.sleep(3)

if __name__ == "__main__":
    main()