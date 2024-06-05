from utils.decorators import *

from threading import Thread
import time
import logging

from pymongo.mongo_client import MongoClient
from pymongo.collection import Collection
from pymongo.server_api import ServerApi
from pymongo.errors import DuplicateKeyError

from zeus_core import modules
from zeus_core.utils.objects.module import Module 

# Cache Collections

class MongoDB():

    def __init__(self, uri):
        self.modules = modules.get_modules()        
        self.client = MongoClient(uri, server_api=ServerApi('1'))

        self.cached_collections = {}
        for module_name, module in self.modules.items():
            self.get_collection(module[1], module_name)

        try:
            self.client.admin.command('ping')
            logging.info("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            logging.exception(e)

    def get_collection(self, db_name, cl_name) -> Collection:
        key = db_name + "." + cl_name
        if key not in self.cached_collections:
            self.cached_collections[key] = self.client.get_database(db_name).get_collection(cl_name)
        return self.cached_collections[key]
    
    def get_collections(self):
        return self.cached_collections

    @include_post
    def log_module_request(self, md_name):
        for module_name, module in self.modules.items():
            if md_name == module_name:
                self.log_module(module_name, module[0], module[1])
                return

    def log_module(self, module_name, module:Module, type):
        try: 
            data = module.get_data()
            if data == {}: return

            if module.logging_frequency == 0:
                if self.data_has_changed(type, module_name, data):
                    self.add_point(type, module_name, data)
            elif module.logging_frequency > 0:
                frequency = max(1, module.logging_frequency)
                difference = time.time() - self.get_last_data_log_timestamp(type, module_name)
                if difference >= frequency:
                    self.add_point(type, module_name, data)
        except:
            pass

    @include_post
    def log_modules(self):
        threads = []
        for module_name, module in self.modules.items():
            Thread(target=self.log_module, args=(module_name, module[0], module[1])).start()

        for thread in threads:
            thread.join()

    def get_last_data_log(self, db_name, cl_name):
        data = self.get_collection(db_name, cl_name).find_one(sort=[("timestamp", -1)])
        if data == None:
            data = {
                "timestamp": 0,
                "value": {}
            }
        return data

    def get_last_data_log_timestamp(self, db_name, cl_name):
        return self.get_last_data_log(db_name, cl_name)["timestamp"]

    def get_last_data_log_value(self, db_name, cl_name):
        return self.get_last_data_log(db_name, cl_name)["value"]
    
    def data_has_changed(self, type, module_name, data):
        return not (self.get_last_data_log_value(type, module_name) == data)

    def add_point(self, db_name, cl_name, value):
        if value == {}: return
        data = {}
        data["timestamp"] = int(time.time())
        data["value"] = value
        try:
            self.get_collection(db_name, cl_name).insert_one(data)
        except DuplicateKeyError:
            pass

    def import_points(self, db_name, cl_name, points, timestamp_key="timestamp"):
        collection = self.get_collection(db_name, cl_name)
        for point in points:
            data = {}
            if timestamp_key in point:
                data["timestamp"] = point[timestamp_key]
                point.pop(timestamp_key)
            else:
                data["timestamp"] = int(time.time())

            data["value"] = point
            try:
                collection.insert_one(data)
            except DuplicateKeyError:
                pass

# set = settings.get_main_settings()["data_logger"]
# uri = set["uri"].replace("<password>", set["password"])
# mdb = MongoDB(uri)
# print(mdb.get_last_data_log_timestamp("extensions", "weather"))
