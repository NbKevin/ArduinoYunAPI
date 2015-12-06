#!/usr/env/bin python
# -*- encoding: utf-8 -*-

"""
Useful utilities.
"""

import contextlib
import json

__author__ = 'Nb'


@contextlib.contextmanager
def open_and_save(path: str, save=True, encoding='utf-8', decoder=None, encoder=None):
    """
    A patched version of open which automatically saves file
    after the with block ends.

    This greatly relies on the fact that python actually
    passes references instead of values. Therefore you can
    only operate on the attributes of the returned object
    but not the object itself. Otherwise the context manager
    would not be able to trace the change.

    The JSON parser is used by default to process the raw
    data read in. Custom parser should be able to handle
    IO like objects.

    :param path: The path to the file.
    :param save: Whether to save the file.
    :param encoding: The encoding to be used to read the file.
    :param decoder: The custom decoder.
    :param encoder: The custom encoder.
    """
    decoder = json.load if decoder is None else decoder
    encoder = json.dump if encoder is None else encoder
    with open(path, mode='r', encoding=encoding) as file:
        content = decoder(file)
    try:
        yield content
    except Exception as e:
        raise e
    finally:
        if save:
            with open(path, mode='w', encoding=encoding) as file:
                encoder(content, file)


class SingletonMeta(type):
    """Meta class for creating singleton class."""
    __instance_dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instance_dict:
            cls.__instance_dict[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls.__instance_dict[cls]
