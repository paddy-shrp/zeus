from time import sleep
import json
import signal

# Database Import
from influxdbData import InfluxDB

# Init DB
influxC = json.load(open("./credentials/influxdb-credentials.json"))
token = influxC["token"]
org = influxC["organization"]
url = "http://192.168.178.132:8086"
db = InfluxDB(token, url, org)
mainBucket = "homeData"


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
    return currentDataSnapshot

signalHandler = SignalHandler()

while signalHandler.can_run():
    currentDataSnapshot = get_current_snapshot()

    for key in currentDataSnapshot:
        currentValue = currentDataSnapshot[key]
        if not (currentValue == db.get_last_value(mainBucket, key)):
            db.add_point(mainBucket, key, currentValue)
    sleep(1)
