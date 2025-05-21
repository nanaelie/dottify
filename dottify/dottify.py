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
        if type(key) == int:
            n = 0
            for ky, value in self.__dict__.items():
                if n == key:
                    return Dottify(value) if isinstance(value, dict) else value
                
                n += 1
            
            raise DottifyKNFError(f"Key '{key}' not found.")
            
        if not self.has_key(key):
            suggestions = self._suggest_keys(key)
            if suggestions:
                raise DottifyKNFError(f"Key '{key}' not found. Did you mean: {', '.join(suggestions)}?")
            raise DottifyKNFError(f"Key '{key}' not found.")
            
        return self.get(key)

    def __setitem__(self, key, value):
        self.__dict__[key] = value
        return self
        
    def __add__(self, other):
        if not isinstance(other, (dict, Dottify)):
            return NotImplemented

        new_data = self.to_dict()
        other_data = other.to_dict() if isinstance(other, Dottify) else other
        new_data.update(other_data)
        return Dottify(new_data)
        
    def __iadd__(self, other):
        if not isinstance(other, (dict, Dottify)):
            raise TypeError(f"Unsupported operand type(s) for +=: 'Dottify' and '{type(other).__name__}'")
        
        for key, value in other.items():
            self.__dict__[key] = value
        
        return self
        
    def __getattr__(self, key):
        if not self.has_key(key):
            suggestions = self._suggest_keys(key)
            if suggestions:
                raise DottifyKNFError(f"Key '{key}' not found. Did you mean: {', '.join(suggestions)}?")
            raise DottifyKNFError(f"Key '{key}' not found.")
            
        return self.get(key)

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
        if not self.has_key(key):
            suggestions = self._suggest_keys(key)
            if suggestions:
                raise DottifyKNFError(f"Key '{key}' not found. Did you mean: {', '.join(suggestions)}?")
            raise DottifyKNFError(f"Key '{key}' not found.")
            
        del self.__dict__[key]
        
    def _suggest_keys(self, key):
        return [ky for ky in self.__dict__.keys() if ky.lower().__contains__(key.lower())]

    def get(self, key: str, default_value: Any = None) -> Any:
        key_found = False
        
        for ky, val in self.__dict__.items():
            if key.lower() == ky.lower():
                key_found = True
                
                return val
                
        if key_found is False and default_value is None:
            suggestions = self._suggest_keys(key)
            if suggestions:
                raise DottifyKNFError(f"Key '{key}' not found. Did you mean: {', '.join(suggestions)}?")
            raise DottifyKNFError(f"Key '{key}' not found.")
            
        return default_value
        
    def keys(self):
        return self.__dict__.keys()
    
    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()
    
    def has_key(self, key):
        for ky in self.__dict__.keys():
            if ky == key:
                return True
                
        return False


