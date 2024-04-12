from utils.getters import *
import utils.settings as settings
from importlib import import_module

def get_extensions(filter=[]):
    
    base_path = "extensions."
    include_extensions = settings.get_settings()["include_extensions"]

    extensions = {}
    for module_name, class_name in include_extensions.items():
        module_path = base_path + module_name
        try: 
            module = import_module(module_path)
            class_ = getattr(module, class_name)
            extensions[class_.get_extension_name()] = class_
        except:
            print("Extension " + module_name + " not found!")
 
    return get_objects_filtered(extensions, filter)

def get_extensions_initalized(filter=[]):
    return get_objects_initalized(get_extensions(filter))

def get_extension_names():
    extensions = get_extensions()
    return list(extensions.keys())