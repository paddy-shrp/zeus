from utils.getters import *
from .weather import Weather
from .spotify import Spotify
from .p_hue import PHue
from .tuya import Tuya

def get_extensions(filter=[]):
    extensions = {}

    extensions[Weather.get_extension_name()] = Weather
    extensions[Spotify.get_extension_name()] = Spotify
    extensions[PHue.get_extension_name()] = PHue
    extensions[Tuya.get_extension_name()] = Tuya
 
    return get_objects_filtered(extensions, filter)

def get_extensions_initalized(filter=[]):
    return get_objects_initalized(get_extensions(filter))

def get_extension_names():
    extensions = get_extensions()
    return list(extensions.keys())