from random import randint
from threading import Thread
from time import sleep, time
from phue import Bridge
from utils.decorators import *
from utils.objects.extension import Extension


# Hue: 7227
# Sat: 223
# ct: 494

class PHue(Extension):
    def __init__(self, host=""):
        default_settings = {"IP": host}
        settings = self.get_extension_settings(default_settings)
        self.bridge = Bridge(settings["IP"])

    def set_light_state(self, ids, on: bool = None, bri: int = None, hue: int = None, sat: int = None, transitiontime: int = None):
        cmds = {}
        if on is not None:
            cmds["on"] = on
        if bri is not None:
            cmds["bri"] = bri
        if hue is not None:
            cmds["hue"] = hue
        if sat is not None:
            cmds["sat"] = sat
        if transitiontime is not None:
            cmds["transitiontime"] = transitiontime
            if transitiontime < 4 and on is True and bri is None:
                cmds["bri"] = 255
        self.bridge.set_light(ids, cmds)

    @include_put
    def on(self, ids, transitiontime=0):
        self.set_light_state(ids, on=True, transitiontime=transitiontime)

    @include_put
    def off(self, ids, transitiontime=0):
        self.set_light_state(ids, on=False, transitiontime=transitiontime)

    @include_put
    def temp_on(self, ids, transitiontime=0):
        self.set_light_state(ids, bri=255, transitiontime=transitiontime)

    @include_put
    def temp_off(self, ids, transitiontime=0):
        self.set_light_state(ids, bri=0, transitiontime=transitiontime)

    @include_put
    def set_to_base_color(self, ids, transitiontime=4):
        self.bridge.set_light(
            ids, self.get_base_color_command(255, transitiontime))

    def start_flicker(self, ids, duration=3, frequency=1):
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

    def start_color_switch(self, ids, duration=3, transitiontime=1, waitTime=0.5):
        Thread(target=self.__color_switch, args=(
            ids, duration, transitiontime, waitTime)).start()

    def __color_switch(self, ids, duration, transitiontime, waitTime):
        startTime = time()
        while (time() - startTime) < duration:
            self.set_light_state(ids, bri=255, hue=randint(0, 65535), sat=randint(
                0, 255), transitiontime=transitiontime)
            sleep(waitTime)
        self.bridge.set_light(ids, self.get_base_color_command(0))

    def start_pulse(self, ids, duration=3, frequency=0.5, stepCount=10, minBri=100, maxBri=255):
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

    def get_base_color_command(self, bri=255, transitiontime=4):
        cmds = {}
        if bri != None:
            cmds["bri"] = bri
        cmds["ct"] = 343
        cmds["hue"] = 8632
        cmds["sat"] = 117
        cmds["transitiontime"] = transitiontime
        return cmds

    @include_get
    def get_lights(self):
        return self.bridge.lights

    @include_get
    def get_data(self):
        data = {}
        for light in self.bridge.lights:
            dataIdName = self.get_extension_name() + "_" + str(light.light_id)
            data[dataIdName] = 1 if light.on else 0
        return data