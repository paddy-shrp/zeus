from os.path import exists
import shutil
from threading import Thread
from time import time, sleep
import tinytuya as tuya
import json

# This cannot be changed later on, else the data will be useless
EXTENSION_NAME = "tuya"


class TuyaExtension:
    def __init__(self):
        devices = self.scanDevices()
        self.deviceList = []
        for device in devices:
            _device = tuya.Device(
                device["id"], device["ip"], device["key"])
            _device.set_version(3.3)
            _device.set_socketPersistent(True)
            self.deviceList.append(_device)

    def scanDevices(self):
        destPath = "./credentials/snapshot.json"
        if not exists(destPath):
            tuya.scan()
            shutil.move("./snapshot.json", destPath)
        return json.load(open(destPath))["devices"]

    def setLightState(self, ids, on: bool):
        if isinstance(ids, int):
            Thread(target=self.deviceList[id].set_value, args=(1, on,)).start()
        else:
            for id in ids:
                Thread(target=self.deviceList[id].set_value, args=(
                    1, on,)).start()

    def on(self, ids):
        self.setLightState(ids, True)

    def off(self, ids):
        self.setLightState(ids, False)

    def startFlicker(self, ids, duration=3, frequency=1):
        Thread(target=self.__flicker, args=(
            ids, duration, frequency)).start()

    def __flicker(self, ids, duration, frequency):
        startTime = time()
        fTime = frequency / 2
        while (time() - startTime) < duration:
            self.on(ids)
            sleep(fTime)
            self.off(ids)
            sleep(fTime)
        self.off(ids)

    def getData(self):
        data = {}
        for device in self.deviceList:
            try:
                d_status = device.status()
                dataIdName = EXTENSION_NAME + "_" + d_status["devId"]
                data[dataIdName] = 1 if d_status["dps"]["1"] else 0
            except:
                pass
        return data
