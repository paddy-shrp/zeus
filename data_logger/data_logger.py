import time
import utils.settings as settings
import utils.dt_formatter as df
from threading import Thread
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

import extensions
import managers

exts = extensions.get_extensions()
mgs = managers.get_managers()

set = settings.get_settings()["data_logger"]
uri = set["uri"].replace("<password>", set["password"])
client = MongoClient(uri)
    
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

def log_extension(name, ext):
    add_point("extensions", name, ext.get_data())

def log_manager(name, mg):
    add_point("managers", name, mg.get_data())

def log_data():
    threads = []
    for name, ext in exts.items():
        Thread(target=log_extension, args=(name, ext)).start()
    
    for name, mg in mgs.items():
        Thread(target=log_manager, args=(name, mg)).start()

    for thread in threads:
        thread.join()

def get_extension_collection(ext_name):
    return client.get_database("extensions").get_collection(ext_name)

def get_manager_collection(mg_name):
    return client.get_database("managers").get_collection(mg_name)

def add_point(db_name, cl_name, value):
    if value == {}: return
    data = {}
    data["timestamp"] = int(time.time())
    data["value"] = value
    collection = client.get_database(db_name).get_collection(cl_name)
    try:
        collection.insert_one(data)
    except DuplicateKeyError:
        pass
