<p align="center">
  <a href="https://pepy.tech/projects/dottify">
    <img src="https://static.pepy.tech/badge/dottify" alt="PyPI Downloads" />
  </a>
  <img src="https://img.shields.io/pypi/v/dottify?style=flat-square" alt="PyPI" />
  <img src="https://img.shields.io/github/last-commit/nanaelie/dottify?style=flat-square" alt="GitHub last commit" />
  <img src="https://img.shields.io/github/license/nanaelie/dottify?style=flat-square" alt="License" />
  <img src="https://img.shields.io/badge/python-3.x-blue?style=flat-square" alt="Python" />
  <img src="https://img.shields.io/badge/tests-pytest-green?style=flat-square" alt="Tests" />
</p>

# Dottify

Dottify is a lightweight Python library that wraps dictionaries in objects with attribute-style access.

Instead of writing:

```python
data["user"]["name"]
```

you can write:

```python
data.user.name
```

Dottify supports nested dictionaries, dictionary-style access, attribute assignment, merging, conversion back to standard dictionaries, and common dictionary operations while providing helpful errors and key suggestions.

## Installation

Install Dottify from PyPI:

```sh
pip install dottify
```

## Quick Start

```python
from dottify import Dottify

data = Dottify({
    "name": "Alice",
    "age": 30,
    "address": {
        "city": "Paris",
        "country": "France"
    }
})

print(data.name)              # Alice
print(data.age)               # 30
print(data.address.city)      # Paris
print(data["address"].city)   # Paris
```

Nested dictionaries are automatically converted to `Dottify` instances.

## Features

### Attribute-style access

Access dictionary keys directly as attributes:

```python
data = Dottify({
    "name": "Alice",
    "age": 30
})

print(data.name)
print(data.age)
```

Dictionary-style access remains available:

```python
print(data["name"])
print(data["age"])
```

### Nested dictionaries

Nested dictionaries are recursively converted:

```python
data = Dottify({
    "user": {
        "name": "Alice",
        "address": {
            "city": "Paris"
        }
    }
})

print(data.user.name)
print(data.user.address.city)
```

### Case-sensitive access

Attribute and direct key access are case-sensitive:

```python
data = Dottify({
    "Name": "Alice"
})

print(data.Name)       # Alice
print(data["Name"])    # Alice
```

Using the wrong case raises a `DottifyKNFError`:

```python
data.name
```

The exception includes a helpful suggestion when an appropriate key exists.

### Key suggestions

When a key is missing, Dottify provides suggestions:

```python
data = Dottify({
    "username": "alice"
})

data.usernme
```

Dottify reports the missing key and suggests the closest matching key.

A default value can also be supplied:

```python
print(data.get("unknown", "Not Found"))
```

### Attribute assignment

Values can be modified using attribute syntax:

```python
data = Dottify({
    "name": "Alice"
})

data.name = "Bob"

print(data.name)  # Bob
```

Dictionary-style assignment is also supported:

```python
data["name"] = "Charlie"
```

Nested assignments are automatically converted when appropriate:

```python
data = Dottify({})

data.user = {
    "name": "Alice",
    "age": 30
}

print(data.user.name)
```

### Removing keys

Keys can be removed with `.remove()`:

```python
data = Dottify({
    "name": "Alice",
    "age": 30
})

data.remove("age")
```

Removal is case-sensitive and provides suggestions for incorrect key names.

### Dictionary interface

Dottify supports common dictionary operations:

```python
data = Dottify({
    "name": "Alice",
    "age": 30
})

print(len(data))
print(list(data.keys()))
print(list(data.values()))
print(list(data.items()))
```

You can also check whether a key exists:

```python
print(data.has_key("name"))     # True
print(data.has_key("Name"))     # False
print(data.has_key("unknown"))  # False
```

Standard dictionary-style operations such as `get()`, `pop()`, and `setdefault()` are also supported:

```python
data = Dottify({
    "name": "Alice"
})

print(data.get("name"))

data.setdefault("age", 30)

age = data.pop("age")
```

### Index-based access

Integer indexes can be used to access values by their position:

```python
people = Dottify({
    "Alice": {"age": 30},
    "Bob": {"age": 25},
    "Charlie": {"age": 35}
})

print(people[0].age)
print(people[1].age)
```

Indexing is zero-based.

### Lists and tuples

`Dottify` does **not** recursively convert dictionaries contained inside lists or tuples.

For example:

```python
from dottify import Dottify

data = Dottify({
    "users": [
        {"name": "Alice"},
        {"name": "Bob"}
    ]
})

print(type(data.users))
# <class 'list'>

print(type(data.users[0]))
# <class 'dict'>
```

Therefore, attribute-style access is not available for dictionaries inside the list:

```python
print(data.users[0].name)
# AttributeError
```

To recursively convert dictionaries, including dictionaries contained inside lists or tuples, use `convert()` instead:

```python
from dottify import convert

data = convert({
    "users": [
        {"name": "Alice"},
        {"name": "Bob"}
    ]
})

print(data.users[0].name)  # Alice
print(data.users[1].name)  # Bob
```

`convert()` recursively converts dictionaries at any level while preserving the surrounding container types.

### Wrapped functions

Dottify also provides the `@wrapped` decorator for automatically converting dictionaries created inside a function.

```python
from dottify import wrapped

@wrapped
def context():
    data = {
        "users": [
            {"name": "Alice"},
            {"name": "Bob"}
        ]
    }

    print(type(data))
    # <class 'dottify.core.Dottify'>

    print(data.users[1].name)
    # Bob
```

The decorator allows regular dictionary literals created inside the decorated function to be automatically converted to `Dottify`.

This is particularly useful when working with data structures containing lists of dictionaries, because the dictionaries inside those lists are also converted.

Without `@wrapped`, the same dictionary literal would remain a standard Python `dict`.

### `Dottify` vs `convert()` vs `@wrapped`

These three approaches have different purposes:

| Approach        | Nested dictionaries | Dicts inside lists/tuples | Usage                                                        |
| --------------- | ------------------- | ------------------------- | ------------------------------------------------------------ |
| `Dottify(data)` | Yes                 | No                        | Explicitly wrap a dictionary                                 |
| `convert(data)` | Yes                 | Yes                       | Recursively convert a data structure                         |
| `@wrapped`      | Yes                 | Yes                       | Automatically convert dictionaries created inside a function |

For example:

```python
from dottify import Dottify, convert, wrapped

# Direct wrapping
data = Dottify({
    "user": {
        "name": "Alice"
    }
})

print(data.user.name)
```

```python
# Recursive conversion
data = convert({
    "users": [
        {"name": "Alice"},
        {"name": "Bob"}
    ]
})

print(data.users[0].name)
```

```python
# Automatic conversion inside a function
@wrapped
def get_users():
    data = {
        "users": [
            {"name": "Alice"},
            {"name": "Bob"}
        ]
    }

    return data

data = get_users()

print(data.users[0].name)
```

### Numeric keys

Dictionary keys are handled consistently by Dottify, including numeric keys:

```python
data = Dottify({
    1: "one",
    2: "two"
})
```

Keys are normalized according to Dottify's internal key-handling rules.

### Merging

Dottify supports merging with the `+` operator:

```python
people = Dottify({
    "Alice": {
        "age": 30
    }
})

new_person = {
    "Bob": {
        "age": 25
    }
}

people = people + new_person

print(people.Bob.age)
```

The `+=` operator can be used for in-place merging:

```python
people += Dottify({
    "Charlie": {
        "age": 35
    }
})
```

### Conversion back to `dict`

A `Dottify` instance can be converted back to a standard Python dictionary:

```python
data = Dottify({
    "name": "Alice",
    "address": {
        "city": "Paris"
    }
})

normal_dict = data.to_dict()

print(type(normal_dict))
# <class 'dict'>
```

Nested `Dottify` instances are converted back to standard dictionaries as well.

### Copying and deep copying

Dottify supports both shallow and deep copying:

```python
from copy import copy, deepcopy

data = Dottify({
    "user": {
        "name": "Alice"
    }
})

shallow = copy(data)
deep = deepcopy(data)
```

### Pickling

Dottify instances can be serialized and restored using Python's `pickle` module:

```python
import pickle

data = Dottify({
    "name": "Alice"
})

serialized = pickle.dumps(data)
restored = pickle.loads(serialized)

print(restored.name)
```

## Complete Example

```python
from dottify import Dottify

people = Dottify({
    "Alice": {
        "age": 30,
        "city": "Paris",
        "profession": "Engineer"
    },
    "Charlie": {
        "age": 35,
        "city": "Marseille",
        "profession": "Doctor"
    }
})

# Attribute access
print(people.Alice.age)
print(people.Charlie.city)

# Dictionary-style access
print(people["Alice"].profession)

# Merge
people += {
    "Bob": {
        "age": 28,
        "city": "Lyon",
        "profession": "Designer"
    }
}

print(people.Bob.profession)

# Modify values
people.Alice.profession = "Developer"
people.Bob.age = 29

# Dictionary interface
print(len(people))
print(list(people.keys()))

# Check keys
print(people.has_key("Alice"))
print(people.has_key("alice"))

# Remove a key
people.remove("Bob")

# Convert back to a standard dictionary
normal_dict = people.to_dict()
```

## Testing

Dottify uses `pytest` for its test suite.

Run all tests with:

```sh
pytest tests/
```

The current test suite covers:

* Initialization from dictionaries and keyword arguments
* Nested dictionary conversion
* Attribute and item access
* Integer indexing
* Missing-key errors and suggestions
* Case-sensitive access
* Case-insensitive `get()`
* Attribute and item assignment
* Nested assignment conversion
* Dictionary conversion
* `keys()`, `values()`, `items()`
* `len()`
* `get()`
* `pop()`
* `setdefault()`
* Key removal
* `+` and `+=` operators
* Lists, tuples, and nested values
* Numeric keys
* Empty dictionaries and special values
* Copy and deep copy
* Pickling
* Equality
* String representation
* Edge cases

## Contributing

Contributions are welcome.

Please open an issue or submit a pull request on the [GitHub repository](https://github.com/nanaelie/dottify).

## License

Dottify is distributed under the MIT License. See [LICENSE](LICENSE) for more information.
