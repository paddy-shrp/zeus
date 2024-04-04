import spotipy
from spotipy import SpotifyOAuth
from os.path import exists
from .decorators import *
import json

# This cannot be changed later on, else the data will be useless
EXTENSION_NAME = "spotify"
CREDENTIALS_PATH = f"./credentials/{EXTENSION_NAME}-credentials.json"

class SpotifyExtension:

    def __init__(self, client_id="", client_secret=""):
        if not exists(CREDENTIALS_PATH):
            credentials = {
                "clientID": client_id,
                "clientSecret": client_secret,
                "redirectUri": "http://localhost:8080/callback",
                "scope": "streaming user-read-playback-state user-modify-playback-state user-read-currently-playing playlist-read-private"
                }
            with open(CREDENTIALS_PATH, "w") as file:
                json.dump(credentials, file, indent=4)
        credentials = json.load(open(CREDENTIALS_PATH))
        self.client = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=credentials["clientID"],
                                                                client_secret=credentials["clientSecret"],
                                                                redirect_uri=credentials["redirectUri"],
                                                                scope=credentials["scopes"]))

    @include_post
    def play(self, songuri, device_id = None, addtoqueue = False):
        if device_id == None:
            if len(self.get_active_devices()) < 1:
                return False
        else:
            if not self.is_device_active(device_id):
                return False

        try:
            if addtoqueue:
                self.client.add_to_queue(songuri, device_id)
            else:
                if (self.is_playing()):
                    self.client.pause_playback()
                self.client.start_playback(device_id, uris=[songuri])
            return True
        except:
            return False

    @include_put
    def pause(self):
        try:
            if self.is_playing():
                self.client.pause_playback()
        except:
            pass

    @include_put
    def unpause(self):
        try:
            if not self.is_playing():
                self.client.start_playback()
        except:
            pass

    @include_put
    def set_volume(self, volumePercent, device_id=None):
        if device_id == None:
            if len(self.get_active_devices()) < 1:
                return False
        else:
            if not self.is_device_active(device_id):
                return False

        try:
            self.client.volume(volumePercent, device_id)
            return True
        except:
            return False

    @include_get
    def get_active_devices(self):
        return self.client.devices()["devices"]

    @include_get
    def is_device_active(self, device_id):
        try:
            active_devices = self.get_active_devices()
            if not active_devices == None:
                return
            for activeDevice in active_devices:
                if activeDevice["name"] == device_id:
                    return True
        except:
            return False

    @include_get
    def get_audio_analysis(self, trackID):
        try:
            return self.client.audio_analysis(trackID)
        except:
            pass

    @include_get
    def get_current_playback(self):
        try:
            return self.client.current_playback()
        except:
            pass

    @include_get
    def is_playing(self):
        try:
            return self.get_current_playback()["is_playing"]
        except:
            pass

    @include_get
    def get_current_device_id(self):
        try:
            return self.get_current_playback()["device"]["id"]
        except:
            pass

    @include_get
    def get_progress(self):
        try:
            return self.get_current_playback()["progress_ms"] / 1000
        except:
            pass

    @include_get
    def get_current_playback_item(self):
        try:
            return self.get_current_playback()["item"]
        except:
            pass

    @include_get
    def get_current_playback_name(self):
        try:
            return self.get_current_playback()["item"]["name"]
        except:
            pass

    @include_get
    def get_current_playback_link(self):
        try:
            return self.get_current_playback()["item"]["href"]
        except:
            pass

    @include_get
    def get_current_playback_uri(self):
        try:
            return self.get_current_playback()["item"]["uri"]
        except:
            pass

    @include_get
    def get_data(self):
        data = {}
        songIdName = EXTENSION_NAME + "_" + "songname"
        data[songIdName] = self.get_current_playback_name()
        return data

#uri = "spotify:track:6AjlKVY7CbQi64zPbMEPZA"
