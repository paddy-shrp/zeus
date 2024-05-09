from utils.decorators import *
from utils.objects.module import Module

class Base(Module):

    def __init__(self):
        default_settings = {}
        settings = self.get_module_settings(default_settings)
        
    @include_get
    def get_data(self):
        data = {}
        return data