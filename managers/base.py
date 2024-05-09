from utils.decorators import *
from utils.objects.manager import Manager

class Base(Manager):

    def __init__(self):
        default_settings = {}
        settings = self.get_manager_settings(default_settings)
        
    @include_get
    def get_data(self):
        data = {}
        return data