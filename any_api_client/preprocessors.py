# -*- coding: utf-8 -*-

import cPickle as pickle

__all__ = (
    'default_preprocessor',
    'pickle_preprocessor'
)


def default_preprocessor(method, value):
    return value


def pickle_preprocessor(method, value):
    return pickle.dumps(value)
