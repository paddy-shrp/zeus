from threading import Thread
import time
import json
import ast
from time import sleep

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


phueLights = {3, 4, 5, 6, 8}
tuyaLights = {0, 1, 2}


def initLights():
    phueExt.set_to_base_color(phueLights, 0)
    phueExt.on(phueLights)
    phueExt.temp_off(phueLights)
    tuyaExt.set_light_state(tuyaLights, on=False)


def readFile(path):
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


def executeCommand(cmd, args):
    argsCount = len(args)

    if argsCount <= 1:
        return

    match cmd:
        case "phue":
            lights = {}
            if args[0] == "*":
                lights = phueLights.copy()
            else:
                lights = ast.literal_eval(args[0])
            match args[1]:
                case "on":
                    transitiontime = 0
                    if argsCount > 2:
                        transitiontime = int(args[2])
                    phueExt.temp_on(lights, transitiontime)
                case "off":
                    transitiontime = 0
                    if argsCount > 2:
                        transitiontime = int(args[2])
                    phueExt.temp_off(lights, transitiontime)
                case "fon":
                    transitiontime = 0
                    if argsCount > 2:
                        transitiontime = int(args[2])
                    phueExt.on(lights, transitiontime)
                case "foff":
                    transitiontime = 0
                    if argsCount > 2:
                        transitiontime = int(args[2])
                    phueExt.off(lights, transitiontime)
                case "flicker":
                    duration = 3
                    if argsCount > 2:
                        duration = float(args[2])
                    frequency = 1
                    if argsCount > 3:
                        frequency = float(args[3])
                    phueExt.start_flicker(lights, duration, frequency)
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
                    phueExt.start_color_switch(
                        lights, duration, transitiontime, waitTime)
        case "tuya":
            lights = {}
            if args[0] == "*":
                lights = tuyaLights.copy()
            else:
                lights = ast.literal_eval(args[0])
            match args[1]:
                case "on":
                    tuyaExt.on(lights)
                case "off":
                    tuyaExt.off(lights)
                case "flicker":
                    duration = 3
                    if argsCount > 2:
                        duration = float(args[2])
                    frequency = 1
                    if argsCount > 3:
                        frequency = float(args[3])
                    tuyaExt.start_flicker(lights, duration, frequency)
        case "spotify":
            match args[0]:
                case "play":
                    if argsCount < 2:
                        return
                    uri = args[1]
                    spotifyExt.play(uri)
                case "pause":
                    spotifyExt.pause()
                case "volume":
                    if argsCount < 2:
                        return
                    volume = int(args[1])
                    spotifyExt.set_volume(volume)
            return


def playFile(path, wait=0.5):
    initLights()
    commands = readFile(path)
    sleep(wait)
    if "start" in commands:
        for command in commands["start"]:
            splits = command.split(" ")
            Thread(target=executeCommand, args=(splits[0], splits[1:])).start()
        commands.pop("start")
    startTime = time.time()
    timestamps = list(commands.keys())
    while len(timestamps) > 0:
        elapsedTime = time.time() - startTime
        key = timestamps[0]
        if elapsedTime >= float(key):
            for command in commands[key]:
                splits = command.split(" ")
                Thread(target=executeCommand, args=(
                    splits[0], splits[1:])).start()

            commands.pop(key)
            timestamps.pop(0)

        sleep(0.01)


playFile("./examples/test.show")
#print(spotifyExt.getCurrentPlaybackURI())
