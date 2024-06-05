import os
from os.path import exists

from utils import settings, credentials, paths
import modules

# Resources
if not exists(paths.get_resources_path()):
        os.mkdir(paths.get_resources_path())

# Logging
if not exists(paths.get_logs_path()):
        os.mkdir(paths.get_logs_path())
        
# Credentials
credentials.init_credentials()
# Settings
settings.init_settings()

# Modules
modules.get_modules()