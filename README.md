[![PyPI Downloads](https://static.pepy.tech/badge/dottify)](https://pepy.tech/projects/dottify)
![PyPI](https://img.shields.io/pypi/v/dottify?style=flat-square)
![GitHub stars](https://img.shields.io/github/stars/nanaelie/dottify?style=flat-square)
![GitHub forks](https://img.shields.io/github/forks/nanaelie/dottify?style=flat-square)
![GitHub issues](https://img.shields.io/github/issues/nanaelie/dottify?style=flat-square)
![GitHub last commit](https://img.shields.io/github/last-commit/nanaelie/dottify?style=flat-square)
![License](https://img.shields.io/github/license/nanaelie/dottify?style=flat-square)
![Python](https://img.shields.io/badge/python-3.x-blue?style=flat-square)

# Dottify

Dottify is a lightweight Python library that converts dictionaries into objects with attribute-style access. Instead of the usual `dict["key"]` syntax, you can access dictionary values using dot notation like `dict.key`. All access is **case-sensitive**, but helpful suggestions are provided when a key is missing.

## Installation

Install via pip:

```sh
pip install dottify
```

## Usage

Here’s an example of how Dottify works:

```python
from dottify import Dottify

# Initial data
persons = {
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
}

# Wrap with Dottify
people = Dottify(persons)

# Merge with + operator (__add__)
new_person = {
    "Bob": {
        "age": 2,
        "city": "Lyon",
        "profession": "Designer"
    }
}
people = people + new_person

# In-place merge with += (__iadd__)
people += Dottify({
    "John": {
        "age": 27,
        "city": "Toulouse",
        "profession": "Carpenter"
    }
})

# Access by dot notation and key lookup
print(people.Alice.age)             # 30
print(people["Charlie"].city)       # Marseille
print(people.Bob.profession)        # Designer

# Index-based access (__getitem__)
print(people[3].profession)         # Carpenter (John)

# Modify attributes
people.John.profession = "Developer"
people.Bob.age = 39

# Use get() with case-insensitive fallback
print(people.get("alice", "Not Found").city)     # Paris
print(people.get("ALICIA", "Not Found"))         # Not Found

# Remove a key by name (case-sensitive)
people.remove("Bob")  # Removes Bob

# Check if a key exists (case-insensitive)
print(people.has_key("charlie"))     # False (because 'charlie' != 'Charlie')
print(people.has_key("Charlie"))     # True
print(people.has_key("unknown"))     # False

# Use len(), keys(), values(), items()
print(len(people))                   # 3 (Alice, Charlie, John)
print(list(people.keys()))           # ['Alice', 'Charlie', 'John']
print([v.city for v in people.values()])  # ['Paris', 'Marseille', 'Toulouse']
print([(k, v.age) for k, v in people.items()])  # [('Alice', 30), ('Charlie', 35), ('John', 27)]
```

## Features

* Converts standard and nested dictionaries into objects with attribute access.
* Supports both dot notation (`obj.key`) and dictionary-style (`obj["key"]`) access.
* All access is **case-sensitive**.
* Friendly error messages with key suggestions (case-insensitive search).
* Key removal with `.remove("Key")` is **case-sensitive**, but also provides suggestions if the key doesn't match.
* Easily convert back to a standard dict using `.to_dict()`.
* Supports `.keys()`, `.values()`, `.items()`, iteration, and `len()` additions.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests on the [GitHub repository](https://github.com/nanaelie/dottify).

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

