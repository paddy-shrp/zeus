from time import sleep
from threading import Thread
import morseCode
import json

# Intervals
SHORT_DURATION = 0.5
LONG_DURATION = 2
SHORT_PAUSE_DURATION = 0.75
LONG_PAUSE_DURATION = 1.5
CYCLE_PAUSE_DURATION = 10

# Extension Imports
from extensions.pHueLightsExtension import PHueExtension
from extensions.spotifyExtension import SpotifyExtension
from extensions.tuyaExtension import TuyaExtension

# Init Extensions
phueC = json.load(open("./credentials/phue-credentials.json"))
phueExt = PHueExtension(phueC["IP"])
tuyaExt = TuyaExtension()
spC = json.load(open("./credentials/spotify-credentials.json"))
spotifyExt = SpotifyExtension(
    spC["clientID"], spC["clientSecret"], spC["redirectUri"], spC["scopes"])


phueLights = {9, 10}
tuyaLights = {1}


def initLights():
    phueExt.setToStandardColor(phueLights, 0)
    phueExt.on(phueLights)
    phueExt.tempOff(phueLights)
    tuyaExt.off(tuyaLights)


def calculateDuration(msg: str):
    pauseDuration = msg.count(" ") * LONG_PAUSE_DURATION
    shortDuration = msg.count(".") * (SHORT_DURATION + SHORT_PAUSE_DURATION)
    longDuration = msg.count("-") * (LONG_DURATION + SHORT_PAUSE_DURATION)
    return pauseDuration + shortDuration + longDuration


def printProgressBar(iteration, total, prefix='', suffix='', decimals=0, length=50, fill='█', printEnd="\r"):

    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration / total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r|{bar}| {percent}%', end=printEnd)
    if iteration == total:
        print()


def showMessage(msg: str, cycles=1):
    morseString = morseCode.parseStringToMorseCode(msg)
    totalDuration = calculateDuration(morseString) * cycles
    print(f"Total Duration (with {cycles} Cycles): {totalDuration}s")
    passedDuration = 0
    for _ in range(cycles):
        printProgressBar(passedDuration, totalDuration)
        for char in morseString:
            if (char == "  "):
                sleep(LONG_DURATION + LONG_PAUSE_DURATION)
                passedDuration += (LONG_DURATION + LONG_PAUSE_DURATION)
            if (char == " "):
                sleep(LONG_PAUSE_DURATION)
                passedDuration += (LONG_PAUSE_DURATION)
            elif (char == "."):
                show(SHORT_DURATION)
                sleep(SHORT_PAUSE_DURATION)
                passedDuration += (SHORT_DURATION + SHORT_PAUSE_DURATION)
            elif (char == "-"):
                show(LONG_DURATION)
                sleep(SHORT_PAUSE_DURATION)
                passedDuration += (LONG_DURATION + SHORT_PAUSE_DURATION)
            printProgressBar(passedDuration, totalDuration)
        sleep(CYCLE_PAUSE_DURATION)

def lights_on():
    Thread(target=phueExt.tempOn, args=(phueLights)).start()
    Thread(target=tuyaExt.on, args=(tuyaLights)).start()

def lights_off():
    Thread(target=phueExt.tempOff, args=(phueLights)).start()
    Thread(target=tuyaExt.off, args=(tuyaLights)).start()

def show(duration:float):
    Thread(target=lights_on).start()
    sleep(duration)
    Thread(target=lights_off).start()

while True:
    print("Type in your message:")
    msg = input()
    print("Number of cycles:")
    cycles = int(input())
    showMessage(msg, cycles)
    phueExt.off(phueLights)