#!/usr/bin/env python3

import unittest
import read, data, witness
import cv2 as cv

read.DEBUG = 1
witness.DEBUG = 3

class TestBoardReading(unittest.TestCase):
    pass
# =============================================================================
#     def test_1(self):
#         print("one")
#         image = cv.imread("unittests/one.png")
#         
#         b = read.readBoard(image, data.ONE)
#         
#         self.assertEqual(3, b.width)
#         self.assertEqual(3, b.height)
#         self.assertTrue(b.solve())
#         print(b)
#         self.assertEqual(len(b.elements), 9)
#     
#     def test_1b(self):
#         print("oneb")
#         image = cv.imread("unittests/oneb.png")
#         
#         b = read.readBoard(image, data.ONE)
#         
#         self.assertEqual(3, b.width)
#         self.assertEqual(3, b.height)
#         self.assertTrue(b.solve())
#         print(b)
#         self.assertEqual(len(b.elements), 6)
#     
#     def test_1c(self):
#         print("onec")
#         image = cv.imread("unittests/onec.png")
#         
#         b = read.readBoard(image, data.ONE)
#         
#         self.assertEqual(3, b.width)
#         self.assertEqual(3, b.height)
#         self.assertTrue(b.solve())
#         print(b)
#         self.assertEqual(len(b.elements), 7)
#     
#     def test_1d(self):
#         print("oned")
#         image = cv.imread("unittests/oned.png")
#         
#         b = read.readBoard(image, data.ONE)
#         
#         self.assertEqual(3, b.width)
#         self.assertEqual(3, b.height)
#         self.assertTrue(b.solve())
#         print(b)
#         self.assertEqual(len(b.elements), 10)
#     
#     def test_1e(self):
#         print("onee")
#         image = cv.imread("unittests/onee.png")
#         
#         b = read.readBoard(image, data.ONE)
#         
#         self.assertTrue(b.width == 3 or b.width == 2)
#         self.assertEqual(3, b.height)
#         self.assertTrue(b.solve())
#         print(b)
#         if b.width == 2:
#             self.assertEqual(len(b.elements), 9)
#         else:
#             self.assertEqual(len(b.elements), 15)
#         
#     def test_2(self):
#         print("two")
#         image = cv.imread("unittests/two.png")
#         
#         b = read.readBoard(image, data.TWO)
#         
#         self.assertEqual(7, b.width)
#         self.assertEqual(7, b.height)
#         self.assertTrue(b.solve())
#         print(b)
#         self.assertEqual(len(b.elements), 51)
#     
#     def test_2b(self):
#         print("twob")
#         image = cv.imread("unittests/twob.png")
#         
#         b = read.readBoard(image, data.TWO)
#         
#         self.assertEqual(7, b.width)
#         self.assertEqual(7, b.height)
#         self.assertTrue(b.solve())
#         print(b)
#         self.assertEqual(len(b.elements), 48)
#     
#     def test_2c(self):
#         print("twoc")
#         image = cv.imread("unittests/twoc.png")
#         
#         b = read.readBoard(image, data.TWO)
#         
#         self.assertEqual(7, b.width)
#         self.assertEqual(7, b.height)
#         self.assertTrue(b.solve())
#         print(b)
#         self.assertEqual(len(b.elements), 57)
#         
#     def test_2d(self):
#         print("twod")
#         image = cv.imread("unittests/twod.png")
#         
#         b = read.readBoard(image, data.TWO)
#         
#         self.assertEqual(7, b.width)
#         self.assertEqual(7, b.height)
#         self.assertTrue(b.solve())
#         print(b)
#         self.assertEqual(len(b.elements), 48)
#         
#     def test_2e(self):
#         print("twoe")
#         image = cv.imread("unittests/twoe.png")
#         
#         b = read.readBoard(image, data.TWO)
#         
#         self.assertEqual(7, b.width)
#         self.assertEqual(7, b.height)
#         self.assertTrue(b.solve())
#         print(b)
#         self.assertEqual(len(b.elements), 59)
#         
#     def test_2f(self):
#         print("twof")
#         image = cv.imread("unittests/twof.png")
#         
#         b = read.readBoard(image, data.TWO)
#         
#         self.assertEqual(7, b.width)
#         self.assertEqual(7, b.height)
#         self.assertTrue(b.solve())
#         print(b)
#         self.assertEqual(len(b.elements), 52)
#         
#     def test_2g(self):
#         print("twog")
#         image = cv.imread("unittests/twog.png")
#         
#         b = read.readBoard(image, data.TWO)
#         
#         self.assertEqual(7, b.width)
#         self.assertEqual(7, b.height)
#         self.assertTrue(b.solve())
#         print(b)
#         self.assertEqual(len(b.elements), 51)
# 
#     def test_3(self):
#         print("three")
#         image = cv.imread("unittests/three.png")
#         
#         b = read.readBoard(image, data.THREE)
#         
#         self.assertEqual(4, b.width)
#         self.assertEqual(4, b.height)
#         self.assertTrue(b.solve())
#         print(b)
#         self.assertEqual(len(b.elements), 13)
# 
#     def test_3b(self):
#         print("threeb")
#         image = cv.imread("unittests/threeb.png")
#         
#         b = read.readBoard(image, data.THREE)
#         
#         self.assertEqual(4, b.width)
#         self.assertEqual(4, b.height)
#         self.assertTrue(b.solve())
#         print(b)
#         self.assertEqual(len(b.elements), 13)
# 
#     def test_3c(self):
#         print("threec")
#         image = cv.imread("unittests/threec.png")
#         
#         b = read.readBoard(image, data.THREE)
#         
#         self.assertEqual(4, b.width)
#         self.assertEqual(4, b.height)
#         self.assertTrue(b.solve())
#         print(b)
#         self.assertEqual(len(b.elements), 12)
# 
#     def test_3d(self):
#         print("threed")
#         image = cv.imread("unittests/threed.png")
#         
#         b = read.readBoard(image, data.THREE)
#         
#         self.assertEqual(4, b.width)
#         self.assertEqual(4, b.height)
#         self.assertTrue(b.solve())
#         print(b)
#         self.assertEqual(len(b.elements), 12)
# 
#     def test_3e(self):
#         print("threee")
#         image = cv.imread("unittests/threee.png")
#         
#         b = read.readBoard(image, data.THREE)
#         
#         self.assertEqual(4, b.width)
#         self.assertEqual(4, b.height)
#         self.assertTrue(b.solve())
#         print(b)
#         self.assertEqual(len(b.elements), 13)
# =============================================================================

# =============================================================================
#     def test_4(self):
#         print("four")
#         image = cv.imread("unittests/four.png")
#         image, _ = witness.warpBoard4(image)
#         
#         b = read.readBoard(image, data.FOUR)
#         
#         self.assertEqual(5, b.width)
#         self.assertEqual(5, b.height)
#         self.assertTrue(b.solve())
#         print(b)
#         self.assertEqual(len(b.elements), 18)
#         
#     def test_4b(self):
#         print("fourb")
#         image = cv.imread("unittests/fourb.png")
#         image, _ = witness.warpBoard4(image)
#         
#         b = read.readBoard(image, data.FOUR)
#         
#         self.assertEqual(5, b.width)
#         self.assertEqual(5, b.height)
#         self.assertTrue(b.solve())
#         print(b)
#         self.assertEqual(len(b.elements), 20)
#         
#     def test_4c(self):
#         print("fourc")
#         image = cv.imread("unittests/fourc.png")
#         image, _ = witness.warpBoard4(image)
#         
#         b = read.readBoard(image, data.FOUR)
#         
#         self.assertEqual(5, b.width)
#         self.assertEqual(5, b.height)
#         self.assertTrue(b.solve())
#         print(b)
#         self.assertEqual(len(b.elements), 23)
# =============================================================================
        
    def test_4d(self):
        print("fourd")
        image = cv.imread("unittests/fourd.png")
        image, _ = witness.warpBoard4(image)
        
        b = read.readBoard(image, data.FOUR)
        
        self.assertEqual(5, b.width)
        self.assertEqual(5, b.height)
        self.assertTrue(b.solve())
        print(b)
        self.assertEqual(len(b.elements), 21)
        
    def test_4e(self):
        print("foure")
        image = cv.imread("unittests/foure.png")
        image, _ = witness.warpBoard4(image)
        
        b = read.readBoard(image, data.FOUR)
        
        self.assertEqual(5, b.width)
        self.assertEqual(5, b.height)
        self.assertTrue(b.solve())
        print(b)
        self.assertEqual(len(b.elements), 25)

# =============================================================================
#     def test_5(self):
#         print("five")
#         image = cv.imread("unittests/five.png")
#         
#         b = read.readBoard(image, data.FSSE)
#         
#         self.assertEqual(7, b.width)
#         self.assertEqual(7, b.height)
#         self.assertTrue(b.solve())
#         print(b)
#         self.assertEqual(len(b.elements), 39)
#     
#     def test_5b(self):
#         print("fiveb")
#         image = cv.imread("unittests/fiveb.png")
#         
#         b = read.readBoard(image, data.FSSE)
#         
#         self.assertEqual(7, b.width)
#         self.assertEqual(7, b.height)
#         self.assertTrue(b.solve())
#         print(b)
#         self.assertEqual(len(b.elements), 42)
#     
#     def test_5c(self):
#         print("fivec")
#         image = cv.imread("unittests/fivec.png")
#         
#         b = read.readBoard(image, data.FSSE)
#         
#         self.assertEqual(7, b.width)
#         self.assertEqual(7, b.height)
#         self.assertTrue(b.solve())
#         print(b)
#         self.assertEqual(len(b.elements), 43)
#     
#     def test_5d(self):
#         print("fived")
#         image = cv.imread("unittests/fived.png")
#         
#         b = read.readBoard(image, data.FSSE)
#         
#         self.assertEqual(7, b.width)
#         self.assertEqual(7, b.height)
#         self.assertTrue(b.solve())
#         print(b)
#         self.assertEqual(len(b.elements), 47)
# 
#     def test_6(self):
#         print("six")
#         image = cv.imread("unittests/six.png")
#         
#         b = read.readBoard(image, data.FSSE)
#         
#         self.assertEqual(4, b.width)
#         self.assertEqual(4, b.height)
#         
#         for elt in b.elements:
#             if elt.type == "square":
#                 self.assertTrue(False)
#         
#         self.assertTrue(b.solve())
#         print(b)
#         self.assertEqual(len(b.elements), 16)
# 
#     def test_6b(self):
#         print("sixb")
#         image = cv.imread("unittests/sixb.png")
#         
#         b = read.readBoard(image, data.FSSE)
#         
#         self.assertEqual(4, b.width)
#         self.assertEqual(4, b.height)
#         
#         for elt in b.elements:
#             if elt.type == "square":
#                 self.assertTrue(False)
#         
#         self.assertTrue(b.solve())
#         print(b)
#         self.assertEqual(len(b.elements), 15)
# 
#     def test_6c(self):
#         print("sixc")
#         image = cv.imread("unittests/sixc.png")
#         
#         b = read.readBoard(image, data.FSSE)
#         
#         self.assertEqual(4, b.width)
#         self.assertEqual(4, b.height)
#         
#         for elt in b.elements:
#             if elt.type == "square":
#                 self.assertTrue(False)
#         
#         self.assertTrue(b.solve())
#         print(b)
#         self.assertEqual(len(b.elements), 17)
# 
#     def test_6d(self):
#         print("sixd")
#         image = cv.imread("unittests/sixd.png")
#         
#         b = read.readBoard(image, data.FSSE)
#         
#         self.assertEqual(4, b.width)
#         self.assertEqual(4, b.height)
#         
#         for elt in b.elements:
#             if elt.type == "square":
#                 self.assertTrue(False)
#         
#         self.assertTrue(b.solve())
#         print(b)
#         self.assertEqual(len(b.elements), 18)
# 
#     def test_6e(self):
#         print("sixe")
#         image = cv.imread("unittests/sixe.png")
#         
#         b = read.readBoard(image, data.FSSE)
#         
#         self.assertEqual(4, b.width)
#         self.assertEqual(4, b.height)
#         
#         for elt in b.elements:
#             if elt.type == "square":
#                 self.assertTrue(False)
#         
#         self.assertTrue(b.solve())
#         print(b)
#         self.assertEqual(len(b.elements), 14)
#     
#     def test_7(self):
#         print("seven")
#         image = cv.imread("unittests/seven.png")
#         
#         b = read.readBoard(image, data.FSSE)
#         
#         self.assertEqual(4, b.width)
#         self.assertEqual(4, b.height)
#         
#         for elt in b.elements:
#             if elt.type == "tetris":
#                 print(elt.shape)
#             if elt.type == "square":
#                 self.assertTrue(False)
#         self.assertTrue(b.solve())
#         print(b)
#         
#         self.assertEqual(len(b.elements), 12)
#         self.assertEqual(len(b.elements[-2].shape), 4)
#         self.assertEqual(len(b.elements[-1].shape), 3)
#     
#     def test_7b(self):
#         print("sevenb")
#         image = cv.imread("unittests/sevenb.png")
#         
#         b = read.readBoard(image, data.FSSE)
#         
#         self.assertEqual(4, b.width)
#         self.assertEqual(4, b.height)
#         
#         for elt in b.elements:
#             if elt.type == "tetris":
#                 print(elt.shape)
#             if elt.type == "square":
#                 self.assertTrue(False)
#         self.assertTrue(b.solve())
#         print(b)
#         
#         self.assertEqual(len(b.elements), 11)
#         self.assertEqual(len(b.elements[-3].shape), 4)
#         self.assertEqual(len(b.elements[-1].shape), 3)
#     
#     def test_7c(self):
#         print("sevenc")
#         image = cv.imread("unittests/sevenc.png")
#         
#         b = read.readBoard(image, data.FSSE)
#         
#         self.assertEqual(4, b.width)
#         self.assertEqual(4, b.height)
#         
#         for elt in b.elements:
#             if elt.type == "tetris":
#                 print(elt.shape)
#             if elt.type == "square":
#                 self.assertTrue(False)
#         self.assertTrue(b.solve())
#         print(b)
#         
#         self.assertEqual(len(b.elements), 11)
#         self.assertEqual(len(b.elements[-3].shape), 3)
#         self.assertEqual(len(b.elements[-1].shape), 3)
# 
#     def test_7d(self):
#         print("sevend")
#         image = cv.imread("unittests/sevend.png")
#         
#         b = read.readBoard(image, data.FSSE)
#         
#         self.assertEqual(4, b.width)
#         self.assertEqual(4, b.height)
#         
#         for elt in b.elements:
#             if elt.type == "tetris":
#                 print(elt.shape)
#             if elt.type == "square":
#                 self.assertTrue(False)
#         self.assertTrue(b.solve())
#         print(b)
#         
#         self.assertEqual(len(b.elements), 11)
#         self.assertEqual(len(b.elements[-3].shape), 4)
#         self.assertEqual(len(b.elements[-2].shape), 4)
# 
#     def test_7e(self):
#         print("sevene")
#         image = cv.imread("unittests/sevene.png")
#         
#         b = read.readBoard(image, data.FSSE)
#         
#         self.assertEqual(4, b.width)
#         self.assertEqual(4, b.height)
#         
#         for elt in b.elements:
#             if elt.type == "tetris":
#                 print(elt.shape)
#             if elt.type == "square":
#                 self.assertTrue(False)
#         self.assertTrue(b.solve())
#         print(b)
#         
#         self.assertEqual(len(b.elements), 12)
#         self.assertEqual(len(b.elements[-2].shape), 4)
#         self.assertEqual(len(b.elements[-1].shape), 3)
# 
#     def test_7f(self):
#         print("sevenf")
#         image = cv.imread("unittests/sevenf.png")
#         
#         b = read.readBoard(image, data.FSSE)
#         
#         self.assertEqual(4, b.width)
#         self.assertEqual(4, b.height)
#         
#         for elt in b.elements:
#             if elt.type == "tetris":
#                 print(elt.shape)
#             if elt.type == "square":
#                 self.assertTrue(False)
#         self.assertTrue(b.solve())
#         print(b)
#         
#         self.assertEqual(len(b.elements), 11)
#         self.assertEqual(len(b.elements[-3].shape), 4)
#         self.assertEqual(len(b.elements[-1].shape), 3)
# 
#     def test_7g(self):
#         print("seveng")
#         image = cv.imread("unittests/seveng.png")
#         
#         b = read.readBoard(image, data.FSSE)
#         
#         self.assertEqual(4, b.width)
#         self.assertEqual(4, b.height)
#         
#         for elt in b.elements:
#             if elt.type == "tetris":
#                 print(elt.shape)
#             if elt.type == "square":
#                 self.assertTrue(False)
#         self.assertTrue(b.solve())
#         print(b)
#         
#         self.assertEqual(len(b.elements), 12)
#         self.assertEqual(len(b.elements[-3].shape), 5)
#         self.assertEqual(len(b.elements[-1].shape), 3)
# 
#     def test_7h(self):
#         print("sevenh")
#         image = cv.imread("unittests/sevenh.png")
#         
#         b = read.readBoard(image, data.FSSE)
#         
#         self.assertEqual(4, b.width)
#         self.assertEqual(4, b.height)
#         
#         for elt in b.elements:
#             if elt.type == "tetris":
#                 print(elt.shape)
#             if elt.type == "square":
#                 self.assertTrue(False)
#         self.assertTrue(b.solve())
#         print(b)
#         
#         self.assertEqual(len(b.elements), 11)
#         self.assertEqual(len(b.elements[-3].shape), 3)
#         self.assertEqual(len(b.elements[-2].shape), 3)
# 
#     def test_7i(self):
#         print("seveni")
#         image = cv.imread("unittests/seveni.png")
#         
#         b = read.readBoard(image, data.FSSE)
#         
#         self.assertEqual(4, b.width)
#         self.assertEqual(4, b.height)
#         
#         for elt in b.elements:
#             if elt.type == "tetris":
#                 print(elt.shape)
#             if elt.type == "square":
#                 self.assertTrue(False)
#         self.assertTrue(b.solve())
#         print(b)
#         
#         self.assertEqual(len(b.elements), 12)
#         self.assertEqual(len(b.elements[-2].shape), 5)
#         self.assertEqual(len(b.elements[-1].shape), 5)
# 
#     def test_8(self):
#         print("eight")
#         image = cv.imread("unittests/eight.png")
#         
#         b = read.readBoard(image, data.FSSE)
#         
#         self.assertEqual(6, b.width)
#         self.assertEqual(6, b.height)
#         self.assertTrue(b.solve())
#         print(b)
#         self.assertEqual(len(b.elements), 12)
#     
#     def test_8b(self):
#         print("eightb")
#         image = cv.imread("unittests/eightb.png")
#         
#         b = read.readBoard(image, data.FSSE)
#         
#         self.assertEqual(6, b.width)
#         self.assertEqual(6, b.height)
#         self.assertTrue(b.solve())
#         print(b)
#         self.assertEqual(len(b.elements), 12)
#     
#     def test_8c(self):
#         print("eightc")
#         image = cv.imread("unittests/eightc.png")
#         
#         b = read.readBoard(image, data.FSSE)
#         
#         self.assertEqual(6, b.width)
#         self.assertEqual(6, b.height)
#         self.assertTrue(b.solve())
#         print(b)
#         self.assertEqual(len(b.elements), 12)
#     
#     def test_8d(self):
#         print("eightd")
#         image = cv.imread("unittests/eightd.png")
#         
#         b = read.readBoard(image, data.FSSE)
#         
#         self.assertEqual(6, b.width)
#         self.assertEqual(6, b.height)
#         self.assertTrue(b.solve())
#         print(b)
#         self.assertEqual(len(b.elements), 12)
# =============================================================================

if __name__ == '__main__':
    unittest.main()