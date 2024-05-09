import inspect
import zeus_core.modules as modules

def generate_module_routes(app, prefix, ext_name, module):
    for name, method in inspect.getmembers(module, inspect.ismethod):
        if name == "__init__": continue
        if name == "include": continue
        if not hasattr(method, 'included'): continue
        path = f"/{prefix}/{ext_name}/{name}/"

        tag = f"{prefix} - {ext_name}"
        if name == "get_data":

            path = f"/data/{prefix}/{ext_name}" 
            tag = "data"
        app.add_api_route(path, method, tags=[tag], methods=[method.request_type])

def generate_modules_routes(app):
    for module_name, module in modules.get_modules().items():
        generate_module_routes(app, module[1], module_name, module[0])