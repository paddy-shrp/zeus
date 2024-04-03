from random import randint
from threading import Thread
from time import sleep, time
from phue import Bridge
from os.path import exists
import json

# This cannot be changed later on, else the data will be useless
EXTENSION_NAME = "phue"
PHUE_C_PATH = "./credentials/phue-credentials.json"

# Hue: 7227
# Sat: 223
# ct: 494

class PHueExtension:
    def __init__(self, host):
        if not exists(PHUE_C_PATH):
            phueC = {"IP": host}
            with open(PHUE_C_PATH, "w") as file:
                json.dump(phueC, file, indent=4)
        self.bridge = Bridge(host)

    def setLightState(self, ids, on: bool = None, bri: int = None, hue: int = None, sat: int = None, transitiontime: int = None):
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

    def on(self, ids, transitiontime=0):
        self.setLightState(ids, on=True, transitiontime=transitiontime)

    def off(self, ids, transitiontime=0):
        self.setLightState(ids, on=False, transitiontime=transitiontime)

    def tempOn(self, ids, transitiontime=0):
        self.setLightState(ids, bri=255, transitiontime=transitiontime)

    def tempOff(self, ids, transitiontime=0):
        self.setLightState(ids, bri=0, transitiontime=transitiontime)

    def setToStandardColor(self, ids, transitiontime=4):
        self.bridge.set_light(
            ids, self.__getStandardColorCommand(255, transitiontime))

    def startFlicker(self, ids, duration=3, frequency=1):
        Thread(target=self.__flicker, args=(
            ids, duration, frequency)).start()

    def __flicker(self, ids, duration, frequency):
        startTime = time()
        fTime = frequency / 2
        while (time() - startTime) < duration:
            self.tempOn(ids)
            sleep(fTime)
            self.tempOff(ids)
            sleep(fTime)
        self.tempOff(ids)

    def startColorSwitch(self, ids, duration=3, transitiontime=1, waitTime=0.5):
        Thread(target=self.__colorSwitch, args=(
            ids, duration, transitiontime, waitTime)).start()

    def __colorSwitch(self, ids, duration, transitiontime, waitTime):
        startTime = time()
        while (time() - startTime) < duration:
            self.setLightState(ids, bri=255, hue=randint(0, 65535), sat=randint(
                0, 255), transitiontime=transitiontime)
            sleep(waitTime)
        self.bridge.set_light(ids, self.__getStandardColorCommand(0))

    def startPulse(self, ids, duration=3, frequency=0.5, stepCount=10, minBri=100, maxBri=255):
        Thread(target=self.__pulse, args=(
            ids, duration, frequency, stepCount, minBri, maxBri)).start()

    def __pulse(self, ids, duration, frequency, stepCount, minBri, maxBri):
        startTime = time()
        fTime = frequency / 2
        stepTime = fTime / stepCount
        briStep = (maxBri-minBri) / stepCount
        while (time() - startTime) < duration:
            for step in range(stepCount):
                self.setLightState(ids, bri=int(minBri + step * briStep))
                sleep(stepTime)
            for step in range(stepCount):
                self.setLightState(ids, bri=int(maxBri - step * briStep))
                sleep(stepTime)
        self.tempOff(ids)

    def getLights(self):
        return self.bridge.lights

    def __getStandardColorCommand(self, bri=255, transitiontime=4):
        cmds = {}
        if bri != None:
            cmds["bri"] = bri
        cmds["ct"] = 343
        cmds["hue"] = 8632
        cmds["sat"] = 117
        cmds["transitiontime"] = transitiontime
        return cmds

    def getData(self):
        data = {}
        for light in self.bridge.lights:
            dataIdName = EXTENSION_NAME + "_" + str(light.light_id)
            data[dataIdName] = 1 if light.on else 0
        return data
