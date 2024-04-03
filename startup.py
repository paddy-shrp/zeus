import os
from os.path import exists
import json

# Extension Imports
from extensions.pHueLightsExtension import PHueExtension
from extensions.spotifyExtension import SpotifyExtension
from extensions.tuyaExtension import TuyaExtension

# NEEDS TO BE CHANGED TO YOUR SPECIFICATIONS
PHUE_IP = "192.168.178.28"

if not exists("./credentials"):
    path = "./credentials"
    os.mkdir(path)

# Setup Phue Extension
phueExt = PHueExtension(PHUE_IP)

# Setup tuya Extension
tuyaExt = TuyaExtension()

# Setup spotify Extension:
#   Please refer to
#   https://github.com/spotipy-dev/spotipy/blob/master/TUTORIAL.md
#   Name your credentials file "spotify-credentials"
#   Move your credentials file to the credentials folder

spC = json.load(open("./credentials/spotify-credentials.json"))
spotifyExt = SpotifyExtension(
    spC["clientID"], spC["clientSecret"], spC["redirectUri"], spC["scopes"])



