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
            if len(self.getActiveDevices()) < 1:
                return False
        else:
            if not self.isDeviceActive(device_id):
                return False

        try:
            if addtoqueue:
                self.client.add_to_queue(songuri, device_id)
            else:
                if (self.isPlaying()):
                    self.client.pause_playback()
                self.client.start_playback(device_id, uris=[songuri])
            return True
        except:
            return False

    def pause(self):
        try:
            if self.isPlaying():
                self.client.pause_playback()
        except:
            pass

    def unpause(self):
        try:
            if not self.isPlaying():
                self.client.start_playback()
        except:
            pass

    def setVolume(self, volumePercent, device_id=None):
        if device_id == None:
            if len(self.getActiveDevices()) < 1:
                return False
        else:
            if not self.isDeviceActive(device_id):
                return False

        try:
            self.client.volume(volumePercent, device_id)
            return True
        except:
            return False

    def getActiveDevices(self):
        return self.client.devices()["devices"]

    def isDeviceActive(self, device_id):
        try:
            active_devices = self.getActiveDevices()
            if not active_devices == None:
                return
            for activeDevice in active_devices:
                if activeDevice["name"] == device_id:
                    return True
        except:
            return False

    def getAudioAnalysis(self, trackID):
        try:
            return self.client.audio_analysis(trackID)
        except:
            pass

    def getCurrentPlayback(self):
        try:
            return self.client.current_playback()
        except:
            pass

    def isPlaying(self):
        try:
            return self.getCurrentPlayback()["is_playing"]
        except:
            pass

    def getCurrentDeviceID(self):
        try:
            return self.getCurrentPlayback()["device"]["id"]
        except:
            pass

    def getProgressInSeconds(self):
        try:
            return self.getCurrentPlayback()["progress_ms"] / 1000
        except:
            pass

    def getCurrentPlaybackItem(self):
        try:
            return self.getCurrentPlayback()["item"]
        except:
            pass

    def getCurrentPlaybackName(self):
        try:
            return self.getCurrentPlayback()["item"]["name"]
        except:
            pass

    def getCurrentPlaybackLink(self):
        try:
            return self.getCurrentPlayback()["item"]["href"]
        except:
            pass

    def getCurrentPlaybackURI(self):
        try:
            return self.getCurrentPlayback()["item"]["uri"]
        except:
            pass

    def getCurrentPlaybackAudioAnalysis(self):
        try:
            return self.getAudioAnalysis(self.getCurrentPlaybackURI())
        except:
            pass

    def getData(self):
        data = {}
        songIdName = EXTENSION_NAME + "_" + "songname"
        data[songIdName] = self.getCurrentPlaybackName()
        return data

#uri = "spotify:track:6AjlKVY7CbQi64zPbMEPZA"
