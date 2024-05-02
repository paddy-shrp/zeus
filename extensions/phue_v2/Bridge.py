import urllib3
import requests as rq
from urllib3.exceptions import InsecureRequestWarning
import utils.credentials as credentials
import json

urllib3.disable_warnings(InsecureRequestWarning)
CREDENTIALS_PATH = "phue_bridge.json"

class Bridge:

    def __init__(self, host = ""):
        self.host = host
        self.general_path = f"https://{host}/clip/v2/resource/"
        cred = credentials.get_credentials_json(CREDENTIALS_PATH)
        if cred == None:
            self.generate_client_key()
            cred = credentials.get_credentials_json(CREDENTIALS_PATH)
        self.username = cred["username"]
        self.clientkey = cred["clientkey"]
        self.get_lights()
        # self.set_light_state(9, cmds={"on": {"on": True}})

    def get_lights(self):
        path = self.general_path + "light"
        data = self.execute_request(path)["data"]
        with open("./extensions/tests/lights.json", "w") as file:
            json.dump(data, file)
        
        lights = []
        for light_raw in data:
            light = {}
            light["id"] = light_raw["id"]
            light["name"] = light_raw["metadata"]["name"]
            lights.append(light)
        print(lights)
        

    def set_light_state(self, ids, cmds, transitiontime = None):
        if type(ids) == int: ids = [ids]

        for id in ids:
            path = self.general_path + f"light/{id}"
            print(self.execute_request(path, cmds, "PUT"))        

    def execute_request(self, url, payload={}, method="GET"):
        response = None
        header = {"hue-application-key": self.username}
        if method == "GET":
            response = rq.get(url, headers=header, verify=False)
        elif method == "PUT":
            response = rq.put(url, headers=header, json=payload, verify=False)
        elif method == "POST":
            response = rq.post(url, headers=header, verify=False)
        return response.json()

    def generate_client_key(self):
        response = rq.post(f"https://{self.host}/api", json={"devicetype": "phueBridge", "generateclientkey": True}, verify=False)
        input("Press any button after the link button has been pressed")
        response = rq.post(f"https://{self.host}/api", json={"devicetype": "phueBridge", "generateclientkey": True}, verify=False)
        try: 
            data = response.json()[0]["success"]
            credentials.write_credentials_json(CREDENTIALS_PATH, 
                                       {"username": data["username"],
                                        "clientkey": data["clientkey"]})
        except:
            print("Please press the link button!")


b = Bridge("192.168.178.28")