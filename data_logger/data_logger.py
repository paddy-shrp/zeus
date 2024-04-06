from time import sleep
import json
import signal

# Database Import
from influxdbData import InfluxDB

# Extension Imports
from extensions.pHueLightsExtension import PHueExtension
from extensions.spotifyExtension import SpotifyExtension
from extensions.tuyaExtension import TuyaExtension

# Init DB
influxC = json.load(open("./credentials/influxdb-credentials.json"))
token = influxC["token"]
org = influxC["organization"]
url = "http://192.168.178.132:8086"
db = InfluxDB(token, url, org)
mainBucket = "homeData"

# Init Extensions
phueC = json.load(open("./credentials/phue-credentials.json"))
phueExt = PHueExtension(phueC["IP"])
poolC = json.load(open("./credentials/pool-credentials.json"))
tuyaExt = TuyaExtension()
spC = json.load(open("./spotify-credentials.json"))
spotifyExt = SpotifyExtension(
    spC["clientID"], spC["clientSecret"], spC["redirectUri"], spC["scopes"])


class SignalHandler:
    shutdown_requested = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.request_shutdown)
        signal.signal(signal.SIGTERM, self.request_shutdown)

    def request_shutdown(self, *args):
        print('Request to shutdown received, stopping')
        self.shutdown_requested = True

    def can_run(self):
        return not self.shutdown_requested


def get_current_snapshot():
    currentDataSnapshot = {}

    # Phue
    try:
        currentDataSnapshot.update(phueExt.get_data())
    except:
        print("Error with Phue Extension")

    # Tuya
    try:
        currentDataSnapshot.update(tuyaExt.get_data())
    except:
        print("Error with Tuya Extension")
    return currentDataSnapshot


signalHandler = SignalHandler()

while signalHandler.can_run():
    currentDataSnapshot = get_current_snapshot()

    for key in currentDataSnapshot:
        currentValue = currentDataSnapshot[key]
        if not (currentValue == db.get_last_value(mainBucket, key)):
            db.add_point(mainBucket, key, currentValue)
    sleep(1)
