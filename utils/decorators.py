def include(func, request_type):
    func.included = True
    func.request_type = request_type
    return func

def include_get(func):
    return include(func, "GET")

def include_put(func):
    return include(func, "PUT")

def include_post(func):
    return include(func, "POST")

def include_delete(func):
    return include(func, "DELETE")

def include_patch(func):
    return include(func, "PATCH")