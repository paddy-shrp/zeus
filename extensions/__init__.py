import utils.getters as ugetters
import utils.settings as settings
from importlib import import_module

cached_extensions = {}

def init_extensions():
    global cached_extensions

    base_path = "extensions."
    include_extensions = settings.get_settings()["include_extensions"]

    cached_extensions = {}
    for module_name, class_name in include_extensions.items():
        module_path = base_path + module_name
        try: 
            module = import_module(module_path)
            class_ = getattr(module, class_name)
            cached_extensions[class_.get_extension_name()] = class_()
        except Exception as e:
            print(e)
            print("Extension " + module_name + " not found!")

def get_extensions(filter=[]):
    if cached_extensions == {}:
        init_extensions()
    return ugetters.get_objects_filtered(cached_extensions, filter)

def get_extension_names():
    if cached_extensions == {}:
        init_extensions()
    return list(cached_extensions.keys())