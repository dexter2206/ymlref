"""Test cases for publicly exposed API."""
from io import StringIO
import pytest
from ymlref import load, loads
from ymlref.proxies import MappingProxy


FLATTENED_DICT = {
    'components': {
        'pet': {'petId': 'number', 'name': 'string'},
        'person': {'name': 'string', 'age': 'number'}
    },
    'foo': {'petId': 'number', 'name': 'string'},
    'bar': 'number',
    'baz': [0, 1, {'name': 'string', 'age': 'number'}]
}

YML = """bar: {$ref: '#/components/person/age'}
baz:
- 0
- 1
- {$ref: '#/components/person'}
components:
  person: {age: number, name: string}
  pet: {name: string, petId: number}
foo: {$ref: '#/components/pet'}
"""

@pytest.fixture(name='stream')
def stream_factory():
    """Factory providing stream to read YML from."""
    stream = StringIO(YML)
    return stream

def test_load_yml(stream):
    """The load function should read data from stream and construct correct proxy."""
    doc = load(stream)
    assert doc == MappingProxy(FLATTENED_DICT)

def test_loads_yml():
    """The loads function should  construct correct proxy."""
    doc = loads(YML)
    assert doc == MappingProxy(FLATTENED_DICT)
