from time import sleep
from threading import Thread

from utils.decorators import *
from utils.objects.module import Module

from modules.managers.morse import morseCode

import modules
from modules.extensions.spotify import Spotify
from modules.extensions.phue_v2.phue_v2 import PHue

# Intervals
SHORT_DURATION = 0.5
LONG_DURATION = 2
SHORT_PAUSE_DURATION = 0.75
LONG_PAUSE_DURATION = 1.5
CYCLE_PAUSE_DURATION = 10

phueLights = {9, 10}

class Morse(Module):
    spotifyExt: Spotify
    phueExt: PHue

    def __init__(self):
        self.spotifyExt = modules.get_module("spotify")
        self.phueExt = modules.get_module("phue")

    def init_lights(self):
        self.phueExt.set_to_base_color(phueLights, 0)
        self.phueExt.on(phueLights)
        self.phueExt.temp_off(phueLights)

    def calculate_duration(self, msg: str):
        pauseDuration = msg.count(" ") * LONG_PAUSE_DURATION
        shortDuration = msg.count(".") * (SHORT_DURATION + SHORT_PAUSE_DURATION)
        longDuration = msg.count("-") * (LONG_DURATION + SHORT_PAUSE_DURATION)
        return pauseDuration + shortDuration + longDuration

    def print_progress_bar(self, iteration, total, prefix='', suffix='', decimals=0, length=50, fill='█', printEnd="\r"):

        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration / total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r|{bar}| {percent}%', end=printEnd)
        if iteration == total:
            print()

    def show_morse(self, msg: str, cycles=1):
        morseString = morseCode.parse_string_to_morse(msg)
        totalDuration = self.calculate_duration(morseString) * cycles
        print(f"Total Duration (with {cycles} Cycles): {totalDuration}s")
        passedDuration = 0
        for _ in range(cycles):
            self.print_progress_bar(passedDuration, totalDuration)
            for char in morseString:
                if (char == "  "):
                    sleep(LONG_DURATION + LONG_PAUSE_DURATION)
                    passedDuration += (LONG_DURATION + LONG_PAUSE_DURATION)
                if (char == " "):
                    sleep(LONG_PAUSE_DURATION)
                    passedDuration += (LONG_PAUSE_DURATION)
                elif (char == "."):
                    self.show(SHORT_DURATION)
                    sleep(SHORT_PAUSE_DURATION)
                    passedDuration += (SHORT_DURATION + SHORT_PAUSE_DURATION)
                elif (char == "-"):
                    self.show(LONG_DURATION)
                    sleep(SHORT_PAUSE_DURATION)
                    passedDuration += (LONG_DURATION + SHORT_PAUSE_DURATION)
                self.print_progress_bar(passedDuration, totalDuration)
            sleep(CYCLE_PAUSE_DURATION)
        self.lights_off()

    def lights_on(self):
        Thread(target=self.phueExt.temp_on, args=(phueLights)).start()
        Thread(target=self.tuyaExt.on, args=(tuyaLights)).start()

    def lights_off(self):
        Thread(target=self.phueExt.temp_off, args=(phueLights)).start()
        Thread(target=self.tuyaExt.off, args=(tuyaLights)).start()

    def show(self, duration:float):
        Thread(target=self.lights_on).start()
        sleep(duration)
        Thread(target=self.lights_off).start()

    @include_put
    async def run_request(self, message, cylces=1):
        Thread(target=self.show_morse, args=(message, cylces)).start()