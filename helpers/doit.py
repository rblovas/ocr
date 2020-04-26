import json
import heapq

def printText(chars):
    text = ''
    for i in range(len(chars)):
        char = chars[i]
        if i > 0 and (char.coordinate[0] - chars[i-1].coordinate[1]) > 10:
            text = text + ' '
        if i > 0 and (char.coordinate[0] < chars[i-1].coordinate[1]):
            text = text + '\n'
        text = text + char.value
    print(text)

def setValues(chars):
    with open('database/abc.json') as f:
        abc = json.load(f)

    bigChars = {str(k): abc[str(k)] for k in range(0, 26)}
    smallChars = {str(k): abc[str(k)] for k in range(26, 52)}

    max = chars[0].size
    min = chars[0].size
    for char in chars:
        if char.size > max:
            max = char.size
        if char.size < min:
            min = char.size

    middle = (max+min)/2

    for char in chars:
        min = -1
        min_char = ''
        if char.size > middle:
            for abc_element in bigChars:
                data = abc[abc_element]
                tmp = compare(char.vector, data['vector'])
                if min == -1 or tmp < min:
                    min = tmp
                    min_char = data['value']
            char.value = min_char
        else:
            for abc_element in smallChars:
                data = abc[abc_element]
                tmp = compare(char.vector, data['vector'])
                if min == -1 or tmp < min:
                    min = tmp
                    min_char = data['value']
            char.value = min_char

def compare(char, abc_char):
    sum = 0
    for i in range(len(char)):
        sum += abs(char[i] - abc_char[i])
    return sum
