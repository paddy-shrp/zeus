import urllib3
from urllib3.exceptions import InsecureRequestWarning
import requests as rq
from threading import Thread
import numpy as np

import utils.credentials as credentials

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

    def get_lights(self):
        path = self.general_path + "light"
        lights_raw = self.execute_request(path)["data"]
        lights = []
        for light_raw in lights_raw:
            lights.append(self.get_processed_light(light_raw))
        return lights

    def get_light(self, id):
        path = self.general_path + f"light/{id}"
        light_raw = self.execute_request(path)["data"][0]
        return self.get_processed_light(light_raw)

    def get_processed_light(self, light_raw):
        light = {}
        light["id"] = light_raw["id"]
        light["name"] = light_raw["metadata"]["name"]
        light["on"] = light_raw["on"]["on"]
        if "dimming" in light_raw:
            light["brightness"] = light_raw["dimming"]["brightness"]
        return light

    def set_light_state(self, ids, on = None, bri = None, color = None, transitiontime = None):
        if type(ids) == str: ids = [ids]

        cmds = {}
        if on is not None:
            cmds["on"] = {"on": on}
        if bri is not None:
            cmds["dimming"] = {"brightness": bri}
        if color is not None:
            color_xy = self.convert_rbg_to_xy(*color)
            cmds["color"] = {"xy": {"x": color_xy[0], "y": color_xy[1]}}

        for id in ids:
            path = self.general_path + f"light/{id}"
            try:
                Thread(target=self.execute_request, args=(path, cmds, "PUT")).start()  
            except:
                pass      

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
        input("Press any button after the link button has been pressed")
        response = rq.post(f"https://{self.host}/api", json={"devicetype": "phueBridge", "generateclientkey": True}, verify=False)
        try: 
            data = response.json()[0]["success"]
            credentials.write_credentials_json(CREDENTIALS_PATH, 
                                       {"username": data["username"],
                                        "clientkey": data["clientkey"]})
        except:
            print("Please press the link button!")
            self.generate_client_key()

    def convert_rbg_to_xy(self, r, g, b):
        rgb_vector = np.array([r, g, b]) / 255.0
        transformation_matrix = np.array([
            [0.4124564, 0.3575761, 0.1804375],
            [0.2126729, 0.7151522, 0.0721750],
            [0.0193339, 0.1191920, 0.9503041]
        ])
        color_vector = transformation_matrix @ rgb_vector
        color_sum = color_vector.sum()
        if color_sum == 0: return [0.35, 0.35] 
        color_xy = (color_vector / color_sum)[:2]
        return color_xy

# https://viereck.ch/hue-xy-rgb/