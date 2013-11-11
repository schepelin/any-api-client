# -*- coding: utf-8 -*-

__all__ = (
    'BaseAPIResponse',
)


class BaseAPIResponse(object):

    def __init__(self, status_code, data):
        self.data = data
        self.status_code = status_code

    @property
    def success(self):
        return self.status_code == 200

    @property
    def failed(self):
        return self.status_code != 200
