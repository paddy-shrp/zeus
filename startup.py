import os
from os.path import exists, abspath, dirname

import utils.settings as settings
import utils.credentials as credentials

import extensions
import managers

# Logging
LOG_PATH = dirname(abspath(__file__)) + "/logs"
if not exists(LOG_PATH):
        os.mkdir(LOG_PATH)

# Credentials
credentials.init_credentials()

# if not credentials.credentials_exist("api.key"):
#     os.system("openssl genrsa -out api.key 2048")
#     os.system("openssl req -x509 -new -nodes -key api.key -sha256 -days 365 -out api.crt")
#     shutil.move("./api.key", credentials.get_path("api.key"))
#     shutil.move("./api.crt", credentials.get_path("api.crt"))

# Settings
settings.init_settings()

# Extensions
extensions.get_extensions()

# Managers
managers.get_managers()
