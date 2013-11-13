# -*- coding: utf-8 -*-

import re
import json

import requests

from any_api_client.response import BaseAPIResponse


__all__ = (
    'bind_method',
    'ApiClientError',
)


class ApiClientError(Exception):
    def __init__(self, error_message):
        self.error_message = error_message

    def __str__(self):
        return self.error_message


def bind_method(**config):

    class APIMethod(object):
        path = config['path']
        method = config.get('method', 'GET')
        accepts_params = config.get('accepts_params', [])
        preprocessor = config.get('preprocessor', lambda x: x)
        timeout = config.get('timeout', 10)
        response_class = config.get('response_class', BaseAPIResponse)

        def __init__(self, api, *args, **kwargs):
            self.params = {}
            self._build_params(args[1:], kwargs)

        def _build_params(self, args, kwargs):
            for index, value in enumerate(args):
                if value is None:
                    continue
                try:
                    self.params[self.accepts_params[index]] = self.preprocessor(value)
                except IndexError:
                    raise ApiClientError(u'Too many arguments supplied')

            for key, value in kwargs.iteritems():

                if value is None:
                    continue
                if key in self.params:
                    raise ApiClientError(u'Parameter %s already supplied' % key)

                self.params[key] = self.preprocessor(value)

        @property
        def request_url(self):
            if not hasattr(self, '_request_url'):
                url = re.sub(r'(\w)//(\w)', lambda m: '%s/%s'%(m.group(1),m.group(2)),
                        '%s%s' % (self.api.api_url, self.path))
                self._request_url = url
            return self._request_url

        def make_request(self):
            try:
                response = requests.request(self.method, self.request_url,
                                            data=self.params,
                                            timeout=self.timeout)
            except requests.RequestException as e:
                content = {
                    'request': {
                        'url': self.request_url,
                        'method': self.method,
                        'data': self.params,
                    },
                    'error': unicode(e),
                }
                status_code = 400
            else:
                status_code = response.status_code

                try:
                    content = json.loads(response.text)
                except ValueError as e:
                    raise ApiClientError(u'Unable to parse response, '
                                         u'not valid JSON. Response: %s' % response.text)

            return self.response_class(status_code=status_code, data=content)

    def _call(api, *args, **kwargs):
        method = APIMethod(api, *args, **kwargs)
        return method.make_request()

    return _call
