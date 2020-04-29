import copy
import cv2 as cv


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

    cv.imshow('Borders', img)


def showInMovedWindow(winname, img, x, y):
    cv.namedWindow(winname)  # Create a named window
    cv.moveWindow(winname, x, y)  # Move it to (x,y)
    cv.imshow(winname, img)
