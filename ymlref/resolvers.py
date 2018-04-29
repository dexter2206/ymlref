"""Classes used for resolving pointers and externals references."""
import abc
from enum import Enum, auto
import re


class ReferenceType(Enum):
    INTERNAL = 'internal'
    LOCAL = 'local'
    REMOTE = 'remote'


class Resolver(abc.ABC):

    SCHEMA_REGEXP = '[A-Za-z]+://'

    @classmethod
    def classify_ref(cls, reference):
        if reference.startswith('#') or reference.startswith('/'):
            return ReferenceType.INTERNAL
        if re.match(cls.SCHEMA_REGEXP, reference):
            return ReferenceType.REMOTE
        return ReferenceType.LOCAL


class DefaultResolver(Resolver):
    pass
