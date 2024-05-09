import utils.paths as paths
import json

morseFile = open(paths.get_path(__file__) + "morse.json")
morseTable = json.load(morseFile)

morseFile.close()

def parse_string_to_morse(msg: str):
    morseString = ""
    msg = msg.lower()
    for letter in msg:
        if letter == " ":
            morseString += "  "
        else:
            morseString += parse_letter_to_morse(letter)
            morseString += " "
    return morseString


def parse_letter_to_morse(letter: str):
    morseLetterString = ""
    try:
        morseLetterString = morseTable[letter]
    except:
        morseLetterString = "$"
    return morseLetterString
