import json
import heapq


def printText(chars):
    text = ''
    space_width = (chars[0].coordinate[1] - chars[0].coordinate[0]) * 0.4
    for i in range(len(chars)):
        char = chars[i]
        if i > 0 and (char.coordinate[0] - chars[i - 1].coordinate[1]) > space_width:
            text = text + ' '
        if i > 0 and (char.coordinate[0] < chars[i - 1].coordinate[1]):
            text = text + '\n'
        if i > 0 and (text[-1] != ' ' and char.value == 'I'):
            char.value = 'l'
        if (char.value == 'l' or char.value == 'I') and char.space:
            char.value = 'i'
        text = text + char.value
    print(text)

    file = open("text.txt", "w")
    file.write(text)
    file.close()


def setValues(chars, p_font='arial'):
    with open('database/' + p_font + '.json') as f:
        abc = json.load(f)

    max = chars[0].size
    min = chars[0].size

    for char in chars:
        if char.size > max:
            max = char.size
        if char.size < min:
            min = char.size

    middle = ((max + min) / 2)

    similars = ['C', 'O', 'S', 'V', 'W', 'X', 'Z', 'c', 'o', 's', 'v', 'w', 'x', 'z']
    for char in chars:
        min = -1
        min_char = ''

        for abc_element in abc:
            data = abc[abc_element]
            tmp = compare(char.vector, data['vector'])
            if min == -1 or tmp < min:
                min = tmp
                min_char = data['value']
        char.value = min_char

        if char.value in similars:
            if char.size > middle:
                char.value = char.value.upper()
            else:
                char.value = char.value.lower()


def compare(char, abc_char):
    sum = 0
    for i in range(len(char)):
        sum += abs(char[i] - abc_char[i])
    return sum
