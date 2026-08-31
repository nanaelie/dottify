import pytest
from dottify import Dottify
from dottify.exceptions import DottifyKNFError


"""
def test_knf_error_message():
    d = Dottify({"name": "Alice", "age": 30})

    with pytest.raises(DottifyKNFError) as exc:
        _ = d.missing_key

    assert "missing_key" in str(exc.value)
    assert "not found" in str(exc.value).lower()


def test_suggestion_in_error():
    d = Dottify({"username": "alice", "user_id": 42})

    with pytest.raises(DottifyKNFError) as exc:
        _ = d.user

    msg = str(exc.value)
    assert "Did you mean" in msg
    assert "username" in msg or "user_id" in msg
"""



def test_knf_error_message():
    d = Dottify({"name": "Alice", "age": 30})

    with pytest.raises(AttributeError) as exc:
        _ = d.missing_key

    assert "missing_key" in str(exc.value)
    assert "not found" in str(exc.value).lower()


def test_suggestion_in_error():
    d = Dottify({"username": "alice", "user_id": 42})

    with pytest.raises(AttributeError) as exc:
        _ = d.user

    msg = str(exc.value)
    assert "Did you mean" in msg
    assert "username" in msg or "user_id" in msg