import os
from os.path import exists
import json
import utils.paths as paths

DIR_PATH = paths.get_settings_path()

MAIN_SETTINGS_PATH = paths.get_settings_path("main.json")
MODULES_SETTINGS_PATH = paths.get_settings_path("modules.json")

def init_settings():
    if not exists(DIR_PATH):
        os.mkdir(DIR_PATH)
    if not exists(MAIN_SETTINGS_PATH):
        settings = { 
            "timezone": "Europe/Berlin",
            "data_logger": {
                "uri": "",
            },
            "allowed_origins": [
                "http://localhost",
                "http://127.0.0.1",
                "http://192.168.178.1"
            ],
            "include_extensions": [
                "spotify",
                "weather"
            ],
            "include_managers": []
        }
        
        with open(MAIN_SETTINGS_PATH, "w") as file:
            json.dump(settings, file, indent=4)
    if not exists(MODULES_SETTINGS_PATH):
        with open(MODULES_SETTINGS_PATH, "w") as file: 
            json.dump({}, file)

def get_main_settings():
    if not exists(MAIN_SETTINGS_PATH):
        init_settings()
    return json.load(open(MAIN_SETTINGS_PATH))

def get_module_settings(module_name, default_settings={}):
    if not exists(MODULES_SETTINGS_PATH):
        init_settings()
    
    modules_settings = json.load(open(MODULES_SETTINGS_PATH))

    if module_name in modules_settings:
        return modules_settings[module_name]
    else:
        modules_settings[module_name] = default_settings
        with open(MODULES_SETTINGS_PATH, "w") as file:
            json.dump(modules_settings, file, indent=4)
        return modules_settings[module_name]
