import logging
from importlib import import_module
import inspect

import utils.settings as settings

cached_modules = {}

def init_modules():
    import_modules("extensions", settings.get_main_settings().get("include_extensions", []))
    import_modules("managers", settings.get_main_settings().get("include_managers", []))

def import_modules(import_path, module_names):
    global cached_modules

    for module_name in module_names:
        module_path = "modules." + import_path + "." + module_name
        try: 
            module = import_module(module_path)
            class_name = ""
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if module_path == obj.__module__: 
                    class_name = name
                    break
            class_ = getattr(module, class_name)
            try:
                if class_.get_module_name() in cached_modules:
                    logging.warning("A module with the name " + class_.get_module_name() + " already exists")
                else: 
                    cached_modules[class_.get_module_name()] = [class_(), import_path]
            except Exception as e:
                logging.exception(e)
                logging.exception("Error initalizing Module " + module_name)
        
        except Exception as e:
            logging.exception(e)
            logging.warning("Module import " + module_name + " not found")

def get_module(module_name):
    if cached_modules == {}: init_modules()
    if module_name in cached_modules:
        return cached_modules[module_name][0]
    else:
        logging.warning("Module " + module_name + " could not be found")
        return None

def get_modules(filter=[]):
    if cached_modules == {}: init_modules()

    if len(filter) > 0:
        return {key: cached_modules[key] for key in filter if key in cached_modules}
    else:
        return cached_modules

def get_module_names():
    if cached_modules == {}:
        init_modules()
    return list(cached_modules.keys())