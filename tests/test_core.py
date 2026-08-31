import pytest
from dottify import Dottify, convert, DottifyKNFError


class TestInitialization:
    def test_empty(self):
        d = Dottify()
        assert len(d) == 0
        assert d.to_dict() == {}

    def test_from_dict(self, sample_data):
        d = Dottify(sample_data)
        assert d.name == "Alice"
        assert d.age == 30
        assert isinstance(d.address, Dottify)

    def test_from_kwargs(self):
        d = Dottify(name="Bob", age=25)
        assert d.name == "Bob"
        assert d["age"] == 25

    def test_nested_conversion(self, d):
        assert isinstance(d.address, Dottify)
        assert isinstance(d.address.coords, Dottify)
        assert d.address.city == "New York"
        assert d.address.coords.lat == 40.71


class TestAccess:
    def test_attribute_access(self, d):
        assert d.name == "Alice"
        assert d.address.city == "New York"

    def test_item_access(self, d):
        assert d["name"] == "Alice"
        assert d["address"]["city"] == "New York"

    def test_integer_index(self, d):
        # Insertion order
        assert d[0] == "Alice"          # first value
        assert d[1] == 30

    def test_missing_key_raises(self, d):
        with pytest.raises(AttributeError, match="not found"):
            _ = d.missing

        with pytest.raises(DottifyKNFError, match="not found"):
            _ = d["missing"]

    def test_suggestion(self, d):
        with pytest.raises(AttributeError, match="Did you mean"):
            _ = d.nam

        with pytest.raises(DottifyKNFError, match="Did you mean"):
            _ = d['nam']  # close to "name"


class TestAssignment:
    def test_attribute_assignment(self, d):
        d.country = "USA"
        assert d.country == "USA"
        assert d["country"] == "USA"

    def test_item_assignment(self, d):
        d["country"] = "Canada"
        assert d.country == "Canada"

    def test_nested_assignment_converts(self, d):
        d.profile = {"theme": "dark"}
        assert isinstance(d.profile, Dottify)
        assert d.profile.theme == "dark"


class TestConversion:
    def test_to_dict(self, d, sample_data):
        result = d.to_dict()
        assert isinstance(result, dict)
        assert not isinstance(result, Dottify)
        assert result["name"] == "Alice"
        assert isinstance(result["address"], dict)

    def test_convert_helper(self, sample_data):
        converted = convert(sample_data)
        assert isinstance(converted, Dottify)
        assert isinstance(converted.address, Dottify)
        assert isinstance(converted.tags, list)
        assert converted.tags[0] == "admin"


class TestDictInterface:
    def test_keys_values_items(self, d):
        assert "name" in d.keys()
        assert "Alice" in d.values()
        assert ("name", "Alice") in d.items()

    def test_len(self, d):
        assert len(d) == 6

    def test_contains(self, d):
        assert "name" in d
        assert "missing" not in d

    def test_get(self, d):
        assert d.get("name") == "Alice"
        assert d.get("missing") is None
        assert d.get("missing", "default") == "default"

    def test_pop(self, d):
        age = d.pop("age")
        assert age == 30
        assert "age" not in d

    def test_update(self, d):
        d.update({"country": "USA", "age": 31})
        assert d.country == "USA"
        assert d.age == 31

    def test_setdefault(self, d):
        assert d.setdefault("name", "Bob") == "Alice"
        assert d.setdefault("new", "value") == "value"
        assert d.new == "value"


class TestOperators:
    def test_add(self, d):
        other = Dottify({"country": "USA"})
        merged = d + other
        assert merged.country == "USA"
        assert merged.name == "Alice"
        assert "country" not in d  # original unchanged

    def test_iadd(self, d):
        d += {"country": "USA"}
        assert d.country == "USA"


class TestEdgeCases:
    def test_empty_nested(self):
        d = Dottify({"empty": {}})
        assert isinstance(d.empty, Dottify)
        assert len(d.empty) == 0

    def test_none_values(self):
        d = Dottify({"value": None})
        assert d.value is None

    def test_boolean_values(self):
        d = Dottify({"active": False})
        assert d.active is False

    def test_list_of_dicts(self):
        d = Dottify({"users": [{"id": 1}, {"id": 2}]})
        assert isinstance(d.users, list)
        # Note: lists of dicts are not auto-converted unless using convert()

