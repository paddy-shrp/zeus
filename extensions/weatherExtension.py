from os.path import exists
from .decorators import *
import json
import requests
import time

# This cannot be changed later on, else the data will be useless
EXTENSION_NAME = "weather"
CREDENTIALS_PATH = f"./credentials/{EXTENSION_NAME}-credentials.json"

ONECALL_URL = "https://api.openweathermap.org/data/3.0/onecall"
CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"

class WeatherExtension:

    def __init__(self, apiKey="", lat="", lon=""):
        if not exists(CREDENTIALS_PATH):
            credentials = {"apiKey": apiKey, "lat": lat, "lon": lon}
            with open(CREDENTIALS_PATH, "w") as file:
                json.dump(credentials, file, indent=4)
        credentials = json.load(open(CREDENTIALS_PATH))
        self.apiKey = credentials["apiKey"]
        self.lat = credentials["lat"]
        self.lon = credentials["lon"]
        self.units = credentials["units"]
        self.last_current = {}
        self.last_onecall = {}

    def get_base_params(self):
        params = {
            "lat": self.lat,
            "lon": self.lon,
            "appid": self.apiKey,
            "units": self.units
        }
        return params

    def one_call(self):
        response = requests.get(ONECALL_URL, params=self.get_base_params())
        if response.status_code == 200:
            self.last_onecall = response.json()
        else:
            print("Error with weather Extension querry: ", response.status_code)

    @include_put
    def current_call(self):
        response = requests.get(CURRENT_URL, params=self.get_base_params())
        if response.status_code == 200:
            self.last_current = response.json()
            return 200
        else:
            return response.status_code

    def get_current(self):
        if self.last_current == {}: 
            self.current_call()
            return self.last_current
        
        time_diff = int(time.time()) - self.last_current["dt"]
        if time_diff > 10: self.current_call()

        return self.last_current

    @include_get
    def get_data(self):
        return self.get_current()