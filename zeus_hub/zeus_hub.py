import subprocess
import os
import signal
import sys

from zeus_core.utils import paths
from zeus_core.utils import credentials

PID_FILE = "hub_pids.json"

APPS_DICT = {
    "api": "api/api_app.py",
    "data": "data/data_app.py"
}

DEFAULT_CREDENTIALS = {
    "pids": {}
}

def get_pids():
    return credentials.get_credentials_json(PID_FILE, DEFAULT_CREDENTIALS)["pids"]

def is_process_running(key):
    return key in get_pids()

def set_process_credentials(key, pid):
    data = credentials.get_credentials_json(PID_FILE, DEFAULT_CREDENTIALS)
    data["pids"][key] = pid
    credentials.write_credentials_json(PID_FILE, data)

def del_process_credentials(key):
    data = credentials.get_credentials_json(PID_FILE, DEFAULT_CREDENTIALS)
    pids = data["pids"]
    pids.pop(key)
    data["pids"] = pids
    credentials.write_credentials_json(PID_FILE, data)

def start_processes():
    for app_name, app_path in APPS_DICT.items():
        if not is_process_running(app_name):
            command = [sys.executable, paths.get_main_path(app_path)]

            process = subprocess.Popen(command)

            set_process_credentials(app_name, process.pid)
            print(f"Started {app_name} with PID: {process.pid}")
        else:
            print("Process already running")

def kill_processes():
    for key, pid in get_pids().items():
        try:
            os.kill(pid, signal.SIGTERM)
            print(f"Killed process with PID: {pid}")
        except Exception as e:
            print(e)
            pass
        del_process_credentials(key)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Use commands start|stop|check as args")
        sys.exit(1)
    
    if sys.argv[1] == "start":
        start_processes()
    elif sys.argv[1] == "stop":
        kill_processes()
    elif sys.argv[1] == "check":
        print("PIDS", get_pids())
    else:
        print("Use commands start|stop|check as args")
        sys.exit(1)