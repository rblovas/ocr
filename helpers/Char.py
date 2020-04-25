import cv2 as cv
class Char:
    def __init__(self, number=0, size=0, vector=None, img=None):
        self.number = number
        self.size = size
        self.vector = vector
        self.img = img

    def printData(self):
        print('Sorszam: ', self.number)
        print('Size: ', self.size)
        print('Sajatvektor: ', self.vector)

    def showImage(self):
        cv.imshow('Show a char', self.img)

    def setSizeByCoordinates(self, top, bottom):
        self.size = bottom - top
