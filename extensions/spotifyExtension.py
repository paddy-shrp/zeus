import spotipy
from spotipy import SpotifyOAuth

# This cannot be changed later on, else the data will be useless
EXTENSION_NAME = "spotify"


class SpotifyExtension:

    def __init__(self, client_id, client_secret, redirect_uri, scope):
        self.client = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                                client_secret=client_secret,
                                                                redirect_uri=redirect_uri,
                                                                scope=scope))

    def play(self, songuri, device_id=None, addtoqueue=False):
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

    def pause(self):
        try:
            if self.is_playing():
                self.client.pause_playback()
        except:
            pass

    def unpause(self):
        try:
            if not self.is_playing():
                self.client.start_playback()
        except:
            pass

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

    def get_active_devices(self):
        return self.client.devices()["devices"]

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

    def get_audio_analysis(self, trackID):
        try:
            return self.client.audio_analysis(trackID)
        except:
            pass

    def get_current_playback(self):
        try:
            return self.client.current_playback()
        except:
            pass

    def is_playing(self):
        try:
            return self.get_current_playback()["is_playing"]
        except:
            pass

    def get_current_device_id(self):
        try:
            return self.get_current_playback()["device"]["id"]
        except:
            pass

    def get_progress(self):
        try:
            return self.get_current_playback()["progress_ms"] / 1000
        except:
            pass

    def get_current_playback_item(self):
        try:
            return self.get_current_playback()["item"]
        except:
            pass

    def get_current_playback_name(self):
        try:
            return self.get_current_playback()["item"]["name"]
        except:
            pass

    def get_current_playback_link(self):
        try:
            return self.get_current_playback()["item"]["href"]
        except:
            pass

    def get_current_playback_uri(self):
        try:
            return self.get_current_playback()["item"]["uri"]
        except:
            pass

    def getData(self):
        data = {}
        songIdName = EXTENSION_NAME + "_" + "songname"
        data[songIdName] = self.get_current_playback_name()
        return data

#uri = "spotify:track:6AjlKVY7CbQi64zPbMEPZA"
