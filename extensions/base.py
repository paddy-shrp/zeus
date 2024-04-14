from utils.decorators import *
from utils.objects.extension import Extension

class Base(Extension):

    def __init__(self):
        default_settings = {}
        settings = self.get_extension_settings(default_settings)
        
    @include_get
    async def get_data(self):
        data = {}
        return data