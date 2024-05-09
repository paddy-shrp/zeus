import requests

from utils.decorators import *
from utils.objects.module import Module

FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"

class Weather(Module):

    def __init__(self, apiKey="", lat="", lon="", units=""):
        default_settings = {"apiKey": apiKey, "lat": lat, "lon": lon, "units": units}
        credentials = self.get_module_settings(default_settings)
        self.apiKey = credentials["apiKey"]
        self.lat = credentials["lat"]
        self.lon = credentials["lon"]
        self.units = credentials["units"]
        self.last_current = {}
        self.last_forecast = {}

    def get_base_params(self, lat=None, lon=None):
        params = {
            "lat": self.lat,
            "lon": self.lon,
            "appid": self.apiKey,
            "units": self.units
        }
        if lat != None or lon != None: 
            params["lat"] = lat
            params["lon"] = lon
        return params
        
    @include_get
    def get_current(self, lat=None, lon=None):
        response = requests.get(CURRENT_URL, params=self.get_base_params(lat, lon))
        if response.status_code == 200:
            return response.json()
        else:
            return response.status_code
    
    @include_get
    def get_forecast(self, lat=None, lon=None):
        response = requests.get(FORECAST_URL, params=self.get_base_params(lat, lon))
        if response.status_code == 200:
            return response.json()
        else:
            return response.status_code

    @include_get
    def get_data(self):
        return self.get_current()