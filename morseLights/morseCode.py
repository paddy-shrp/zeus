import json

morseFile = open("./morseLights/morse.json")
morseTable = json.load(morseFile)

morseFile.close()


def parseStringToMorseCode(msg: str):
    morseString = ""
    msg = msg.lower()
    for letter in msg:
        if letter == " ":
            morseString += "  "
        else:
            morseString += parseLetterToMorse(letter)
            morseString += " "
    return morseString


def parseLetterToMorse(letter: str):
    morseLetterString = ""
    try:
        morseLetterString = morseTable[letter]
    except:
        morseLetterString = "$"
    return morseLetterString
