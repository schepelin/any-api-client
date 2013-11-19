# -*- coding: utf-8 -*-
import unittest
from mock import patch

from api import BaseAPIClass
from core import bind_method, ApiClientError
from response import BaseAPIResponse


class FakeResponse(object):
    u"""
    Uses for mock requests.request
    """
    status_code = None
    content = None
    text = None
    parent = None
    headers = None

    def __init__(self, status_code, text, content=None):
        self.status_code = status_code
        self.text = text
        self.content = content


class CustomResponseClass(BaseAPIResponse):

    def __init__(self, status_code, data):
        self.status_code = status_code
        self.__dict__.update(data)


class TestApiClass(BaseAPIClass):
    u"""
    Api wrapper for tests
    """
    simple_method = bind_method(
        path='/foo/', accepts_params=['foo', 'bar']
    )

    custom_response_method = bind_method(
        path='/foo/bar/', accepts_params=['foo', 'bar'],
        response_class=CustomResponseClass
    )


def make_fake_request(fake_response_instance):
    def fake_response(method, request_url, data, timeout):
        return fake_response_instance
    return fake_response


class ApiClientTests(unittest.TestCase):
    def setUp(self):
        self.client = TestApiClass(api_url='http://test_url.test/')

    @patch('requests.request', new=make_fake_request(FakeResponse(200, '{"success": true}')))
    def test_base(self):
        response = self.client.simple_method(foo='foo', bar='bar')
        self.assertEqual(response.success, True)
        self.assertEqual(response.data, {'success': True})

    @patch('requests.request', new=make_fake_request(FakeResponse(200, 'just string')))
    def test_incorrect_json(self):
        with self.assertRaises(ApiClientError) as ex:
            response = self.client.simple_method(foo='foo', bar='bar')
            self.assertEqual(
                ex.error_message,
                u'Unable to parse response, not valid JSON. Response: just string'
            )
            self.assertEqual(response.success, False)
            self.assertEqual(response.failed, True)

    @patch('requests.request', new=make_fake_request(FakeResponse(200, '{"success": true}')))
    def test_paramalready_supplied(self):
        with self.assertRaises(ApiClientError) as ex:
            response = self.client.simple_method('test', foo='foo', bar='bar')
            self.assertEqual(ex.error_message, u'Parameter foo already supplied')
            self.assertEqual(response.success, False)

    @patch('requests.request', new=make_fake_request(FakeResponse(200, '{"success": true}')))
    def test_to_many_arguments(self):
        with self.assertRaises(ApiClientError) as ex:
            response = self.client.simple_method('foo', 'bar', 'test')
            self.assertEqual(ex.error_message, u'Too many arguments supplied')
            self.assertEqual(response.success, False)

    @patch('requests.request', new=make_fake_request(FakeResponse(200, '{"foo": 10, "bar": 20}')))
    def test_custom_response(self):
        response = self.client.custom_response_method('foo', 'bar')
        self.assertEqual(response.foo, 10)
        self.assertEqual(response.bar, 20)


if __name__ == "__main__":
    unittest.main()
