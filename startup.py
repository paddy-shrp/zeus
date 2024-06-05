import os
from os.path import exists

from zeus_core.utils import settings, credentials, paths
import zeus_core.modules as modules

# Resources
if not exists(paths.get_resources_path()):
        os.mkdir(paths.get_resources_path())

# Logging
if not exists(paths.get_logs_path()):
        os.mkdir(paths.get_logs_path())
# Credentials
credentials.init_credentials()
# Settings
settings.init_settings()

# Modules
modules.get_modules()

# Export the ZEUS_REPO_DIR Variable
export_command = "export ZEUS_REPO_DIR=" + paths.get_main_path()
shell_config_path = os.path.expanduser("~/.bashrc")

if not exists("~/.bashrc"):
    with open(shell_config_path, "w") as file:
        file.write("")

with open(shell_config_path, "r") as file:
    lines = file.readlines()

if export_command not in lines:
    with open(shell_config_path, "a") as file:
        file.write(f'\n{export_command}\n')

    print(f"Added {export_command} to {shell_config_path}")
else:
    print(f"{export_command} is already in {shell_config_path}")

# "shellscript": "bash --login -c"