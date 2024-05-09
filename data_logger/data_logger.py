import time

from threading import Thread
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import DuplicateKeyError
import logging

import zeus_core.utils.settings as settings
import zeus_core.modules as modules

modules = modules.get_modules()

set = settings.get_main_settings()["data_logger"]
uri = set["uri"].replace("<password>", set["password"])
client = MongoClient(uri, server_api=ServerApi('1'))
    
# Log last point addons or geht last point addons
# Check for extension data reference
# Either only on change or on a frequent basis => last_call_timer

try:
    client.admin.command('ping')
    logging.info("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    logging.exception(e)

def log_module(module_name, module, type):
    try: 
        add_point(type, module_name, module.get_data())
    except:
        pass

def log_data():
    threads = []
    for module_name, module in modules.items():
        Thread(target=log_module, args=(module_name, module[0], module[1])).start()

    for thread in threads:
        thread.join()
    
    logging.info("All data has been logged!")

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
