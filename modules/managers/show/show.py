from threading import Thread
import time
import ast
from time import sleep
from os.path import exists

from utils.objects.module import Module
from utils.decorators import *
import modules

# Make dynamic
PHUE_LIGHT_IDS = {3, 4, 5, 6, 8}
TUYA_LIGHT_IDS = {0, 1, 2}

class Show(Module):
    def __init__(self):
        mds = modules.get_modules()
        self.spotifyExt = modules.get_module("spotify")
        self.phueExt = modules.get_module("phue")
        self.tuyaExt = modules.get_module("tuya")
        self.phue_light_ids = PHUE_LIGHT_IDS
        self.tuya_light_ids = TUYA_LIGHT_IDS

    def init_lights(self):
        self.phueExt.set_to_base_color(self.phue_light_ids, 0)
        self.phueExt.on(self.phue_light_ids)
        self.phueExt.temp_off(self.phue_light_ids)
        self.tuyaExt.set_light_state(self.tuya_light_ids, on=False)

    # Converts the file into a readable command dictionary
    def read_file(self, path):
        timeCommands = {}
        showFile = open(path, "r")

        currentCMD = None
        commands = []
        for line in showFile:
            leading_spaces = len(line) - len(line.lstrip())
            if leading_spaces == 0:
                if currentCMD is not None:
                    timeCommands[currentCMD] = commands
                currentCMD = line.replace(":", "").replace("\n", "").strip()
                commands = []
            elif leading_spaces == 4:
                commands.append(line.replace("\n", "").strip())
        timeCommands[currentCMD] = commands
        return timeCommands


    def execute_command(self, cmd, args):
        argsCount = len(args)

        if argsCount <= 1:
            return

        match cmd:
            case "phue":
                lights = {}
                if args[0] == "*":
                    lights = self.phue_light_ids.copy()
                else:
                    lights = ast.literal_eval(args[0])
                match args[1]:
                    case "on":
                        transitiontime = 0
                        if argsCount > 2:
                            transitiontime = int(args[2])
                        self.phueExt.temp_on(lights, transitiontime)
                    case "off":
                        transitiontime = 0
                        if argsCount > 2:
                            transitiontime = int(args[2])
                        self.phueExt.temp_off(lights, transitiontime)
                    case "fon":
                        transitiontime = 0
                        if argsCount > 2:
                            transitiontime = int(args[2])
                        self.phueExt.on(lights, transitiontime)
                    case "foff":
                        transitiontime = 0
                        if argsCount > 2:
                            transitiontime = int(args[2])
                        self.phueExt.off(lights, transitiontime)
                    case "flicker":
                        duration = 3
                        if argsCount > 2:
                            duration = float(args[2])
                        frequency = 1
                        if argsCount > 3:
                            frequency = float(args[3])
                        self.phueExt.start_flicker(lights, duration, frequency)
                    case "colorswitch":
                        duration = 3
                        if argsCount > 2:
                            duration = float(args[2])
                        transitiontime = 1
                        if argsCount > 3:
                            transitiontime = int(args[3])
                        waitTime = 0.5
                        if argsCount > 4:
                            waitTime = float(args[4])
                        self.phueExt.start_color_switch(
                            lights, duration, transitiontime, waitTime)
            case "tuya":
                lights = {}
                if args[0] == "*":
                    lights = self.tuyaLights.copy()
                else:
                    lights = ast.literal_eval(args[0])
                match args[1]:
                    case "on":
                        self.tuyaExt.on(lights)
                    case "off":
                        self.tuyaExt.off(lights)
                    case "flicker":
                        duration = 3
                        if argsCount > 2: duration = float(args[2])
                        frequency = 1
                        if argsCount > 3: frequency = float(args[3])
                        self.tuyaExt.start_flicker(lights, duration, frequency)
            case "spotify":
                match args[0]:
                    case "play":
                        if argsCount < 2:
                            return
                        uri = args[1]
                        self.spotifyExt.play(uri)
                    case "pause":
                        self.spotifyExt.pause()
                    case "resume":
                        self.spotifyExt.resume()
                    case "volume":
                        if argsCount < 2:
                            return
                        volume = int(args[1])
                        self.spotifyExt.set_volume(volume)
                return

    
    def play_file(self, path, wait=0.5):
        self.init_lights()
        commands = self.read_file(path)
        sleep(wait)

        # Execute start command
        if "start" in commands:
            for command in commands["start"]:
                splits = command.split(" ")
                Thread(target=self.execute_command, args=(splits[0], splits[1:])).start()
            commands.pop("start")

        # Exectue all the other commands by timestamp
        startTime = time.time()
        timestamps = list(commands.keys())
        while len(timestamps) > 0:
            elapsedTime = time.time() - startTime
            key = timestamps[0]
            if elapsedTime >= float(key):
                for command in commands[key]:
                    splits = command.split(" ")
                    Thread(target=self.executeCommand, args=(
                        splits[0], splits[1:])).start()

                commands.pop(key)
                timestamps.pop(0)

            sleep(0.01)

    @include_put
    async def play_file_request(self, path):
        if not exists(path): return 400
        Thread(target=self.play_file, args=(path)).start()