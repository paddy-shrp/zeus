
class Extension:
    
    @classmethod
    def get_extension_name(cls):
        return cls.__name__.lower()
    
    @classmethod
    def get_credentials_path(cls):
        return f"./credentials/{cls.get_extension_name()}-credentials.json"
