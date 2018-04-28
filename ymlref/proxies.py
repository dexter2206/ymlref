"""Proxy objects used by ymlref.

Those are read-only (immutable) objects that allow JSON reference resolving in transprent
way.
"""
from collections.abc import Mapping, Sequence
from jsonpointer import resolve_pointer


class ProxyBase:

    def __init__(self, wrapped, root_doc=None):
        self._wrapped = wrapped
        self.root_doc = root_doc if root_doc is not None else self


    def __len__(self):
        return len(self._wrapped)

    def resolve_ref(self, ref):
        if ref.startswith('#'):
            return resolve_pointer(self.root_doc, ref[1:])
        else:
            return resolve_pointer(self.root_doc, ref[1:])

    def extract_item(self, index):
        value = self._wrapped[index]
        if isinstance(value, Mapping):
            if '$ref' in value:
                return self.resolve_ref(value['$ref'])
            return MappingProxy(value, self.root_doc)
        elif isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
            return SequenceProxy(value, self.root_doc)
        else:
            return value


class MappingProxy(ProxyBase, Mapping):
    """Proxy wrapping Mapping object."""

    def __getitem__(self, key):
        return self.extract_item(key)

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
        return self.extract_item(idx)

    def __eq__(self, other):
        if not isinstance(other, Sequence):
            return False
        if len(self) != len(other):
            return False
        return all(value == other[idx] for idx, value in enumerate(self))
