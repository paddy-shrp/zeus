import spotipy
from spotipy import SpotifyOAuth
from utils.decorators import *
from utils.objects.extension import Extension

class Spotify(Extension):

    def __init__(self, client_id="", client_secret=""):
        default_settings = {
                "clientID": client_id,
                "clientSecret": client_secret,
                "redirectUri": "http://localhost:8080/callback",
                "scopes": "streaming user-read-playback-state user-modify-playback-state user-read-currently-playing playlist-read-private"
                }
        settings = self.get_extension_settings(default_settings)
        self.client = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=settings["clientID"],
                                                                client_secret=settings["clientSecret"],
                                                                redirect_uri=settings["redirectUri"],
                                                                scope=settings["scopes"]))

    # Return Codes need to be adjusted

    @include_post
    async def play(self, song, device_id = None):

        if device_id != None:
            if not self.is_device_active(device_id):
                return 504

        if self.is_spotify_link(song):
            song = self.get_uri_from_link(song)

        try:
            if "album" in song or "playlist" in song:
                self.client.start_playback(device_id, context_uri=song)
            else:
                self.client.start_playback(device_id, uris=[song])
            return 200
        except: return 504

    @include_put
    async def pause(self):
        try:
            self.client.pause_playback()
            return 200
        except: return 504
        
    @include_put
    async def resume(self):
        try:
            self.client.start_playback()
            return 200
        except: return 504

    @include_put
    async def set_volume(self, volume_percent:int, device_id=None):

        if device_id != None:
            if not self.is_device_active(device_id):
                return False

        try:
            self.client.volume(volume_percent, device_id)
            return 200
        except:
            return 504
        
    @include_put
    async def previous(self):
        try:
            self.client.previous_track()
            return 200
        except: return 504
    
    @include_put
    async def skip(self):
        try:
            self.client.next_track()
            return 200
        except: return 504

    @include_get
    async def get_active_devices(self):
        try:
            return self.client.devices()["devices"]
        except: return 504

    @include_get
    async def get_current_device(self):
        try:
            return self.get_current_playback()["device"]
        except: return 504

    @include_put
    async def change_current_device(self, device_id):
        try:
            self.client.transfer_playback(device_id)
            return 200
        except:
            return 504

    def is_device_active(self, device_id):
        try:
            active_devices = self.get_active_devices()
            if active_devices == None: return False
            for activeDevice in active_devices:
                if activeDevice["id"] == device_id:
                    return True
        except:
            return False

    def get_audio_analysis(self, track):

        if self.is_spotify_link(track):
            track = self.get_uri_from_link(track)

        try:
            return self.client.audio_analysis(track)
        except: return 504

    @include_get
    async def get_current_playback(self):
        try:
            return self.client.current_playback()
        except: return 504

    @include_get
    async def is_playing(self):
        try:
            return self.get_current_playback()["is_playing"]
        except: return 500

    @include_get
    async def get_progress(self):
        try:
            return self.get_current_playback()["progress_ms"] / 1000
        except: return 500
        
    @include_get
    async def get_current_playback_item(self):
        try:
            return self.get_current_playback()["item"]
        except: return 500
        
    @include_get
    async def get_data(self):
        data = {}
        return data
    
    def is_spotify_link(self, value:str):
        return "https://open.spotify.com/" in value

    def get_uri_from_link(self, link:str):
        base = "spotify:"
        link = link.replace("https://open.spotify.com/", "")
        link = link[:link.find("?")]
        link = link.replace("/", ":")

        return base + link

# https://open.spotify.com/track/1qwZ8rW8EGBf6sLUANCFZs?si=1e0e51670cbe4116
# spotify:track:1qwZ8rW8EGBf6sLUANCFZs

#uri = "spotify:track:6AjlKVY7CbQi64zPbMEPZA"