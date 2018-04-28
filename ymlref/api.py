"""Publicly exposed API."""
from io import StringIO
import yaml
from ymlref.proxies import MappingProxy


def load(stream, raw_loader=yaml.load):
    """Load YAML docfrom a given stream.

    :param stream: file-like object to read a document from.
    :type stream: file-like
    :param raw_loader: a callable to use to load the raw document before making a proxy out of it.
     by default uses :py:func:`yaml.load` function fro `pyaml` package.
    :type raw_loader: callable.
    :rtype: :py:class:`ymlref.proxies.MappingProxy`
    """
    return MappingProxy(raw_loader(stream))

def loads(document_str, raw_loader=yaml.load):
    """Load YAML doc from a given string.

    This is just a wrapper around `load` function, which passes it `document_str` in `StringIO`.
    """
    return load(StringIO(document_str), raw_loader)
