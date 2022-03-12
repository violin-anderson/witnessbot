#!/usr/bin/env python3

import unittest
import read, data, witness
import cv2 as cv

read.DEBUG = 0
witness.DEBUG = 0

class TestBoardReading(unittest.TestCase):
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
# =============================================================================
# =============================================================================
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
# 
#     def test_3f(self):
#         print("threef")
#         image = cv.imread("unittests/threef.png")
#         
#         b = read.readBoard(image, data.THREE)
#         
#         self.assertEqual(4, b.width)
#         self.assertEqual(4, b.height)
#         self.assertTrue(b.solve())
#         print(b)
#         self.assertEqual(len(b.elements), 14)
# 
#     def test_3g(self):
#         print("threeg")
#         image = cv.imread("unittests/threeg.png")
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
# 
#     def test_4(self):
#         print("four")
#         image = cv.imread("unittests/four.png")
#         image, _ = witness.warpBoard4(image)
#         
#         b = read.readBoard(image, data.FOUR)
#         
#         self.assertEqual(5, b.width)
#         self.assertEqual(5, b.height)
#         self.assertTrue(b.solve(optimal=True))
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
#         self.assertTrue(b.solve(optimal=True))
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
#         self.assertTrue(b.solve(optimal=True))
#         print(b)
#         self.assertEqual(len(b.elements), 23)
#         
#     def test_4d(self):
#         print("fourd")
#         image = cv.imread("unittests/fourd.png")
#         image, _ = witness.warpBoard4(image)
#         
#         b = read.readBoard(image, data.FOUR)
#         
#         self.assertEqual(5, b.width)
#         self.assertEqual(5, b.height)
#         self.assertTrue(b.solve(optimal=True))
#         print(b)
#         self.assertEqual(len(b.elements), 23)
#         
#     def test_4e(self):
#         print("foure")
#         image = cv.imread("unittests/foure.png")
#         image, _ = witness.warpBoard4(image)
#         
#         b = read.readBoard(image, data.FOUR)
#         
#         self.assertEqual(5, b.width)
#         self.assertEqual(5, b.height)
#         self.assertTrue(b.solve(optimal=True))
#         print(b)
#         self.assertEqual(len(b.elements), 25)
#         
#     def test_4f(self):
#         print("fourf")
#         image = cv.imread("unittests/fourf.png")
#         image, _ = witness.warpBoard4(image)
#         
#         b = read.readBoard(image, data.FOUR)
#         
#         self.assertEqual(5, b.width)
#         self.assertEqual(5, b.height)
#         self.assertTrue(b.solve(optimal=True))
#         print(b)
#         self.assertEqual(len(b.elements), 26)
#                 
#     def test_4g(self):
#         print("fourg")
#         image = cv.imread("unittests/fourg.png")
#         image, _ = witness.warpBoard4(image)
#         
#         b = read.readBoard(image, data.FOUR)
#         
#         self.assertEqual(5, b.width)
#         self.assertEqual(5, b.height)
#         self.assertTrue(b.solve(optimal=True))
#         print(b)
#         self.assertEqual(len(b.elements), 26)
#                 
#     def test_4h(self):
#         print("fourh")
#         image = cv.imread("unittests/fourh.png")
#         image, _ = witness.warpBoard4(image)
#         
#         b = read.readBoard(image, data.FOUR)
#         
#         self.assertEqual(5, b.width)
#         self.assertEqual(5, b.height)
#         self.assertTrue(b.solve(optimal=True))
#         print(b)
#         self.assertEqual(len(b.elements), 24)
#                 
#     def test_4i(self):
#         print("fouri")
#         image = cv.imread("unittests/fouri.png")
#         image, _ = witness.warpBoard4(image)
#         
#         b = read.readBoard(image, data.FOUR)
#         
#         self.assertEqual(5, b.width)
#         self.assertEqual(5, b.height)
#         self.assertTrue(b.solve(optimal=True))
#         print(b)
#         self.assertEqual(len(b.elements), 25)
# 
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
#     def test_5f(self):
#         print("fivef")
#         image = cv.imread("unittests/fivef.png")
#         
#         b = read.readBoard(image, data.FSSE)
#         
#         self.assertEqual(7, b.width)
#         self.assertEqual(7, b.height)
#         self.assertTrue(b.solve())
#         print(b)
#         self.assertEqual(len(b.elements), 43)
# 
#     def test_5g(self):
#         print("fiveg")
#         image = cv.imread("unittests/fiveg.png")
#         
#         b = read.readBoard(image, data.FSSE)
#         
#         self.assertEqual(7, b.width)
#         self.assertEqual(7, b.height)
#         self.assertTrue(b.solve())
#         print(b)
#         self.assertEqual(len(b.elements), 42)
# 
#     def test_5h(self):
#         print("fiveh")
#         image = cv.imread("unittests/fiveh.png")
#         
#         b = read.readBoard(image, data.FSSE)
#         
#         self.assertTrue(b.width == 7 or b.width == 4)
#         self.assertEqual(7, b.height)
#         self.assertTrue(b.solve())
#         print(b)
#         self.assertEqual(len(b.elements), 37)
# 
# # =============================================================================
# # def test_5c(self):
# #     print("fivec")
# #     image = cv.imread("unittests/fivec.png")
# #     
# #     b = read.readBoard(image, data.FSSE)
# #     
# #     self.assertEqual(7, b.width)
# #     self.assertEqual(7, b.height)
# #     self.assertTrue(b.solve())
# #     print(b)
# #     self.assertEqual(len(b.elements), 43)
# # 
# # def test_5e(self):
# #     print("fivee")
# #     image = cv.imread("unittests/fivee.png")
# #     
# #     b = read.readBoard(image, data.FSSE)
# #     
# #     self.assertEqual(7, b.width)
# #     self.assertEqual(7, b.height)
# #     self.assertTrue(b.solve())
# #     print(b)
# #     self.assertEqual(len(b.elements), 47)
# # =============================================================================
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
#     def test_7j(self):
#         print("sevenj")
#         image = cv.imread("unittests/sevenj.png")
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
#         self.assertEqual(len(b.elements[-3].shape), 3)
#         self.assertEqual(len(b.elements[-2].shape), 3)
#                 
#     def test_7k(self):
#         print("sevenk")
#         image = cv.imread("unittests/sevenk.png")
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
#         self.assertEqual(len(b.elements[-4].shape), 3)
#                 
#     def test_7l(self):
#         print("sevenl")
#         image = cv.imread("unittests/sevenl.png")
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
#         self.assertEqual(len(b.elements), 10)
#         self.assertEqual(len(b.elements[-2].shape), 3)
#         self.assertEqual(len(b.elements[-4].shape), 4)
#                 
#     def test_7m(self):
#         print("sevenm")
#         image = cv.imread("unittests/sevenm.png")
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
#         self.assertEqual(len(b.elements[-1].shape), 5)
#         self.assertEqual(len(b.elements[-3].shape), 5)
#                 
#     def test_7n(self):
#         print("sevenn")
#         image = cv.imread("unittests/sevenn.png")
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
#         self.assertEqual(len(b.elements[-4].shape), 4)
#         self.assertEqual(len(b.elements[-1].shape), 3)
#                 
#     def test_7o(self):
#         print("seveno")
#         image = cv.imread("unittests/seveno.png")
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
#         self.assertEqual(len(b.elements), 10)
#         self.assertEqual(len(b.elements[-3].shape), 3)
#         self.assertEqual(len(b.elements[-4].shape), 3)
#                         
#     def test_7p(self):
#         print("sevenp")
#         image = cv.imread("unittests/sevenp.png")
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
#         self.assertEqual(len(b.elements), 9)
#         self.assertEqual(len(b.elements[-2].shape), 4)
#         self.assertEqual(len(b.elements[-4].shape), 5)
# =============================================================================

# =============================================================================
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
#         self.assertEqual(len(list(filter(lambda e: e.type == "hex" and e.color == 'o', b.elements))), 2)
#         self.assertEqual(len(list(filter(lambda e: e.type == "hex" and e.color == 'c', b.elements))), 2)
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
#         self.assertEqual(len(list(filter(lambda e: e.type == "hex" and e.color == 'o', b.elements))), 2)
#         self.assertEqual(len(list(filter(lambda e: e.type == "hex" and e.color == 'c', b.elements))), 2)
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
#         self.assertEqual(len(list(filter(lambda e: e.type == "hex" and e.color == 'o', b.elements))), 2)
#         self.assertEqual(len(list(filter(lambda e: e.type == "hex" and e.color == 'c', b.elements))), 2)
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
#         self.assertEqual(len(list(filter(lambda e: e.type == "hex" and e.color == 'o', b.elements))), 2)
#         self.assertEqual(len(list(filter(lambda e: e.type == "hex" and e.color == 'c', b.elements))), 2)
#     
#     def test_8e(self):
#         print("eighte")
#         image = cv.imread("unittests/eighte.png")
#         
#         b = read.readBoard(image, data.FSSE)
#         
#         self.assertEqual(6, b.width)
#         self.assertEqual(6, b.height)
#         self.assertTrue(b.solve())
#         print(b)
#         self.assertEqual(len(b.elements), 12)
#         self.assertEqual(len(list(filter(lambda e: e.type == "hex" and e.color == 'o', b.elements))), 2)
#         self.assertEqual(len(list(filter(lambda e: e.type == "hex" and e.color == 'c', b.elements))), 2)
#     
#     def test_8f(self):
#         print("eightf")
#         image = cv.imread("unittests/eightf.png")
#         
#         b = read.readBoard(image, data.FSSE)
#         
#         self.assertEqual(6, b.width)
#         self.assertEqual(6, b.height)
#         self.assertTrue(b.solve())
#         print(b)
#         self.assertEqual(len(b.elements), 12)
#         self.assertEqual(len(list(filter(lambda e: e.type == "hex" and e.color == 'o', b.elements))), 2)
#         self.assertEqual(len(list(filter(lambda e: e.type == "hex" and e.color == 'c', b.elements))), 2)
# =============================================================================

# =============================================================================
#     def test_9(self):
#         print("nine")
#         image = cv.imread("unittests/nine.png")
#         image, _ = witness.resize(image, *witness.NINECREGION)
#         
#         b = read.readBoard(image, data.NINE)
#         
#         self.assertEqual(4, b.width)
#         self.assertEqual(4, b.height)
#         self.assertFalse(b.solve())
#         self.assertEqual(len(b.elements), 12)
#     
#     def test_9b1(self):
#         print("nineb1")
#         image = cv.imread("unittests/nineb.png")
#         image, _ = witness.resize(image, *witness.NINECREGION)
#         
#         b = read.readBoard(image, data.NINE)
#         
#         self.assertEqual(4, b.width)
#         self.assertEqual(4, b.height)
#         self.assertTrue(b.solve())
#         print(b)
#         self.assertEqual(len(b.elements), 12)
#     
#     def test_9b2(self):
#         print("nineb2")
#         image = cv.imread("unittests/nineb.png")
#         image, _ = witness.resize(image, *witness.NINELREGION)
#         
#         b = read.readBoard(image, data.NINE)
#         
#         self.assertEqual(4, b.width)
#         self.assertEqual(4, b.height)
#         self.assertFalse(b.solve())
#         self.assertEqual(len(b.elements), 12)
#     
#     def test_9b3(self):
#         print("nineb3")
#         image = cv.imread("unittests/nineb.png")
#         image, _ = witness.resize(image, *witness.NINERREGION)
#         
#         b = read.readBoard(image, data.NINE)
#         
#         self.assertEqual(4, b.width)
#         self.assertEqual(4, b.height)
#         self.assertFalse(b.solve())
#         self.assertEqual(len(b.elements), 12)
#     
#     def test_9c1(self):
#         print("ninec1")
#         image = cv.imread("unittests/ninec.png")
#         image, _ = witness.resize(image, *witness.NINECREGION)
#         
#         b = read.readBoard(image, data.NINE)
#         
#         self.assertEqual(4, b.width)
#         self.assertEqual(4, b.height)
#         self.assertTrue(b.solve())
#         print(b)
#         self.assertEqual(len(b.elements), 12)
#     
#     def test_9c2(self):
#         print("ninec2")
#         image = cv.imread("unittests/ninec.png")
#         image, _ = witness.resize(image, *witness.NINELREGION)
#         
#         b = read.readBoard(image, data.NINE)
#         
#         self.assertEqual(4, b.width)
#         self.assertEqual(4, b.height)
#         self.assertFalse(b.solve())
#         self.assertEqual(len(b.elements), 12)
#     
#     def test_10(self):
#         print("ten")
#         image = cv.imread("unittests/ten.png")
#         image, _ = witness.resize(image, *witness.TENCREGION)
#         
#         b = read.readBoard(image, data.TEN)
#         
#         self.assertEqual(4, b.width)
#         self.assertEqual(4, b.height)
#         self.assertFalse(b.solve())
#         self.assertEqual(len(b.elements), 9)
#             
#     def test_10b(self):
#         print("tenb")
#         image = cv.imread("unittests/tenb.png")
#         image, _ = witness.resize(image, *witness.TENLREGION)
#         
#         b = read.readBoard(image, data.TEN)
#         
#         self.assertEqual(4, b.width)
#         self.assertEqual(4, b.height)
#         self.assertTrue(b.solve())
#         print(b)
#         self.assertEqual(len(b.elements), 9)
#             
#     def test_10c(self):
#         print("tenc")
#         image = cv.imread("unittests/tenc.png")
#         image, _ = witness.resize(image, *witness.TENRREGION)
#         
#         b = read.readBoard(image, data.TEN)
#         
#         self.assertEqual(4, b.width)
#         self.assertEqual(4, b.height)
#         self.assertFalse(b.solve())
#         self.assertEqual(len(b.elements), 9)
#             
#     def test_10d(self):
#         print("tend")
#         image = cv.imread("unittests/tend.png")
#         image, _ = witness.resize(image, *witness.TENLREGION)
#         
#         b = read.readBoard(image, data.TEN)
#         
#         self.assertEqual(4, b.width)
#         self.assertEqual(4, b.height)
#         self.assertTrue(b.solve())
#         print(b)
#         self.assertEqual(len(b.elements), 9)
# 
#     def test_11(self):
#         print("eleven")
#         image = cv.imread("unittests/eleven.png")
#         image, _ = witness.resize(image, 0, 0, 1920, 1080, eleven=True)
#         
#         b = read.readBoard(image, data.ELEVEN)
#         
#         self.assertEqual(4, b.width)
#         self.assertEqual(4, b.height)
#         self.assertEqual(len(b.elements), 8)
#         self.assertEqual(sum(map(lambda e: e.count, b.elements)), 9)
#         self.assertTrue(b.solve())
#         print(b)
# 
#     def test_11b(self):
#         print("elevenb")
#         image = cv.imread("unittests/elevenb.png")
#         image, _ = witness.resize(image, 0, 0, 1920, 1080, eleven=True)
#         
#         b = read.readBoard(image, data.ELEVEN)
#         
#         self.assertEqual(4, b.width)
#         self.assertEqual(4, b.height)
#         self.assertEqual(len(b.elements), 6)
#         self.assertEqual(sum(map(lambda e: e.count, b.elements)), 8)
#         self.assertTrue(b.solve())
#         print(b)
# 
#     def test_11c(self):
#         print("elevenc")
#         image = cv.imread("unittests/elevenc.png")
#         image, _ = witness.resize(image, 0, 0, 1920, 1080, eleven=True)
#         
#         b = read.readBoard(image, data.ELEVEN)
#         
#         self.assertEqual(4, b.width)
#         self.assertEqual(4, b.height)
#         self.assertEqual(len(b.elements), 8)
#         self.assertEqual(sum(map(lambda e: e.count, b.elements)), 12)
#         self.assertTrue(b.solve())
#         print(b)
# 
#     def test_11d(self):
#         print("elevend")
#         image = cv.imread("unittests/elevend.png")
#         image, _ = witness.resize(image, 0, 0, 1920, 1080, eleven=True)
#         
#         b = read.readBoard(image, data.ELEVEN)
#         
#         self.assertEqual(4, b.width)
#         self.assertEqual(4, b.height)
#         self.assertEqual(len(b.elements), 6)
#         self.assertEqual(sum(map(lambda e: e.count, b.elements)), 10)
#         self.assertTrue(b.solve())
#         print(b)
# 
#     def test_11e(self):
#         print("elevene")
#         image = cv.imread("unittests/elevene.png")
#         image, _ = witness.resize(image, 0, 0, 1920, 1080, eleven=True)
#         
#         b = read.readBoard(image, data.ELEVEN)
#         
#         self.assertEqual(4, b.width)
#         self.assertEqual(4, b.height)
#         self.assertEqual(len(b.elements), 6)
#         self.assertEqual(sum(map(lambda e: e.count, b.elements)), 9)
#         self.assertTrue(b.solve())
#         print(b)
# 
#     def test_11f(self):
#         print("elevenf")
#         image = cv.imread("unittests/elevenf.png")
#         image, _ = witness.resize(image, 0, 0, 1920, 1080, eleven=True)
#         
#         b = read.readBoard(image, data.ELEVEN)
#         
#         self.assertEqual(4, b.width)
#         self.assertEqual(4, b.height)
#         self.assertEqual(len(b.elements), 6)
#         self.assertEqual(sum(map(lambda e: e.count, b.elements)), 13)
#         self.assertTrue(b.solve())
#         print(b)
# 
#     def test_11g(self):
#         print("eleveng")
#         image = cv.imread("unittests/eleveng.png")
#         image, _ = witness.resize(image, 0, 0, 1920, 1080, eleven=True)
#         
#         b = read.readBoard(image, data.ELEVEN)
#         
#         self.assertEqual(4, b.width)
#         self.assertEqual(4, b.height)
#         self.assertEqual(len(b.elements), 6)
#         self.assertEqual(sum(map(lambda e: e.count, b.elements)), 14)
#         self.assertTrue(b.solve())
#         print(b)
# =============================================================================
        
# =============================================================================
#     def test_13(self):
#         print("thirteen")
#         image0 = cv.imread("unittests/thirteen0.png")
#         image1 = cv.imread("unittests/thirteen1.png")
#         image2 = cv.imread("unittests/thirteen2.png")
#         
#         b = read.readCylinder([image1, image0, image2], data.THIRTEEN)
#         self.assertEqual(len(b.elements), 6)
#         self.assertTrue(b.solve(True))
#         print(b)
#                 
#     def test_13b(self):
#         print("thirteenb")
#         image0 = cv.imread("unittests/thirteenb0.png")
#         image1 = cv.imread("unittests/thirteenb1.png")
#         image2 = cv.imread("unittests/thirteenb2.png")
#         
#         b = read.readCylinder([image1, image0, image2], data.THIRTEEN)
#         self.assertEqual(len(b.elements), 6)
#         self.assertTrue(b.solve(True))
#         print(b)
#                         
#     def test_13c(self):
#         print("thirteenc")
#         image0 = cv.imread("unittests/thirteenc0.png")
#         image1 = cv.imread("unittests/thirteenc1.png")
#         image2 = cv.imread("unittests/thirteenc2.png")
#         
#         b = read.readCylinder([image1, image0, image2], data.THIRTEEN)
#         #b.symmetry = "rotparallel"
#         self.assertEqual(len(b.elements), 6)
#         self.assertTrue(b.solve(True))
#         print(b)
#                                 
#     def test_13d(self):
#         print("thirteend")
#         image0 = cv.imread("unittests/thirteend0.png")
#         image1 = cv.imread("unittests/thirteend1.png")
#         image2 = cv.imread("unittests/thirteend2.png")
#         
#         b = read.readCylinder([image1, image0, image2], data.THIRTEEN)
#         self.assertEqual(len(b.elements), 6)
#         self.assertTrue(b.solve(True))
#         print(b)
#                         
#     def test_13e(self):
#         print("thirteene")
#         image0 = cv.imread("unittests/thirteene0.png")
#         image1 = cv.imread("unittests/thirteene1.png")
#         image2 = cv.imread("unittests/thirteene2.png")
#         
#         b = read.readCylinder([image1, image0, image2], data.THIRTEEN)
#         self.assertEqual(len(b.elements), 6)
#         self.assertTrue(b.solve(True))
#         print(b)
#                                 
#     def test_13f(self):
#         print("thirteenf")
#         image0 = cv.imread("unittests/thirteenf0.png")
#         image1 = cv.imread("unittests/thirteenf1.png")
#         image2 = cv.imread("unittests/thirteenf2.png")
#         
#         b = read.readCylinder([image1, image0, image2], data.THIRTEEN)
#         self.assertEqual(len(b.elements), 6)
#         self.assertTrue(b.solve(True))
#         print(b)
#                                 
#     def test_13g(self):
#         print("thirteeng")
#         image0 = cv.imread("unittests/thirteeng0.png")
#         image1 = cv.imread("unittests/thirteeng1.png")
#         image2 = cv.imread("unittests/thirteeng2.png")
#         
#         b = read.readCylinder([image1, image0, image2], data.THIRTEEN)
#         self.assertEqual(len(b.elements), 6)
#         self.assertTrue(b.solve(True))
#         print(b)
#                                 
#     def test_13h(self):
#         print("thirteenh")
#         image0 = cv.imread("unittests/thirteenh0.png")
#         image1 = cv.imread("unittests/thirteenh1.png")
#         image2 = cv.imread("unittests/thirteenh2.png")
#         
#         b = read.readCylinder([image1, image0, image2], data.THIRTEEN)
#         self.assertEqual(len(b.elements), 6)
#         self.assertTrue(b.solve(True))
#         print(b)
#                                 
#     def test_13i(self):
#         print("thirteeni")
#         image0 = cv.imread("unittests/thirteeni0.png")
#         image1 = cv.imread("unittests/thirteeni1.png")
#         image2 = cv.imread("unittests/thirteeni2.png")
#         
#         b = read.readCylinder([image1, image0, image2], data.THIRTEEN)
#         self.assertEqual(len(b.elements), 6)
#         self.assertTrue(b.solve(True))
#         print(b)
# 
#     def test_13j(self):
#         print("thirteenj")
#         image0 = cv.imread("unittests/thirteenj0.png")
#         image1 = cv.imread("unittests/thirteenj1.png")
#         image2 = cv.imread("unittests/thirteenj2.png")
#         
#         b = read.readCylinder([image1, image0, image2], data.THIRTEEN)
#         self.assertEqual(len(b.elements), 6)
#         self.assertTrue(b.solve(True))
#         print(b)
# =============================================================================

    def test_14(self):
        print("fourteen")
        image0 = cv.imread("unittests/fourteen0.png")
        image1 = cv.imread("unittests/fourteen1.png")
        image2 = cv.imread("unittests/fourteen2.png")
        
        b = read.readCylinder([image2, image1, image0], data.FOURTEEN)
        self.assertEqual(len(b.elements), 6)
        self.assertTrue(b.solve(True))
        print(b)

    def test_14b(self):
        print("fourteenb")
        image0 = cv.imread("unittests/fourteenb0.png")
        image1 = cv.imread("unittests/fourteenb1.png")
        image2 = cv.imread("unittests/fourteenb2.png")
        
        b = read.readCylinder([image2, image1, image0], data.FOURTEEN)
        self.assertEqual(len(b.elements), 7)
        self.assertTrue(b.solve(True))
        print(b)

    def test_14c(self):
        print("fourteenc")
        image0 = cv.imread("unittests/fourteenc0.png")
        image1 = cv.imread("unittests/fourteenc1.png")
        image2 = cv.imread("unittests/fourteenc2.png")
        
        b = read.readCylinder([image2, image1, image0], data.FOURTEEN)
        self.assertEqual(len(b.elements), 6)
        self.assertTrue(b.solve(True))
        print(b)

    def test_14d(self):
        print("fourteend")
        image0 = cv.imread("unittests/fourteend0.png")
        image1 = cv.imread("unittests/fourteend1.png")
        image2 = cv.imread("unittests/fourteend2.png")
        
        b = read.readCylinder([image2, image1, image0], data.FOURTEEN)
        self.assertEqual(len(b.elements), 6)
        self.assertTrue(b.solve(True))
        print(b)

    def test_14e(self):
        print("fourteene")
        image0 = cv.imread("unittests/fourteene0.png")
        image1 = cv.imread("unittests/fourteene1.png")
        image2 = cv.imread("unittests/fourteene2.png")
        
        b = read.readCylinder([image2, image1, image0], data.FOURTEEN)
        self.assertEqual(len(b.elements), 6)
        self.assertTrue(b.solve(True))
        print(b)

    def test_14f(self):
        print("fourteenf")
        image0 = cv.imread("unittests/fourteenf0.png")
        image1 = cv.imread("unittests/fourteenf1.png")
        image2 = cv.imread("unittests/fourteenf2.png")
        
        b = read.readCylinder([image2, image1, image0], data.FOURTEEN)
        self.assertEqual(len(b.elements), 6)
        self.assertTrue(b.solve(True))
        print(b)

    def test_14g(self):
        print("fourteeng")
        image0 = cv.imread("unittests/fourteeng0.png")
        image1 = cv.imread("unittests/fourteeng1.png")
        image2 = cv.imread("unittests/fourteeng2.png")
        
        b = read.readCylinder([image2, image1, image0], data.FOURTEEN)
        self.assertEqual(len(b.elements), 8)
        self.assertTrue(b.solve(True))
        print(b)

    def test_14h(self):
        print("fourteenh")
        image0 = cv.imread("unittests/fourteenh0.png")
        image1 = cv.imread("unittests/fourteenh1.png")
        image2 = cv.imread("unittests/fourteenh2.png")
        
        b = read.readCylinder([image2, image1, image0], data.FOURTEEN)
        self.assertEqual(len(b.elements), 7)
        self.assertTrue(b.solve(True))
        print(b)

    def test_14i(self):
        print("fourteeni")
        image0 = cv.imread("unittests/fourteeni0.png")
        image1 = cv.imread("unittests/fourteeni1.png")
        image2 = cv.imread("unittests/fourteeni2.png")
        
        b = read.readCylinder([image2, image1, image0], data.FOURTEEN)
        self.assertEqual(len(b.elements), 7)
        self.assertTrue(b.solve(True))
        print(b)

if __name__ == '__main__':
    unittest.main()
