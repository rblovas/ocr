import cv2 as cv
class Char:
    def __init__(self, number=0, size=0, coordinate=None, space=False, vector=None, img=None, value=''):
        self.number = number
        self.size = size
        self.coordinate = coordinate
        self.space = space
        self.vector = vector
        self.img = img
        self.value = value

    def printData(self):
        print('Sorszam: ', self.number)
        print('Size: ', self.size)
        print('Koordináta: ', self.coordinate)
        print('Van benne space: ', self.space)
        print('Sajatvektor: ', self.vector)
        print('Erteke: ', self.value)

    def showImage(self):
        cv.imshow('Show a char', self.img)

    def setSizeByCoordinates(self, top, bottom):
        self.size = bottom - top
