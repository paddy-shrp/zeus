from time import sleep
from threading import Thread
import morseCode as morse

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
phueExt = PHueExtension()
tuyaExt = TuyaExtension()
spotifyExt = SpotifyExtension()


phueLights = {9, 10}
tuyaLights = {1}


def init_lights():
    phueExt.set_to_base_color(phueLights, 0)
    phueExt.on(phueLights)
    phueExt.temp_off(phueLights)
    tuyaExt.off(tuyaLights)


def calculate_duration(msg: str):
    pauseDuration = msg.count(" ") * LONG_PAUSE_DURATION
    shortDuration = msg.count(".") * (SHORT_DURATION + SHORT_PAUSE_DURATION)
    longDuration = msg.count("-") * (LONG_DURATION + SHORT_PAUSE_DURATION)
    return pauseDuration + shortDuration + longDuration


def print_progress_bar(iteration, total, prefix='', suffix='', decimals=0, length=50, fill='█', printEnd="\r"):

    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration / total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r|{bar}| {percent}%', end=printEnd)
    if iteration == total:
        print()


def show_morse(msg: str, cycles=1):
    morseString = morse.parse_string_to_morse(msg)
    totalDuration = calculate_duration(morseString) * cycles
    print(f"Total Duration (with {cycles} Cycles): {totalDuration}s")
    passedDuration = 0
    for _ in range(cycles):
        print_progress_bar(passedDuration, totalDuration)
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
            print_progress_bar(passedDuration, totalDuration)
        sleep(CYCLE_PAUSE_DURATION)

def lights_on():
    Thread(target=phueExt.temp_on, args=(phueLights)).start()
    Thread(target=tuyaExt.on, args=(tuyaLights)).start()

def lights_off():
    Thread(target=phueExt.temp_off, args=(phueLights)).start()
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
    show_morse(msg, cycles)
    phueExt.off(phueLights)