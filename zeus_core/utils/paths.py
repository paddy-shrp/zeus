from os.path import join, abspath, dirname
    
def get_path(file):
    return dirname(abspath(file)) + "/"

def get_main_path():
    return dirname(dirname(dirname(abspath(__file__))))

def get_resources_path():
    return join(get_main_path(), "resources")

def get_settings_path(file_path=""):
    return join(get_resources_path(), "settings", file_path)

def get_credentials_path(file_path=""):
    return join(get_resources_path(), "credentials", file_path)

def get_logs_path(file_path=""):
    return join(get_resources_path(), "logs", file_path)