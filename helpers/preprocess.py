import argparse
import copy
import cv2 as cv


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
    _, dst = cv.threshold(src_gray, 125, 255, 0) #photohoz--> 125, többihez: 200
    # cv.imshow('Grayscaled img', dst)
    return dst


def get_image(p_img, p_font='arial'):

    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='Path to input image.', default='images/' + p_font + '/' + p_img + '.png')
    args = parser.parse_args()
    src = cv.imread(cv.samples.findFile(args.input))

    if src is None:
        print('Could not open or find the image: ', args.input)
        exit(0)
    return src