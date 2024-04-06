from utils.getters import *
from .show.show import Show


def get_managers(filter=[]):
    managers = {}

    managers[Show.get_manager_name()] = Show

    return get_objects_filtered(managers, filter)

def get_managers_initalized(filter=[]):
    return get_objects_initalized(get_managers(filter))

def get_managers_names():
    return list(get_managers().keys())