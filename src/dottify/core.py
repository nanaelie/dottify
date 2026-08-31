from __future__ import annotations

from typing import Any, Iterator, Mapping, Optional, Union
from .exceptions import DottifyKNFError


class Dottify(dict):
    """
    Dictionary that supports both item and attribute access, recursive
    conversion of nested dicts, integer indexing by insertion order,
    merging with + / +=, and helpful KeyError-style suggestions.
    """

    def __init__(self, data: Optional[Mapping[str, Any]] = None, **kwargs: Any) -> None:
        super().__init__()
        if data is None:
            data = {}
        # Accept both a mapping and keyword arguments
        self.update(data)
        self.update(kwargs)

    # ------------------------------------------------------------------
    # Core conversion helpers
    # ------------------------------------------------------------------

    def _convert(self, value: Any) -> Any:
        """Recursively turn plain dicts into Dottify instances."""
        if isinstance(value, dict) and not isinstance(value, Dottify):
            return Dottify(value)
        return value

    def to_dict(self) -> dict:
        """Recursively convert back to a plain dict."""
        return {
            k: (v.to_dict() if isinstance(v, Dottify) else v)
            for k, v in self.items()
        }

    # ------------------------------------------------------------------
    # Item / attribute access
    # ------------------------------------------------------------------

    def __getitem__(self, key: Union[str, int]) -> Any:
        if isinstance(key, int):
            try:
                return list(self.values())[key]
            except IndexError:
                raise DottifyKNFError(f"Index {key} out of range (size {len(self)}).") from None

        try:
            return super().__getitem__(key)
        except KeyError:
            suggestions = self._suggest_keys(key)
            msg = f"Key '{key}' not found."
            if suggestions:
                msg += f" Did you mean: {', '.join(suggestions)}?"
            raise DottifyKNFError(msg) from None

    def __setitem__(self, key: str, value: Any) -> None:
        super().__setitem__(key, self._convert(value))

    def __delitem__(self, key: str) -> None:
        try:
            super().__delitem__(key)
        except KeyError:
            suggestions = self._suggest_keys(key)
            msg = f"Key '{key}' not found."
            if suggestions:
                msg += f" Did you mean: {', '.join(suggestions)}?"
            raise DottifyKNFError(msg) from None

    def __getattr__(self, name: str) -> Any:
        # Called only when normal attribute lookup fails
        try:
            return self[name]
        except DottifyKNFError as e:
            raise AttributeError(str(e)) from None

    def __setattr__(self, name: str, value: Any) -> None:
        # Keep real instance attributes (and methods) out of the dict
        if name.startswith("_") or name in type(self).__dict__:
            super().__setattr__(name, value)
        else:
            self[name] = value

    def __delattr__(self, name: str) -> None:
        try:
            del self[name]
        except DottifyKNFError as e:
            raise AttributeError(str(e)) from None

    # ------------------------------------------------------------------
    # dict-like interface (with suggestions)
    # ------------------------------------------------------------------

    # def get(self, key: str, default: Any = None, *, raise_missing: bool = False) -> Any:
    #     """
    #     Case-sensitive get.
    #     If raise_missing=True and the key is absent, raise DottifyKNFError
    #     (with suggestions) instead of returning default.
    #     """
    #     try:
    #         return self[key]
    #     except DottifyKNFError:
    #         if raise_missing:
    #             raise
    #         return default
    
    def get(self, key: str, default: Any = None, *, raise_missing: bool = False) -> Any:
        """
        Get a value by key case-insensitively, optionally returning a default value.

        :param key: The key to retrieve.
        :type key: str
        :param default: The value to return if key not found. Defaults to None.
        :type default: Any, optional
        :return: The found value or default.
        :rtype: Any
        :raises DottifyKNFError: If key not found and no default provided, with suggestions.
        """

        try:
            return self[key]
        except DottifyKNFError:
            if raise_missing:
                raise
            return default
        
    def get_ci(self, key: str, default: Any = None) -> Any:
        """Case-insensitive get (returns first match)."""
        key_lower = key.lower()
        for k, v in self.items():
            if k.lower() == key_lower:
                return v
        return default

    def pop(self, key: str, *args) -> Any:
        try:
            return super().pop(key, *args)
        except KeyError:
            if args:
                return args[0]
            suggestions = self._suggest_keys(key)
            msg = f"Key '{key}' not found."
            if suggestions:
                msg += f" Did you mean: {', '.join(suggestions)}?"
            raise DottifyKNFError(msg) from None

    def setdefault(self, key: str, default: Any = None) -> Any:
        if key not in self:
            self[key] = default
        return self[key]

    def update(self, other: Optional[Mapping] = None, **kwargs) -> None:
        if other is not None:
            for k, v in other.items():
                self[k] = v
        for k, v in kwargs.items():
            self[k] = v

    def remove(self, key: str) -> Any:
        """Alias for pop that always raises on missing key."""
        return self.pop(key)

    # ------------------------------------------------------------------
    # Operators
    # ------------------------------------------------------------------

    def __add__(self, other: Mapping) -> Dottify:
        if not isinstance(other, Mapping):
            return NotImplemented
        result = Dottify(self)
        result.update(other)
        return result

    def __iadd__(self, other: Mapping) -> Dottify:
        if not isinstance(other, Mapping):
            raise TypeError(
                f"unsupported operand type(s) for +=: 'Dottify' and '{type(other).__name__}'"
            )
        self.update(other)
        return self

    def __or__(self, other: Mapping) -> Dottify:          # Python 3.9+ style
        return self + other

    def __ior__(self, other: Mapping) -> Dottify:
        self += other
        return self

    # ------------------------------------------------------------------
    # Representation & iteration
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return f"Dottify({super().__repr__()})"

    def __str__(self) -> str:
        return self.__repr__()

    def __iter__(self) -> Iterator[str]:
        return super().__iter__()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _suggest_keys(self, key: str, limit: int = 5) -> list[str]:
        """Simple substring suggestions (case-insensitive)."""
        key_lower = key.lower()
        matches = [k for k in self if key_lower in k.lower()]
        # Prefer closer matches first (shortest extra characters)
        matches.sort(key=lambda k: abs(len(k) - len(key)))
        return matches[:limit]

    def has_key(self, key: str) -> bool:
        """Deprecated-style helper kept for compatibility."""
        return key in self


# ------------------------------------------------------------------
# Quick self-test (optional)
# ------------------------------------------------------------------
if __name__ == "__main__":
    d = Dottify({"Name": "Alice", "age": 30, "address": {"city": "NYC", "zip": 10001}})
    print(d.Name)                 # Alice
    print(d["age"])               # 30
    print(d[0])                   # Alice (first value)
    print(d.address.city)         # NYC
    print(d + {"country": "USA"}) # merged
    d += {"phone": "123"}
    print(d.to_dict())
    try:
        print(d.missing)
    except AttributeError as e:
        print(e)
