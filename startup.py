import os
from os.path import exists

import settings as settings

# Extension Imports
import extensions

if not exists("./credentials"):
    path = "./credentials"
    os.mkdir(path)

# Settings
settings.get_settings()

# Extensions
extensions.get_extensions_initalized()

# Setup phue Extension
# Edit the IP adress in the phue-credentials file

# Setup spotify Extension:
#   Please refer to
#   https://github.com/spotipy-dev/spotipy/blob/master/TUTORIAL.md
#   Edit the clientID and clientSecret in the spotify credentials file
