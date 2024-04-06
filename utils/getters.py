def get_objects_filtered(objects, filter=[]):
    if len(filter) > 0:
        filtered_objects = {key: objects[key] for key in filter if key in objects}
        return filtered_objects
    else:
        return objects


def get_objects_initalized(objects):
    for name in objects.keys():
        objects[name] = objects[name]()

    return objects

