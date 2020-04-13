#!/usr/bin/env python3
from __future__ import print_function

import argparse
import copy

import cv2 as cv


def main():
    # get image
    img = get_image()

    # img grayscale
    grayscaled = grayscale(img)

    # img filter
    filtered = filter(grayscaled, 3)
    # cv.imshow('After filter', filtered)

    # szegmentalas
    #   get rows
    img_rows = get_image_rows(filtered)
    # print(img_rows)

    #   get chars
    img_chars = get_image_chars(filtered, img_rows)
    # print(img_chars)

    #   show where is the chars
    img_with_borders = add_char_border_to_the_image(filtered, img_rows, img_chars)
    cv.imshow('After border', img_with_borders)


def add_char_border_to_the_image(p_img, img_rows, img_chars):
    img = copy.copy(p_img)
    rows = img.shape[0]
    cols = img.shape[1]

    for img_row in range(len(img_rows)):
        for char_col in img_chars[img_row]:

            for char_rows in range(img_rows[img_row][0], img_rows[img_row][1]):
                img[char_rows][char_col[0]] = 0
                img[char_rows][char_col[1]] = 0

            for char_col in range(char_col[0], char_col[1]):
                img[img_rows[img_row][0]][char_col] = 0
                img[img_rows[img_row][1]][char_col] = 0

    return img


def get_image_chars(p_img, img_rows):
    img = copy.copy(p_img)
    rows = img.shape[0]
    cols = img.shape[1]
    img_chars = []

    inchar = 0
    for rowIndex in range(len(img_rows)):
        img_row = img_rows[rowIndex]
        img_chars.append([])
        for pixelCol in range(cols):
            hasBlack = 0
            for pixelRow in range(img_row[0], img_row[1]):
                if img[pixelRow, pixelCol] == 0:
                    hasBlack = 1

            if hasBlack:
                if inchar == 0:
                    img_chars[rowIndex].append([pixelCol])
                    inchar = 1
            else:
                if inchar == 1:
                    img_chars[rowIndex][len(img_chars[rowIndex]) - 1].append(pixelCol - 1)
                    inchar = 0

    return img_chars


def get_image_rows(p_img):
    img = copy.copy(p_img)
    rows = img.shape[0]
    cols = img.shape[1]
    img_rows = []

    inrow = 0

    for row in range(rows):
        hasBlack = 0
        for col in range(cols):
            if img[row, col] == 0:
                hasBlack = 1

        if hasBlack:
            if inrow == 0:
                img_rows.append([row])
                inrow = 1
        else:
            if inrow == 1:
                img_rows[len(img_rows) - 1].append(row - 1)
                inrow = 0

    return img_rows


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
