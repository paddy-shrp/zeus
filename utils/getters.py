from os.path import join, abspath, dirname

def get_objects_filtered(objects, filter=[]):
    if len(filter) > 0:
        filtered_objects = {key: objects[key] for key in filter if key in objects}
        return filtered_objects
    else:
        return objects
    
def get_path(file):
    return dirname(abspath(file)) + "/"

def get_main_path():
    return dirname(dirname(abspath(__file__)))

def get_resources_path():
    return join(get_main_path(), "resources")

def get_settings_path(file_path=""):
    return join(get_resources_path(), "settings", file_path)

def get_credentials_path(file_path=""):
    return join(get_resources_path(), "credentials", file_path)

def get_logs_path(file_path=""):
    return join(get_resources_path(), "logs", file_path)