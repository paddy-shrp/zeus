import utils.settings as st

class Module:
    logging_frequency = 0
    
    @classmethod
    def get_module_settings(cls, default_settings):
        return st.get_module_settings(cls.get_module_name(), default_settings)
    
    def get_interal_settings(cls):
        data = {
            "logging_frequency": cls.logging_frequency
            }
        return data

    @classmethod
    def get_module_name(cls):
        return cls.__name__.lower()