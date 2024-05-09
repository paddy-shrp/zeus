import utils.settings as st

class Module:
    
    @classmethod
    def get_module_settings(cls, default_settings):
        return st.get_module_settings(cls.get_module_name(), default_settings) 

    @classmethod
    def get_module_name(cls):
        return cls.__name__.lower()