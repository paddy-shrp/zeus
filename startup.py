import os
from os.path import exists, abspath, dirname

import utils.settings as settings
import utils.credentials as credentials
import utils.paths as paths

import modules

# Resources
if not exists(paths.get_resources_path()):
        os.mkdir(paths.get_resources_path())

# Logging
if not exists(paths.get_logs_path()):
        os.mkdir(paths.get_logs_path())

# Credentials
credentials.init_credentials()

# if not credentials.credentials_exist("api.key"):
#     os.system("openssl genrsa -out api.key 2048")
#     os.system("openssl req -x509 -new -nodes -key api.key -sha256 -days 365 -out api.crt")
#     shutil.move("./api.key", credentials.get_path("api.key"))
#     shutil.move("./api.crt", credentials.get_path("api.crt"))

# Settings
settings.init_settings()

# Modules
modules.get_modules()
