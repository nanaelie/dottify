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

