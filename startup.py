import os
from os.path import exists

import settings

# Extension Imports
from extensions.pHueLightsExtension import PHueExtension
from extensions.spotifyExtension import SpotifyExtension
from extensions.tuyaExtension import TuyaExtension
from extensions.weatherExtension import WeatherExtension

if not exists("./credentials"):
    path = "./credentials"
    os.mkdir(path)

# Settings
settings.get_settings()


# Setup weather Extension
WeatherExtension()

# Setup phue Extension
# Edit the IP adress in the phue-credentials file
PHueExtension()

# Setup tuya Extension
TuyaExtension()

# Setup spotify Extension:
#   Please refer to
#   https://github.com/spotipy-dev/spotipy/blob/master/TUTORIAL.md
#   Edit the clientID and clientSecret in the spotify credentials file
SpotifyExtension()