import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dottify.dottify import Dottify
from dottify.exceptions import DottifyKNFError

def test_basic_access():
    data = {"user": {"name": "Alice", "age": 30}}
    d = Dottify(data)

    assert d.user.name == "Alice"
    assert d.user.age == 30
    assert isinstance(d.user, Dottify)

def test_key_error_with_suggestion():
    data = {"foo": "bar"}
    d = Dottify(data)
    
    with pytest.raises(DottifyKNFError) as excinfo:
        _ = d["fo"]  # close to "foo"
    assert "Did you mean" in str(excinfo.value)

def test_to_dict():
    data = {"x": {"y": 42}}
    d = Dottify(data)
    result = d.to_dict()
    assert result == data
    assert isinstance(result, dict)

def test_remove_key():
    data = {"a": 1, "b": 2}
    d = Dottify(data)
    d.remove("a")
    assert "a" not in d.keys()

def test_merge_add_operator():
    d1 = Dottify({"a": 1})
    d2 = Dottify({"b": 2})
    d3 = d1 + d2
    assert d3.a == 1
    assert d3.b == 2
    assert isinstance(d3, Dottify)

def test_merge_iadd_operator():
    d1 = Dottify({"a": 1})
    d2 = {"b": 2}
    d1 += d2
    assert d1.a == 1
    assert d1.b == 2

def test_case_insensitive_get():
    d = Dottify({"Name": "Bob"})
    assert d.get("name") == "Bob"
    assert d.get("NAME") == "Bob"
    assert d.get("notfound", "default") == "default"

