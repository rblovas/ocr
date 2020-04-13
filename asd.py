#!/usr/bin/env python3
from __future__ import print_function

import argparse
import copy

import cv2 as cv
import numpy as np


def main():
    # get image
    img = get_image()

    # img grayscale
    grayscaled = grayscale(img)

    # img filter
    filtered = filter(grayscaled, 3)
    # cv.imshow('After filter', filtered)

    # szegmentalas

    #   HORIZONTAL: get rows
    rows = horizontalCut(filtered)
    coordinates_of_rows = rows[0]
    img_of_the_rows = rows[1]

    #   VERTICAL: get first cut of chars in all rows
    ALL_coordinates_of_chars = []
    ALL_images_of_chars = []
    for row in range(len(coordinates_of_rows)):
        cut = verticalCut(img_of_the_rows[row])
        ALL_coordinates_of_chars.append(cut[0])
        ALL_images_of_chars.append(cut[1])

    ALL_coordinates_of_cutted_chars = []
    ALL_images_of_cutted_chars = []
    for row in range(len(coordinates_of_rows)):  # minden sorban
        ALL_coordinates_of_cutted_chars.append([])
        ALL_images_of_cutted_chars.append([])
        for col in range(len(ALL_coordinates_of_chars[row])):  # minden sorban található char
            cut = horizontalCut(ALL_images_of_chars[row][col])

            new_cut = []
            if len(cut[0]) > 1:
                new_cut = solveSpaceInsideChars(cut)
            else:
                new_cut.append(cut[0][0])
                new_cut.append(cut[1][0])

            ALL_coordinates_of_cutted_chars[row].append(new_cut[0])
            ALL_images_of_cutted_chars[row].append(new_cut[1])

    cv.imshow('Show a char', ALL_images_of_cutted_chars[1][1])

    addBorder(filtered, coordinates_of_rows, ALL_coordinates_of_chars, ALL_coordinates_of_cutted_chars)


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
    cv.imshow('asd', new_cut[1])

    return new_cut


def addBorder(p_img, p_row_coordinates, p_all_col_coordinates, ALL_coordinates_of_cutted_chars):
    img = copy.copy(p_img)
    rows = img.shape[0]
    cols = img.shape[1]

    for row_coordinate in p_row_coordinates:
        row_index = p_row_coordinates.index(row_coordinate)
        for col_coordinate in p_all_col_coordinates[row_index]:
            col_index = p_all_col_coordinates[row_index].index(col_coordinate)

            newRowrangeStart = row_coordinate[0] + ALL_coordinates_of_cutted_chars[row_index][col_index][0]
            newRowrangeEnd = row_coordinate[0] + ALL_coordinates_of_cutted_chars[row_index][col_index][1]
            for row in range(newRowrangeStart, newRowrangeEnd):
                img[row, col_coordinate[0]] = 0
                img[row, col_coordinate[1]] = 0
            for col in range(col_coordinate[0], col_coordinate[1]):
                img[newRowrangeStart, col] = 0
                img[newRowrangeEnd, col] = 0

    cv.imshow('asd', img)


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


def filter(p_img, n):
    img = copy.copy(p_img)
    rows = img.shape[0]
    cols = img.shape[1]

    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            color_sum = int(p_img[i - 1, j - 1]) + int(p_img[i - 1, j]) + int(p_img[i - 1, j + 1]) + int(
                p_img[i, j - 1]) + int(p_img[i, j + 1]) + int(p_img[i + 1, j - 1]) + int(p_img[i + 1, j]) + int(
                p_img[i + 1, j + 1])

            # ha több mint n fehér van körülötte
            if color_sum > n * 255:
                img[i, j] = 255
            else:
                img[i, j] = 0
    return img


def grayscale(img):
    src = img
    # Convert the image to Gray
    src_gray = cv.cvtColor(src, cv.COLOR_RGB2GRAY)
    _, dst = cv.threshold(src_gray, 200, 255, 0)
    # cv.imshow('Grayscaled img', dst)
    return dst


def get_image():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='Path to input image.', default='test3.png')
    args = parser.parse_args()
    src = cv.imread(cv.samples.findFile(args.input))

    if src is None:
        print('Could not open or find the image: ', args.input)
        exit(0)
    return src


if __name__ == "__main__":
    main()
    cv.waitKey()
