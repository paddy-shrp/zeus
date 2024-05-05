import extensions
import time
import utils.settings as settings
from threading import Thread
from influxdb_client_3 import InfluxDBClient3, Point

exts = extensions.get_extensions()

class DataLogger():

    def __init__(self, token, host, org, bucket):
        self.client = InfluxDBClient3(host=host, token=token, org=org)
        self.bucket = bucket

    def log_extension(self, name, ext):
        self.add_point(name, ext.get_data())

    def log_data(self):
        threads = []
        for name, ext in exts.items():
            Thread(target=self.log_extension, args=(name, ext)).start()
    
        for thread in threads:
            thread.join()

    def add_point(self, id, value):
        point = (
            Point(id)
            .field("status", value)
        )
        self.client.write(database=self.bucket, record=point)

db_settings = settings.get_settings()["data"]
db = DataLogger(db_settings["key"], db_settings["host"], db_settings["org"], db_settings["bucket"])


while True:
    db.log_data()
    time.sleep(5)