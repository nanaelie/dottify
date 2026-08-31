import pytest
from dottify import Dottify

@pytest.fixture
def sample_data():
    return {
        "name": "Alice",
        "age": 30,
        "active": True,
        "address": {
            "city": "New York",
            "zip": "10001",
            "coords": {"lat": 40.71, "lng": -74.00},
        },
        "tags": ["admin", "user"],
        "scores": [10, 20, 30],
    }


@pytest.fixture
def d(sample_data):
    """A fully converted Dottify instance."""
    return Dottify(sample_data)