from os.path import exists
from utils.decorators import *
from utils.extension import Extension
import json
import requests
import time

FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"

class Weather(Extension):

    def __init__(self, apiKey="", lat="", lon=""):
        if not exists(self.get_credentials_path()):
            credentials = {"apiKey": apiKey, "lat": lat, "lon": lon}
            with open(self.get_credentials_path(), "w") as file:
                json.dump(credentials, file, indent=4)
        credentials = json.load(open(self.get_credentials_path()))
        self.apiKey = credentials["apiKey"]
        self.lat = credentials["lat"]
        self.lon = credentials["lon"]
        self.units = credentials["units"]
        self.last_current = {}
        self.last_forecast = {}

    def get_base_params(self):
        params = {
            "lat": self.lat,
            "lon": self.lon,
            "appid": self.apiKey,
            "units": self.units
        }
        return params

    def forecast_call(self):
        response = requests.get(FORECAST_URL, params=self.get_base_params())
        if response.status_code == 200:
            self.last_forecast = response.json()
            self.last_forecast_dt = int(time.time())
            return 200
        else:
            return response.status_code

    def current_call(self):
        response = requests.get(CURRENT_URL, params=self.get_base_params())
        if response.status_code == 200:
            self.last_current = response.json()
            self.last_current_dt = int(time.time())
            return 200
        else:
            return response.status_code

    @include_get
    def get_current(self):
        if self.last_current == {}: 
            self.current_call()
            return self.last_current
        
        time_diff = int(time.time()) - self.last_current_dt
        if time_diff > 10: self.current_call()

        # Modify for general usage

        return self.last_current
    
    @include_get
    def get_forecast(self):
        if self.last_forecast == {}:
            self.forecast_call()
            return self.last_forecast
    
        time_diff = int(time.time()) - self.last_forecast_dt
        if time_diff > 60: self.forecast_call()

        # Modify for general usage

        return self.last_forecast

    @include_get
    def get_data(self):
        return {}
