import utils.settings as st

class Manager:
    
    @classmethod
    def get_manager_settings(cls, default_settings):
        return st.get_manager_settings(cls.get_manager_name(), default_settings) 

    @classmethod
    def get_manager_name(cls):
        return cls.__name__.lower()