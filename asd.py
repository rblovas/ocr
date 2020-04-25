#!/usr/bin/env python3


from __future__ import print_function

from helpers import learning
from helpers import preprocess
from helpers import segment
from helpers import walsh
from helpers import showSteps
from helpers import Char

import argparse
import copy

import cv2 as cv
import numpy as np


def main():
    #   PREPROCESS
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
    for row in range(len(coordinates_of_rows)):  # minden sorban
        ALL_coordinates_of_cutted_chars.append([])
        ALL_images_of_cutted_chars.append([])
        for col in range(len(ALL_coordinates_of_chars[row])):  # minden sorban található char
            cut = segment.horizontalCut(ALL_images_of_chars[row][col])
            new_cut = []
            if len(cut[0]) > 1:
                new_cut = segment.solveSpaceInsideChars(cut)
            else:
                new_cut.append(cut[0][0])
                new_cut.append(cut[1][0])

            ALL_coordinates_of_cutted_chars[row].append(new_cut[0])
            ALL_images_of_cutted_chars[row].append(new_cut[1])
    cv.imshow('Show a char', ALL_images_of_cutted_chars[1][2])
    showSteps.addBorder(filtered, coordinates_of_rows, ALL_coordinates_of_chars, ALL_coordinates_of_cutted_chars)

    #   WALSH
    resizedChars = walsh.resizeChars(ALL_images_of_cutted_chars)
    # cv.imshow('Show a char', resizedChars[0][1])
    walshImages = walsh.generateWalshImages()
    sajatvektorok = walsh.osszesSajatVetkor(resizedChars, walshImages)
    print(sajatvektorok)
    # char = Char.Char(1, 2, ['asd'], ['asd'])
    # char.printData()



if __name__ == "__main__":
    main()
    cv.waitKey()
