# -*- coding: utf-8 -*-

__all__ = (
    'BaseAPIClass',
)

class BaseAPIClass(object):

    def __init__(self, api_url):
        self.api_url = api_url
