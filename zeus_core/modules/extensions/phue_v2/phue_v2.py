from random import randint
from threading import Thread
from time import sleep, time

from utils.decorators import *
from utils.objects.module import Module

from modules.extensions.phue_v2.Bridge import Bridge

class PHue(Module):
    logging_frequency = 0

    def __init__(self, host=""):
        default_settings = {"IP": host}
        settings = self.get_module_settings(default_settings)
        self.bridge = Bridge(settings["IP"])

    def set_light_state(self, ids, on = None, bri = None, color = None, transitiontime = None):
        if transitiontime is not None:
            if transitiontime < 4 and on is True and bri is None:
                bri = 255
        self.bridge.set_light_state(ids, on, bri, color, transitiontime)

    @include_put
    def on(self, ids, transitiontime:int = None):
        return self.set_light_state(ids, on=True, transitiontime=transitiontime)

    @include_put
    def off(self, ids, transitiontime:int = None):
        return self.set_light_state(ids, on=False, transitiontime=transitiontime)

    @include_put
    def temp_on(self, ids, transitiontime:int = None):
        return self.set_light_state(ids, bri=255, transitiontime=transitiontime)

    @include_put
    def temp_off(self, ids, transitiontime:int = None):
        return self.set_light_state(ids, bri=0, transitiontime=transitiontime)

    @include_put
    def set_to_base_color(self, ids, transitiontime:int = 4):
        return self.set_light_state(ids, bri=255, color=[255, 255, 255], transitiontime=transitiontime)

    @include_put
    def start_flicker(self, ids, duration:int = 3, frequency:int = 1):
        Thread(target=self.__flicker, args=(
            ids, duration, frequency)).start()

    def __flicker(self, ids, duration, frequency):
        startTime = time()
        fTime = frequency / 2
        while (time() - startTime) < duration:
            self.temp_on(ids)
            sleep(fTime)
            self.temp_off(ids)
            sleep(fTime)
        self.temp_off(ids)

    @include_put
    def start_color_switch(self, ids, duration:int = 3, transitiontime:int = 1, waitTime:float = 0.5):
        Thread(target=self.__color_switch, args=(
            ids, duration, transitiontime, waitTime)).start()

    def __color_switch(self, ids, duration, transitiontime, waitTime):
        startTime = time()
        while (time() - startTime) < duration:
            self.set_light_state(ids, bri=255, color=self.get_random_color(), transitiontime=transitiontime)
            sleep(waitTime)
        self.set_to_base_color(ids)

    @include_put
    def start_pulse(self, ids, duration:int = 3, frequency:float = 0.5, stepCount:int = 10, minBri:int = 100, maxBri:int = 255):
        Thread(target=self.__pulse, args=(
            ids, duration, frequency, stepCount, minBri, maxBri)).start()

    def __pulse(self, ids, duration, frequency, stepCount, minBri, maxBri):
        startTime = time()
        fTime = frequency / 2
        stepTime = fTime / stepCount
        briStep = (maxBri-minBri) / stepCount
        while (time() - startTime) < duration:
            for step in range(stepCount):
                self.set_light_state(ids, bri=int(minBri + step * briStep))
                sleep(stepTime)
            for step in range(stepCount):
                self.set_light_state(ids, bri=int(maxBri - step * briStep))
                sleep(stepTime)
        self.temp_off(ids)

    @include_get
    def get_lights(self):
        return self.bridge.get_lights()

    @include_get
    def get_data(self):
        data = {}
        return data
    
    def get_random_color(self):
        return [randint(0, 255), randint(0, 255), randint(0, 255)]