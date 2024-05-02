import os
from os.path import exists
import json

DIR_PATH = "./credentials/"

def init_credentials():
    if not exists(DIR_PATH):
        os.mkdir(DIR_PATH)

def get_credentials_json(path):  
    if not credentials_exist(): init_credentials()
    if credentials_exist(path):
        return json.load(open(DIR_PATH + path))

def write_credentials_json(path, credentials):
    with open(DIR_PATH + path, "w") as file:
         json.dump(credentials, file)

def write_credentials(path, credentials):
    with open(DIR_PATH + path, "w") as file:
            file.write(credentials)

def credentials_exist(path=""):
     return exists(DIR_PATH + path)

def get_path(path=""):
     return DIR_PATH + path