import utils.settings as st

class Extension:
    
    @classmethod
    def get_extension_settings(cls, default_settings):
        return st.get_extension_settings(cls.get_extension_name(), default_settings) 
    
    @classmethod
    def get_extension_name(cls):
        return cls.__name__.lower()
