import os
from os.path import exists
import json
import utils.paths as paths

DIR_PATH = paths.get_credentials_path()

def init_credentials():
    if not exists(DIR_PATH):
        os.mkdir(DIR_PATH)

def get_credentials_json(file_name, default_credentials={}):  
    path = get_path(file_name)
    if exists(path):
        return json.load(open(path))
    else:
        write_credentials_json(file_name, default_credentials)
        return default_credentials

def write_credentials_json(file_name, credentials):
    with open(get_path(file_name), "w") as file:
         json.dump(credentials, file)

def write_credentials(file_name, credentials):
    with open(get_path(file_name), "w") as file:
            file.write(credentials)

def file_exists(file_name):
    return exists(DIR_PATH + file_name)

def get_path(file_name=""):
     return DIR_PATH + file_name