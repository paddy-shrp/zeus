from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


class InfluxDB:
    def __init__(self, token, url, org):
        self.client = InfluxDBClient(url=url, token=token, org=org)
        self.writeAPI = self.client.write_api(write_options=SYNCHRONOUS)
        self.queryAPI = self.client.query_api()
        pass

    def add_point(self, bucket, id, value):
        self.writeAPI.write(bucket, record=(
            Point(id)
            .field("status", value)
        ))

    def get_last_value(self, bucket, measurement):
        query = """from(bucket: "{b}")
        |> range(start: -1h)
        |> filter(fn: (r) => r._measurement == "{m}")"""
        query = query.format(b=bucket, m=measurement)

        tables = self.queryAPI.query(query)
        if len(tables) > 0:
            lastRecord = tables[0].records[-1]
            return lastRecord["_value"]
        else:
            return None
