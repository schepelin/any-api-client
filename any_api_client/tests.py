# -*- coding: utf-8 -*-
import unittest
import mock

from any_api_client.api import BaseAPIClass
from any_api_client.core import bind_method, ApiClientError


class TestApiClass(BaseAPIClass):
    test_method = bind_method(
        path='/foo/', accepts_params=['foo', 'bar']
    )


class ApiClientTests(unittest.TestCase):
    def setUp(self):
        pass



if __name__ == "__main__":
    unittest.main()
