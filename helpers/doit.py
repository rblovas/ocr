import json

def printText(chars):
    text = ''
    for char in chars:
        text = text + char.value
    print(text)

def setValues(chars):
    with open('database/abc.json') as f:
        abc = json.load(f)

    for char in chars:
        min_compare_value = -1
        min_abc_char = ''
        for abc_element in abc:
            data = abc[abc_element]
            tmp = compare(char.vector, data['vector'])
            if min_compare_value == -1:
                min_compare_value = tmp
                min_abc_char = data['value']
            else:
                if tmp < min_compare_value:
                    min_compare_value = tmp
                    min_abc_char = data['value']
        char.value = min_abc_char

def compare(char, abc_char):
    sum = 0
    for i in range(len(char)):
        sum += abs(char[i] - abc_char[i])
    return sum
