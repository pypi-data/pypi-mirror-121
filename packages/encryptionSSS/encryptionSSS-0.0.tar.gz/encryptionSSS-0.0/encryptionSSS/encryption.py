from coder import AdditionalElements



def encode(text):
    shifter = {"a": 20, "b": 30, "c": 40, "d": 55, "e": 66, "f": 75, "g": 68, "h": 36, "i": 44, "j": 58, "k": 185,
               "l": 399, "m": 156, "n": 157, "o": 158, "p": 159, "q": 160, "r": 1, "s": 9, "t": 8, "u": 3, "v": 5,
               "w": 16, "x": 26, "y": 71, "z": 201, " ": 350}

    NSs = [20, 11, 16, 21, 23, 2]
    letters = []
    encodedLetters = []
    encodedFraze = ""

    letter = ''
    text += " "

    for el in text:
        if el == " ":
            letters.append(letter)
            letter = ""
        else:
            letter += el

    NSnum = 0
    for let in letters:
        if NSnum == 6:
            NSnum = 0
        encodedletter = AdditionalElements.toDec(let, NSs[NSnum])
        encodedLetters.append(encodedletter)
        NSnum += 1
    for encodedletter in encodedLetters:
        encodedFraze += AdditionalElements.get_key(shifter, encodedletter)
    return encodedFraze


def code(text):
    ret = ''
    ret2 = ''

    NSs = [20, 11, 16, 21, 23, 2]

    shifter = {"a": 20, "b": 30, "c": 40, "d": 55, "e": 66, "f": 75, "g": 68, "h": 36, "i": 44, "j": 58, "k": 185,
               "l": 399, "m": 156, "n": 157, "o": 158, "p": 159, "q": 160, "r": 1, "s": 9, "t": 8, "u": 3, "v": 5,
               "w": 16, "x": 26, "y": 71, "z": 201, " ": 350}
    num = 0
    for i in text:
        NSel = NSs[num]

        s = AdditionalElements.toNS(shifter.get(i, 99), NSel)
        ret = ret + str(s) + " "
        ret2 += " " + str(NSel)
        num += 1
        if num == 6:
            num = 0
    return ret[:len(ret)-1]
