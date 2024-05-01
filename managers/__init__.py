import utils.getters as ugetters
import utils.settings as settings
from importlib import import_module

cached_managers = {}

def init_managers():
    global cached_managers

    base_path = "managers."
    include_managers = settings.get_settings()["include_managers"]

    cached_managers = {}
    for module_name, class_name in include_managers.items():
        module_path = base_path + module_name + "." + module_name
        try: 
            module = import_module(module_path)
            class_ = getattr(module, class_name)
            cached_managers[class_.get_manager_name()] = class_()
        except Exception as e:
            print(e)
            print("Manager " + module_name + " not found!")

def get_managers(filter=[]):
    if cached_managers == {}:
        init_managers()
    return ugetters.get_objects_filtered(cached_managers, filter)

def get_managers_names():
    if cached_managers == {}:
        init_managers()
    return list(cached_managers.keys())