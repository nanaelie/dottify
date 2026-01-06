from dottify.exceptions import *
from typing import Any

class Dottify(dict):
    """
    A dictionary subclass that allows attribute-style access to keys,
    recursive conversion of nested dictionaries to Dottify instances,
    and enhanced key handling with suggestions on missing keys.

    Features:
    - Access keys as attributes or with item access (obj.key or obj['key']).
    - Supports accessing keys by integer index (order of insertion).
    - Supports merging with other dict-like objects using + and += operators.
    - Case-insensitive get method with optional default and suggestions.
    - Raises DottifyKNFError with suggestions if a key is not found.
    """

    def __init__(self, dic: dict):
        """
        Initialize the Dottify instance, recursively converting nested dictionaries.

        :param dic: The dictionary to convert into a Dottify object.
        :type dic: dict
        """
        super().__init__()
        
        for key, value in dic.items():
            if isinstance(value, dict):
                setattr(self, key, Dottify(value))
            else:
                setattr(self, key, value)
                
    def __str__(self):
        return f"Dottify({self.__repr__()})"
                
    def __repr__(self):
        """
        Return the string representation of the Dottify object as a dict.

        :return: String representation of the dictionary form.
        :rtype: str
        """
        return self.to_dict().__repr__()
        
    def __getitem__(self, key):
        """
        Retrieve an item by key or integer index.

        :param key: The key (str) or index (int) to access.
        :type key: str or int
        :return: The value corresponding to the key or index.
        :rtype: Any
        :raises DottifyKNFError: If the key or index is not found, with suggestions.
        """
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
        """
        Set an item by key.

        :param key: The key to set.
        :type key: str
        :param value: The value to assign.
        :type value: Any
        :return: Self, to allow chaining.
        :rtype: Dottify
        """
        self.__dict__[key] = value
        return self
        
    def __add__(self, other):
        """
        Return a new Dottify instance merging self with another dict-like object.

        :param other: The dictionary to merge.
        :type other: dict or Dottify
        :return: A new Dottify instance with merged keys.
        :rtype: Dottify
        :return: NotImplemented if 'other' is not dict-like.
        """
        if not isinstance(other, (dict, Dottify)):
            return NotImplemented

        new_data = self.to_dict()
        other_data = other.to_dict() if isinstance(other, Dottify) else other
        new_data.update(other_data)
        return Dottify(new_data)
        
    def __iadd__(self, other):
        """
        Update self in-place by merging keys from another dict-like object.

        :param other: The dictionary to merge.
        :type other: dict or Dottify
        :return: Self updated.
        :rtype: Dottify
        :raises TypeError: If 'other' is not dict-like.
        """
        if not isinstance(other, (dict, Dottify)):
            raise TypeError(f"Unsupported operand type(s) for +=: 'Dottify' and '{type(other).__name__}'")
        
        for key, value in other.items():
            self.__dict__[key] = value
        
        return self
        
    def __getattr__(self, key):
        """
        Provide attribute-style access to keys.

        :param key: The attribute/key to access.
        :type key: str
        :return: The value for the key.
        :rtype: Any
        :raises DottifyKNFError: If the key is not found, with suggestions.
        """
        if not self.has_key(key):
            suggestions = self._suggest_keys(key)
            if suggestions:
                raise DottifyKNFError(f"Key '{key}' not found. Did you mean: {', '.join(suggestions)}?")
            raise DottifyKNFError(f"Key '{key}' not found.")
            
        return self.get(key)

    def __len__(self):
        """
        Return the number of keys.

        :return: Number of keys stored.
        :rtype: int
        """
        return len(self.__dict__)
        
    def __iter__(self):
        """
        Return an iterator over keys.

        :return: Iterator over the keys.
        :rtype: Iterator[str]
        """
        return iter(self.__dict__)
        
    def to_dict(self) -> dict:
        """
        Recursively convert Dottify back into a standard dictionary.

        :return: Standard dict representation of this object.
        :rtype: dict
        """
        res = {}
        for key, value in self.__dict__.items():
            if isinstance(value, Dottify):
                res[key] = value.to_dict()
            else:
                res[key] = value
                
        return res

    def remove(self, key: str) -> Any:
        """
        Remove a key from the Dottify object.

        :param key: The key to remove.
        :type key: str
        :raises DottifyKNFError: If the key is not found, with suggestions.
        """
        if not self.has_key(key):
            suggestions = self._suggest_keys(key)
            if suggestions:
                raise DottifyKNFError(f"Key '{key}' not found. Did you mean: {', '.join(suggestions)}?")
            raise DottifyKNFError(f"Key '{key}' not found.")
            
        del self.__dict__[key]
        
    def _suggest_keys(self, key):
        """
        Suggest similar keys based on a substring case-insensitive match.

        :param key: The key to match against.
        :type key: str
        :return: List of suggested keys.
        :rtype: list[str]
        """
        return [ky for ky in self.__dict__.keys() if key.lower() in ky.lower()]

    def get(self, key: str, default_value: Any = None) -> Any:
        """
        Get a value by key case-insensitively, optionally returning a default value.

        :param key: The key to retrieve.
        :type key: str
        :param default_value: The value to return if key not found. Defaults to None.
        :type default_value: Any, optional
        :return: The found value or default_value.
        :rtype: Any
        :raises DottifyKNFError: If key not found and no default_value provided, with suggestions.
        """
        key_found = False
        
        for ky, val in self.__dict__.items():
            if key.lower() == ky.lower():
                key_found = True
                return val
                
        if not key_found and default_value is None:
            suggestions = self._suggest_keys(key)
            if suggestions:
                raise DottifyKNFError(f"Key '{key}' not found. Did you mean: {', '.join(suggestions)}?")
            raise DottifyKNFError(f"Key '{key}' not found.")
            
        return default_value
        
    def keys(self):
        """
        Return keys view.

        :return: Keys view of the dictionary.
        :rtype: KeysView
        """
        return self.__dict__.keys()
    
    def values(self):
        """
        Return values view.

        :return: Values view of the dictionary.
        :rtype: ValuesView
        """
        return self.__dict__.values()

    def items(self):
        """
        Return items view.

        :return: Items view of the dictionary.
        :rtype: ItemsView
        """
        return self.__dict__.items()
    
    def has_key(self, key):
        """
        Check if a key exists exactly (case-sensitive).

        :param key: Key to check.
        :type key: str
        :return: True if key exists, False otherwise.
        :rtype: bool
        """
        for ky in self.__dict__.keys():
            if ky == key:
                return True
        return False

