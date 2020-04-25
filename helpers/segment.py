import copy
import numpy as np

def horizontalCut(p_img):
    img = copy.copy(p_img)
    rows = img.shape[0]
    cols = img.shape[1]

    coordinates = []
    coordinate = []
    elements = []
    element = []

    inElement = 0
    for row in range(rows):
        hasBlack = 0
        for col in range(cols):
            if img[row, col] == 0:
                hasBlack = 1

        if hasBlack:
            if inElement == 0:
                coordinate = []
                element = []
                coordinate.append(row)
                inElement = 1
            element.append(img[row])
        else:
            if inElement == 1:
                coordinate.append(row - 1)
                coordinates.append(coordinate)
                elements.append(np.array(element))
                inElement = 0

    if len(coordinate) == 1:
        coordinate.append(row - 1)
        coordinates.append(coordinate)
        elements.append(np.array(element))
    return (coordinates, elements)


def verticalCut(p_img):
    img = copy.copy(p_img)
    rows = img.shape[0]
    cols = img.shape[1]

    coordinates = []
    coordinate = []
    elements = []
    element = []
    inElement = 0

    for pixelCol in range(cols):
        hasBlack = 0
        for pixelRow in range(rows):
            if img[pixelRow, pixelCol] == 0:
                hasBlack = 1

        if hasBlack:
            if inElement == 0:
                inElement = 1
                element = []
                coordinate = []
                coordinate.append(pixelCol)
            element.append(img[:, pixelCol])
        else:
            if inElement == 1:
                coordinate.append(pixelCol - 1)
                coordinates.append(coordinate)
                elements.append(np.array(np.transpose(element)))
                inElement = 0

    return (coordinates, elements)




def solveSpaceInsideChars(p_cut):
    new_cut = []
    new_cut.append([p_cut[0][0][0], p_cut[0][1][1]])

    pont = p_cut[1][0]
    vonal = p_cut[1][1]

    new_img = []
    for row in range(pont.shape[0]):
        new_img.append(np.array(pont[row], dtype='uint8'))

    for row in range(6):
        new_row = []
        for col in range(pont.shape[1]):
            new_row.append(255)
        new_img.append(np.array(new_row, dtype='uint8'))

    for row in range(vonal.shape[0]):
        new_img.append(np.array(vonal[row], dtype='uint8'))

    new_cut.append([])
    new_cut[1] = np.array(new_img)
    # cv.imshow('asd', new_cut[1])

    return new_cut