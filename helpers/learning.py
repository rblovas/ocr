from helpers import Char
import cv2 as cv
import json

def learn(chars):
    for char in chars:
        char.showImage()
        cv.waitKey(300)
        char.value = input('What is this character?')
        char.printData()
    cv.destroyAllWindows()

    dict = {}
    for char in chars:
        dict[char.number] = {
            # 'size': char.size,
            'vector': char.vector,
            # 'img': char.img.tolist(),
            'value': char.value,
        }
    str = json.dumps(dict, indent=4)
    with open('database/db.json', 'w+') as outfile:
        outfile.write(str)
