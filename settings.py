import json
from os.path import exists

SETTINGS_PATH = f"./credentials/settings.json"

def get_settings():
    if not exists(SETTINGS_PATH):
        settings = { 
            "allowed_origins": [
                "http://localhost",
                "http://127.0.0.1",
                "http://192.168.178.1"
            ]
        }
        
        with open(SETTINGS_PATH, "w") as file:
            json.dump(settings, file, indent=4)
    return json.load(open(SETTINGS_PATH))