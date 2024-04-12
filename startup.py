import os
from os.path import exists

import utils.settings as settings

# Extension Imports
import extensions

credentials_path = "./credentials"
if not exists(credentials_path):
    os.mkdir(credentials_path)

# Settings
settings.init_settings()

# Extensions
extensions.get_extensions_initalized()

# Setup phue Extension
# Edit the IP adress in the phue-credentials file

# Setup spotify Extension:
#   Please refer to
#   https://github.com/spotipy-dev/spotipy/blob/master/TUTORIAL.md
#   Edit the clientID and clientSecret in the spotify credentials file
