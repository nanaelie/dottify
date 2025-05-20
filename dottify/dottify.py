from dottify.exceptions import *
from typing import Any

class Dottify(dict):
    def __init__(self, dic: dict):
        super().__init__()
        
        for key, value in dic.items():
            if isinstance(value, dict):
                setattr(self, key, Dottify(value))
            else:
                setattr(self, key, value)
                
    def __repr__(self):
        return self.to_dict().__repr__()
        
    def __getitem__(self, key):
        match_ = self._find_key(key)
        if match_:
            return self.__dict__[match_]
            
        suggestions = self._suggest_keys(key)
        if suggestions:
            raise DottifyKNFError(f"Key '{key}' not found. Did you mean: {', '.join(suggestions)}?")
        raise DottifyKNFError(f"Key '{key}' not found.")

    def __setitem__(self, key, value):
        self.__dict__[key] = value
        return self
        
    def __getattr__(self, key):
        if not self.has_key(key):
            matches = []
            for ky, val in self.__dict__.items():
                if ky.lower().__contains__(key.lower()):
                    matches.append(ky)
            
            if matches:
                raise DottifyKNFError("Key '{}' not found. Do you mean '{}' ?".format(key, ', '.join(matches)))
            
            else:
                raise DottifyKNFError(f"Key '{key}' not found.")
                
        else:
            return self.__dict__[key]
                 
    def __len__(self):
        return len(self.__dict__)
        
    def __iter__(self):
        return iter(self.__dict__)
        
    def to_dict(self) -> dict:
        res = {}
        for key, value in self.__dict__.items():
            if isinstance(value, Dottify):
                res[key] = value.to_dict()
            else:
                res[key] = value
                
        return res

    def remove(self, key: str) -> Any:
        for ky in self.__dict__:
            if ky.lower() == key.lower():
                del self.__dict__[ky]
                return
                
        matches = [ky for ky in self.__dict__ if key.lower() in ky.lower()]
        if matches:
            raise DottifyKNFError(f"Key '{key}' not found. Did you mean: {', '.join(matches)}?")
        
        raise DottifyKNFError(f"Key '{key}' not found.")

    def _find_key(self, key):
        for ky in self.__dict__:
            if ky.lower() == key.lower():
                return ky
        return None

    def _suggest_keys(self, key):
        return [ky for ky in self.__dict__ if key.lower() in ky.lower()]

    def get(self, key: str, default_value: Any = None) -> Any:
        key_found = False
        
        for ky, val in self.__dict__.items():
            if key.lower() == ky.lower():
                key_found = True
                
                return val
                
        if key_found is False and default_value is None:
            matches = []
            for ky, val in self.__dict__.items():
                if ky.lower().__contains__(key.lower()):
                    matches.append(ky)
            
            if matches:
                raise DottifyKNFError("Key '{}' not found. Do you mean '{}' ?".format(key, ', '.join(matches)))
            
            else:
                raise DottifyKNFError(f"Key '{key}' not found.")
                
        return default_value
        
    def keys(self):
        return self.__dict__.keys()
    
    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()
    
    def has_key(self, key):
        return self._find_key(key) is not None


