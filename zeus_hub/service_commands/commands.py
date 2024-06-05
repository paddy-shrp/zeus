import subprocess
import os
from zeus_core.utils import paths

ZEUS_REPO_DIR = paths.get_main_path()

os.chdir(ZEUS_REPO_DIR)

activate_venv_command = f"source {ZEUS_REPO_DIR}/.venv/bin/activate"
subprocess.run(activate_venv_command, shell=True, executable="/bin/bash")

gunicorn_command = "gunicorn api_app:app --bind 127.0.0.1:8000 --workers 4 --worker-class uvicorn.workers.UvicornWorker &"
subprocess.run(gunicorn_command, shell=True, cwd=f"{ZEUS_REPO_DIR}/api")

data_app_command = f"{ZEUS_REPO_DIR}/.venv/bin/python {ZEUS_REPO_DIR}/data/data_app.py &"
subprocess.run(data_app_command, shell=True)