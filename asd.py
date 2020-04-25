#!/usr/bin/env python3


from __future__ import print_function

from helpers import learning
from helpers import preprocess
from helpers import segment
from helpers import walsh
from helpers import showSteps
from helpers import Char
from helpers import doit

import argparse
import copy

import cv2 as cv
import numpy as np


def main():
    #   PREPROCESS
    # img = preprocess.get_image('learn.png')
    img = preprocess.get_image('helloworld.png')
    grayscaled = preprocess.grayscale(img)
    filtered = preprocess.filter(grayscaled, 3)

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
    for row in range(len(coordinates_of_rows)):
        ALL_coordinates_of_cutted_chars.append([])
        ALL_images_of_cutted_chars.append([])
        for col in range(len(ALL_coordinates_of_chars[row])):
            cut = segment.horizontalCut(ALL_images_of_chars[row][col])
            new_cut = []
            if len(cut[0]) > 1:
                new_cut = segment.solveSpaceInsideChars(cut)
            else:
                new_cut.append(cut[0][0])
                new_cut.append(cut[1][0])

            ALL_coordinates_of_cutted_chars[row].append(new_cut[0])
            ALL_images_of_cutted_chars[row].append(new_cut[1])

    counter = 0
    chars = []
    for rowIndex in range(len(ALL_images_of_cutted_chars)):
        for colIndex in range(len(ALL_images_of_cutted_chars[rowIndex])):
            char = Char.Char()
            char.number = counter
            char.setSizeByCoordinates(ALL_coordinates_of_cutted_chars[rowIndex][colIndex][0], ALL_coordinates_of_cutted_chars[rowIndex][colIndex][1])
            char.img = ALL_images_of_cutted_chars[rowIndex][colIndex]
            chars.append(char)
            counter = counter + 1

    #   WALSH
    walsh.resizeChars(chars)
    walsh.setVectors(chars)
    # chars[0].printData()

    # learning.learn(chars)
    doit.setValues(chars)
    doit.printText(chars)


if __name__ == "__main__":
    main()
    cv.waitKey()
