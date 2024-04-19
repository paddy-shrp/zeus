import os
import shutil

import utils.settings as settings
import utils.credentials as credentials

import extensions

credentials.init_credentials()

# if not credentials.credentials_exist("api.key"):
#     os.system("openssl genrsa -out api.key 2048")
#     os.system("openssl req -x509 -new -nodes -key api.key -sha256 -days 365 -out api.crt")
#     shutil.move("./api.key", credentials.get_path("api.key"))
#     shutil.move("./api.crt", credentials.get_path("api.crt"))

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
