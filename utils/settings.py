import os
from os.path import exists, abspath, dirname
import json

DIR_PATH = dirname(dirname(abspath(__file__))) + "/settings/"

MAIN_SETTINGS_PATH = f"{DIR_PATH}main.json"
EXTENSION_SETTINGS_PATH = f"{DIR_PATH}extensions.json"
MANAGER_SETTINGS_PATH = f"{DIR_PATH}managers.json"

def init_settings():
    if not exists(DIR_PATH):
        os.mkdir(DIR_PATH)
    if not exists(MAIN_SETTINGS_PATH):
        settings = { 
            "allowed_origins": [
                "http://localhost",
                "http://127.0.0.1",
                "http://192.168.178.1"
            ],
            "include_extensions": {
                "spotify": "Spotify",
                "weather": "Weather"
            },
            "include_managers": {}
        }
        
        with open(MAIN_SETTINGS_PATH, "w") as file:
            json.dump(settings, file, indent=4)
    if not exists(EXTENSION_SETTINGS_PATH):
        with open(EXTENSION_SETTINGS_PATH, "w") as file: 
            json.dump({}, file)
    if not exists(MANAGER_SETTINGS_PATH):
        with open(MANAGER_SETTINGS_PATH, "w") as file: 
            json.dump({}, file)

def get_settings():
    if not exists(MAIN_SETTINGS_PATH):
        init_settings()
    return json.load(open(MAIN_SETTINGS_PATH))

def get_extension_settings(ext_name, default_settings={}):
    if not exists(EXTENSION_SETTINGS_PATH):
        init_settings()
    
    extensions_settings = json.load(open(EXTENSION_SETTINGS_PATH))

    if ext_name in extensions_settings:
        return extensions_settings[ext_name]
    else:
        extensions_settings[ext_name] = default_settings
        with open(EXTENSION_SETTINGS_PATH, "w") as file:
            json.dump(extensions_settings, file, indent=4)
        return extensions_settings[ext_name]
    

def get_manager_settings(mg_name, default_settings={}):
    if not exists(MANAGER_SETTINGS_PATH):
        init_settings()
    
    manager_settings = json.load(open(MANAGER_SETTINGS_PATH))

    if mg_name in manager_settings:
        return manager_settings[mg_name]
    else:
        manager_settings[mg_name] = default_settings
        with open(MANAGER_SETTINGS_PATH, "w") as file:
            json.dump(manager_settings, file, indent=4)
        return manager_settings[mg_name]
    
