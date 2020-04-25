import cv2 as cv
import numpy as np

def osszesSajatVetkor(resizedChars, walshImages):
    sajatvektorok = []
    # len(resizedChars)
    for rowIndex in range(1):
        for colIndex in range(len(resizedChars[rowIndex])):
            sajatvektorok.append(sajatVektor(resizedChars[rowIndex][colIndex], walshImages))
    return sajatvektorok



def sajatVektor(char, walshImages):
    vektor = []
    for walshImage in walshImages:
        sum = 0
        for i in range(64):
            for j in range(64):
                sum += colorToNum(char[i][j]) * colorToNum(walshImage[i][j])
        vektor.append(sum)
    return vektor


def generateWalshImages():
    images = []

    images.append(generateAWalshImage([1, 1, 1, 1]))
    images.append(generateAWalshImage([-1, 1, -1, 1]))
    images.append(generateAWalshImage([-1, -1, 1, 1]))
    images.append(generateAWalshImage([-1, 1, 1, -1]))
    images.append(generateAWalshImage([1, 1, -1, -1]))
    images.append(generateAWalshImage([1, -1, 1, -1]))
    images.append(generateAWalshImage([1, -1, -1, -1]))
    images.append(generateAWalshImage([-1, -1, -1, -1]))

    for imageIndex in range(1, 8):
        image = images[imageIndex].transpose()
        images.append(np.array(image, dtype='uint8'))

    for image1Index in range(1, 8):
        image1 = images[image1Index]
        for image2Index in range(8, 15):
            image2 = images[image2Index]
            image = []
            for i in range(64):
                image.append([])
                for j in range(64):
                    image[i].append(colorToNum(image1[i][j]) * colorToNum(image2[i][j]))
            images.append(np.array(image, dtype='uint8'))

    # cv.imshow('asd', images[16])
    return images



def colorToNum(color):
    if color == 255:
        return 1
    else:
        return -1


def generateAWalshImage(colors):
    image = []
    for row in range(4):
        for i in range(row * 16, (row + 1) * 16):
            image.append([])
            for j in range(64):
                image[i].append(colors[row])
    return np.array(image, dtype='uint8')


def resizeChars(all_chars):
    resizedChars = all_chars
    for rowIndex in range(len(all_chars)):
        for colIndex in range(len(all_chars[rowIndex])):
            resizedChars[rowIndex][colIndex] = cv.resize(all_chars[rowIndex][colIndex], (64, 64))
    return resizedChars