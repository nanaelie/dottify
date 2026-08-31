import copy
import pickle
import pytest
from dottify import Dottify, convert, DottifyKNFError


class TestEdgeCases:
    def test_empty_dict(self):
        d = Dottify({})
        assert len(d) == 0
        assert d.to_dict() == {}
        assert list(d.keys()) == []

    def test_none_value(self):
        d = Dottify({"key": None})
        assert d.key is None
        assert d["key"] is None

    def test_boolean_values(self):
        d = Dottify({"active": True, "disabled": False})
        assert d.active is True
        assert d.disabled is False

    def test_numeric_keys_are_strings(self):
        d = Dottify({"1": "one", "2": "two"})
        assert d["1"] == "one"
        # Integer access is by position (insertion order), not by key
        assert d[0] == "one"
        assert d[1] == "two"

    def test_pop_missing_raises(self):
        d = Dottify({"a": 1})
        with pytest.raises(DottifyKNFError):
            d.pop("missing")


    def test_integer_index_out_of_range(self):
        d = Dottify({"a": 1, "b": 2})
        with pytest.raises(DottifyKNFError, match="out of range"):
            _ = d[10]


    def test_exact_match_required_for_access(self):
        d = Dottify({"Name": "Alice"})
        assert d.Name == "Alice"
        with pytest.raises(AttributeError):
            _ = d.name  # different case

    def test_special_characters_in_keys(self):
        d = Dottify({"user-name": "alice", "user.name": "bob", "user_name": "charlie"})
        assert d["user-name"] == "alice"
        assert d["user.name"] == "bob"
        assert d.user_name == "charlie"

    def test_deeply_nested(self):
        data = {"a": {"b": {"c": {"d": {"e": "deep"}}}}}
        d = Dottify(data)
        assert d.a.b.c.d.e == "deep"
        assert isinstance(d.a.b.c.d, Dottify)

    def test_list_of_dicts_not_auto_converted(self):
        d = Dottify({"users": [{"id": 1}, {"id": 2}]})
        assert isinstance(d.users, list)
        assert isinstance(d.users[0], dict)  # stays as normal dict
        assert not isinstance(d.users[0], Dottify)

    def test_convert_list_of_dicts(self):
        data = {"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]}
        d = convert(data)
        assert isinstance(d.users[0], Dottify)
        assert d.users[0].name == "Alice"
        assert d.users[1].id == 2

    def test_tuple_and_list_values(self):
        d = Dottify({
            "coords": (10, 20),
            "tags": ["a", "b", "c"],
        })
        assert d.coords == (10, 20)
        assert d.tags == ["a", "b", "c"]

    def test_copy(self):
        d = Dottify({"name": "Alice", "address": {"city": "NYC"}})
        d2 = copy.copy(d)
        assert d2.name == "Alice"
        assert d2 is not d
        # Shallow copy shares nested objects
        d2.address.city = "LA"
        assert d.address.city == "LA"

    def test_deepcopy(self):
        d = Dottify({"name": "Alice", "address": {"city": "NYC"}})
        d2 = copy.deepcopy(d)
        assert d2.name == "Alice"
        assert d2 is not d
        assert d2.address is not d.address
        d2.address.city = "LA"
        assert d.address.city == "NYC"

    def test_pickle(self):
        d = Dottify({"name": "Alice", "age": 30, "address": {"city": "NYC"}})
        data = pickle.dumps(d)
        d2 = pickle.loads(data)
        assert isinstance(d2, Dottify)
        assert d2.name == "Alice"
        assert d2.address.city == "NYC"

    def test_update_with_dict(self):
        d = Dottify({"a": 1})
        d.update({"b": 2, "c": {"d": 3}})
        assert d.b == 2
        assert isinstance(d.c, Dottify)
        assert d.c.d == 3

    def test_update_with_dottify(self):
        d = Dottify({"a": 1})
        other = Dottify({"b": 2})
        d.update(other)
        assert d.b == 2

    def test_pop_missing_with_default(self):
        d = Dottify({"a": 1})
        assert d.pop("missing", "default") == "default"

    def test_pop_missing_raises(self):
        d = Dottify({"a": 1})
        with pytest.raises(DottifyKNFError):
            d.pop("missing")

    def test_delete_attribute(self):
        d = Dottify({"name": "Alice", "age": 30})
        del d.age
        assert "age" not in d
        with pytest.raises(AttributeError):
            _ = d.age

    def test_delete_item(self):
        d = Dottify({"name": "Alice", "age": 30})
        del d["age"]
        assert "age" not in d

    def test_integer_index_out_of_range(self):
        d = Dottify({"a": 1, "b": 2})
        with pytest.raises(DottifyKNFError, match="out of range"):
            _ = d[10]

    def test_equality(self):
        d1 = Dottify({"a": 1, "b": {"c": 2}})
        d2 = Dottify({"a": 1, "b": {"c": 2}})
        d3 = Dottify({"a": 1, "b": {"c": 3}})
        assert d1 == d2
        assert d1 != d3
        assert d1 == {"a": 1, "b": {"c": 2}}  # compares equal to normal dict

    def test_repr_and_str(self):
        d = Dottify({"name": "Alice"})
        assert "Dottify" in repr(d)
        assert "Alice" in repr(d)
        assert repr(d) == str(d)

# Je ne comprends pas ce que ce (test_exact_match_required_for_access) test teste exactement sans param match=.
class TestCaseSensitivity:
    def test_exact_match_required_for_access(self):
        d = Dottify({"Name": "Alice"})
        assert d.Name == "Alice"
        with pytest.raises(AttributeError):
            _ = d.name

    def test_get_is_case_sensitive(self):
        d = Dottify({"Name": "Alice"})
        assert d.get("Name") == "Alice"
        assert d.get("name") is None

