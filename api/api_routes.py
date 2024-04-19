import inspect
import extensions
import managers

exts = extensions.get_extensions_initalized()
mgs = managers.get_managers_initalized()

def generate_routes(app, prefix, ext_name, module):
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

def generate_ext_mg_routes(app):
    for name, ext in exts.items():
        generate_routes(app, "extensions", name, ext)

    for name, mg in mgs.items():
        generate_routes(app, "managers", name, mg)

