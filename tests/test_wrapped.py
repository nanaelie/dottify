from dottify import Dottify, wrapped

def test_wrapped():

    @wrapped
    def fwrapped():
        d = {
            'name': 'Alice', 
            'age': 20,
            'pos': {
                'x': 176,
                'y': 152
            }
        }

        assert isinstance(d, Dottify)
        assert isinstance(d.pos, Dottify)

        assert d.pos.x == 176

    d = {
        'name': 'Alice', 
        'age': 20,
        'pos': {
            'x': 176,
            'y': 152
        }
    }

    assert isinstance(d, dict)

