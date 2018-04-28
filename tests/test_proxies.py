""""Test cases for proxy objects."""
import pytest
from ymlref.proxies import MappingProxy, SequenceProxy


PLAIN_DICT = {
    'foo': 'bar',
    'baz': {
        'type': 'object',
        'number': 200,
        'list': [0, 1, 2, 3]
    }
}

PLAIN_LIST = [0, 1.0, 'foobar']

def test_plain_dict_access():
    """MappingProxy should allow accessing objects in wrapped plain dictionary using __getitem__."""
    proxy = MappingProxy(PLAIN_DICT)
    assert proxy['foo'] == 'bar'
    assert proxy['baz']['type'] == 'object'
    assert proxy['baz']['number'] == 200

def test_plain_list_access():
    """SequenceProxy should allow accessing elements using __getitem__."""
    proxy = SequenceProxy(PLAIN_LIST)
    assert proxy[0] == 0
    assert proxy[1] == 1.0
    assert proxy[2] == 'foobar'

def test_correct_len():
    """MappingProxy should have the same length as the wrapped dict."""
    proxy = MappingProxy(PLAIN_DICT)
    assert len(proxy) == 2, 'Should have length equal to length of wrapped dict.'

def test_equals_plain_dict():
    """MappingProxy should compare as equal to the wrapped plain dictionary."""
    proxy = MappingProxy(PLAIN_DICT)
    assert proxy == PLAIN_DICT, 'Should compare as equal to wrapped plain dict.'

def test_notequals_to_other_dict():
    """MappingProxy should not compare as equal to different dict than the wrapped one."""
    proxy = MappingProxy(PLAIN_DICT)
    other_dict = {'foo': 'baz', 'baz': 100}
    assert proxy != other_dict, 'Should compare as not equal.'

def test_equals_plain_list():
    """SequenceProxy should compare as equal to the wrapped plain list."""
    proxy = SequenceProxy(PLAIN_LIST)
    assert proxy == PLAIN_LIST, 'Should compare as equal to wrapped plain list.'

@pytest.mark.parametrize('other', [[1, 3, 'xyz'], 100, [1, 'a', 'b', 'c']])
def test_notequals_to_other_list(other):
    """SequenceProxy should not compare as equal to different object than the wrapped one."""
    proxy = SequenceProxy(PLAIN_LIST)
    assert proxy != other, 'Should compare as not equal.'
