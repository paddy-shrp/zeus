import os
from os.path import exists, abspath, dirname
import json
import utils.getters as getters

DIR_PATH = getters.get_credentials_path()

def init_credentials():
    if not exists(DIR_PATH):
        os.mkdir(DIR_PATH)

def get_credentials_json(file_name):  
    path = get_path(file_name)
    if not exists(path): init_credentials()
    if exists(path):
        return json.load(open(path))

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