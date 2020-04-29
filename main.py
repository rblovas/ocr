#!/usr/bin/env python3
from __future__ import print_function

from helpers import learning
from helpers import preprocess
from helpers import segment
from helpers import walsh
from helpers import showSteps
from helpers import Char
from helpers import doit

import cv2 as cv

LEARN = False
FONT = 'arial'
IMG_NAME = 'photo_hello'

# good example: lorem_short_md, photo_hello

def main():
    #   PREPROCESS
    if LEARN:
        img = preprocess.get_image('learn', FONT)
    else:
        img = preprocess.get_image(IMG_NAME, FONT)

    grayscaled = preprocess.grayscale(img)
    showSteps.showInMovedWindow('grayscaled', grayscaled, 0, 600)
    if FONT == 'arial':
        filter_n = 3
    else:
        filter_n = 4
    filtered = preprocess.filter(grayscaled, filter_n)
    showSteps.showInMovedWindow('filtered', filtered, 0, 200)

    #   SEGMENT
    #   HORIZONTAL
    rows = segment.horizontalCut(filtered)
    coordinates_of_rows = rows[0]
    img_of_the_rows = rows[1]

    #   VERTICAL
    ALL_coordinates_of_chars = []
    ALL_images_of_chars = []
    for row in range(len(coordinates_of_rows)):
        cut = segment.verticalCut(img_of_the_rows[row])
        ALL_coordinates_of_chars.append(cut[0])
        ALL_images_of_chars.append(cut[1])

    #   HORIZONTAL
    ALL_coordinates_of_cutted_chars = []
    ALL_images_of_cutted_chars = []
    spaceInside = []
    for row in range(len(coordinates_of_rows)):
        ALL_coordinates_of_cutted_chars.append([])
        ALL_images_of_cutted_chars.append([])
        for col in range(len(ALL_coordinates_of_chars[row])):
            cut = segment.horizontalCut(ALL_images_of_chars[row][col])
            new_cut = []
            if len(cut[0]) > 1:
                new_cut = segment.solveSpaceInsideChars(cut)
                spaceInside.append([row, col])
            else:
                new_cut.append(cut[0][0])
                new_cut.append(cut[1][0])

            ALL_coordinates_of_cutted_chars[row].append(new_cut[0])
            ALL_images_of_cutted_chars[row].append(new_cut[1])

    showSteps.addBorder(img, coordinates_of_rows, ALL_coordinates_of_chars, ALL_coordinates_of_cutted_chars)

    counter = 0
    chars = []
    for rowIndex in range(len(ALL_images_of_cutted_chars)):
        for colIndex in range(len(ALL_images_of_cutted_chars[rowIndex])):
            char = Char.Char()
            char.number = counter
            char.setSizeByCoordinates(ALL_coordinates_of_cutted_chars[rowIndex][colIndex][0],
                                      ALL_coordinates_of_cutted_chars[rowIndex][colIndex][1])
            char.coordinate = ALL_coordinates_of_chars[rowIndex][colIndex]
            if [rowIndex, colIndex] in spaceInside:
                char.space = True
            char.img = ALL_images_of_cutted_chars[rowIndex][colIndex]
            chars.append(char)
            counter = counter + 1
    #chars[0].showImage()

    if len(chars) > 0:
        #   WALSH
        walsh.resizeChars(chars)
        walsh.setVectors(chars)

        if LEARN:
            learning.learn(chars)
        else:
            doit.setValues(chars, FONT)
            doit.printText(chars)
    else:
        print('A kepen nem talalhato olvashato karakter')
        cv.imshow('Filtered', filtered)


if __name__ == "__main__":
    main()
    cv.waitKey()
