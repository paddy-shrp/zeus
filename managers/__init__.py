from utils.getters import *
import settings
from importlib import import_module

def get_managers(filter=[]):
    
    base_path = "managers."
    include_managers = settings.get_settings()["include_managers"]

    managers = {}
    for module_name, class_name in include_managers.items():
        module_path = base_path + module_name + "." + module_name
        module = import_module(module_path)
        class_ = getattr(module, class_name)
        managers[class_.get_manager_name()] = class_

    return get_objects_filtered(managers, filter)

def get_managers_initalized(filter=[]):
    return get_objects_initalized(get_managers(filter))

def get_managers_names():
    return list(get_managers().keys())