"""Proxy objects used by ymlref.

Those are read-only (immutable) objects that allow JSON reference resolving in transprent
way.
"""
from collections.abc import Mapping, Sequence
from jsonpointer import resolve_pointer


class ProxyBase:
    """Base class for concrete proxies."""

    def __init__(self, wrapped, root_doc=None):
        self._wrapped = wrapped
        self.root_doc = root_doc if root_doc is not None else self


    def __len__(self):
        return len(self._wrapped)

    def resolve_ref(self, ref):
        """Resolve given reference using this proxy's root document.

        :param ref: JSON reference string.
        :type ref: str
        :returns: proxy or concrete object, depending on which part of the document is referenced
         by the pointer.
        :rtype: object.
        """
        if ref.startswith('#'):
            return resolve_pointer(self.root_doc, ref[1:])
        return resolve_pointer(self.root_doc, ref[1:])

    def extract_item(self, index):
        """Extract top level item from document wrapped by this proxy.

        Note that this is generic method, it applies both to MappingProxy and SequenceProxy.
        It gets item from underlying object and, depending on its type, return either next
        proxy, or some other object present in document (i.e. int, str etc.).

        :param index: index of the element. Depending on the concrete implementation, this might
         be key to the dictionary or list index.
        :type index: arbitrary.
        :returns: item of the given index.
        :rtype: dependent on the type of the underlying item.
        """
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

    def get(self, key, default=None):
        """Get given key, if present, otherwise return default value.

        This behaves exactly like its `dict.get` counterpart.
        """
        if key in self:
            return self[key]
        return default

    def __in__(self, key):
        return key in self._wrapped

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


# It seems that Sequence class has a lot of ancestors and pylint does not like it
# We are deliberately disabling this warning only here.
class SequenceProxy(ProxyBase, Sequence): # pylint: disable=too-many-ancestors
    """Proxy wrapping Sequence object."""

    def __getitem__(self, idx):
        return self.extract_item(idx)

    def __eq__(self, other):
        if not isinstance(other, Sequence):
            return False
        if len(self) != len(other):
            return False
        return all(value == other[idx] for idx, value in enumerate(self))
