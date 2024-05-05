from utils.decorators import *
from utils.objects.extension import Extension
import utils.credentials as credentials

import shutil
from threading import Thread
from time import time, sleep
import tinytuya as tuya

class Tuya(Extension):
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
        file_name = "snapshot.json"
        if not credentials.file_exists(file_name):
            tuya.scan()
            shutil.move("./snapshot.json", credentials.get_path(file_name))
        return credentials.get_credentials_json(file_name)["devices"]

    @include_put
    def set_light_state(self, ids, on: bool):
        if isinstance(ids, int):
            Thread(target=self.deviceList[id].set_value, args=(1, on,)).start()
        else:
            for id in ids:
                Thread(target=self.deviceList[id].set_value, args=(
                    1, on,)).start()

    @include_put
    def on(self, ids):
        self.set_light_state(ids, True)

    @include_put
    def off(self, ids):
        self.set_light_state(ids, False)

    @include_put
    def start_flicker(self, ids, duration=3, frequency=1):
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

    @include_get
    def get_data(self):
        data = {}
        return data