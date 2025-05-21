## [v1.1.0]

### **1. Inheritance**

* **Before:** `Dottify` did not inherit from any class.
* **Now:** `Dottify` inherits from `dict`.

### **2. Dot and Bracket Notation Support**

* **Before:** Only dot-access (`data.key`) was supported.
* **Now:** Both dot-access (`data.key`) and bracket-access (`data['key']`) are supported.

### **3. Improved Error Handling**

* Introduced a custom exception: `DottifyKNFError`, raised when keys are not found.
* Suggests similar keys when an invalid key is accessed.

### **4. New Methods Added**

* `__getitem__`, `__setitem__`: Allow using `data['key'] = value` syntax.
* `__getattr__`: Enhanced dot-access with fuzzy key matching and suggestions.
* `__len__`, `__iter__`, `keys()`, `values()`, `items()`: Emulate standard `dict` behavior.
* `remove(key)`: Removes key case-insensitively.
* `has_key(key)`: Checks for key existence (case-insensitive).
* `_suggest_keys(key)`: Internal helpers for smart key resolution.
* `__add__` method to support merging two `Dottify` instances using the `+` operator.

### **5. Enhanced `get()` Method**

* **Before:** Simply returned the default value if the key was missing.
* **Now:** If no default is given, suggests similar keys when key is missing.

### **6. Improved Recursive Conversion**

* All nested dictionaries are recursively converted into `Dottify` instances.

### **7. Type Hinting**

* Added type annotations, including `from typing import Any` for better clarity and IDE support.

The new version is a powerful and flexible upgrade. It transforms `Dottify` into a clean, user-friendly structure ideal for dynamic JSON-like data handling with both attribute and key access.

