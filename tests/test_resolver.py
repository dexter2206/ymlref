"""Test cases for Resolvers."""
import pytest
from ymlref.resolvers import DefaultResolver, ReferenceType


@pytest.fixture(name='resolver')
def resolver_factory():
    """Fixture providing DefaultResolver instance."""
    return DefaultResolver()

def test_classifies_reference(resolver):
    """DefaultResolver should correctly classify internal, local and remote references."""
    assert ReferenceType.INTERNAL == resolver.classify_ref('#/components/pet')
    assert ReferenceType.LOCAL == resolver.classify_ref('components.yml')
    assert ReferenceType.REMOTE == resolver.classify_ref('file://definitions.yml')
    assert ReferenceType.REMOTE == resolver.classify_ref('https://definitions.yml')
