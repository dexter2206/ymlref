"""Proxy objects used by ymlref.

Those are read-only (immutable) objects that allow JSON reference resolving in transprent
way.
"""
from collections.abc import Mapping, Sequence


class ProxyBase:

    def __init__(self, wrapped):
        self._wrapped = wrapped


    def __len__(self):
        return len(self._wrapped)


class MappingProxy(ProxyBase, Mapping):
    """Proxy wrapping Mapping object."""

    def __getitem__(self, key):
        value = self._wrapped[key]
        if isinstance(value, Mapping):
            return MappingProxy(value)
        elif isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
            return SequenceProxy(value)
        else:
            return value

    def __iter__(self):
        return iter(self._wrapped)

    def __eq__(self, other):
        if not isinstance(other, Mapping):
            return False
        if len(self) != len(other):
            return False
        for key in self:
            if key not in other:
                return False
            if not self[key] == other[key]:
                return False
        return True


class SequenceProxy(ProxyBase, Sequence):
    """Proxy wrapping Sequence object."""

    def __getitem__(self, idx):
        value = self._wrapped[idx]
        if isinstance(value, Mapping):
            return MappingProxy(value)
        elif isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
            return SequenceProxy(value)
        else:
            return value

    def __eq__(self, other):
        if not isinstance(other, Sequence):
            return False
        if len(self) != len(other):
            return False
        return all(value == other[idx] for idx, value in enumerate(self))
