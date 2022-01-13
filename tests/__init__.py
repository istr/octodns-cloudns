#
#
#

from os import environ

from unittest import TestCase

import octodns_cloudns

from octodns.provider import ProviderException
from octodns.provider.base import BaseProvider


class TestClouDNSModule(TestCase):

    def setUp(self):
        environ['CLOUDNS_API_AUTH_ID'] = '11111'
        environ['CLOUDNS_API_AUTH_PASSWORD'] = 'test_auth_password'

    def test_has_exceptions(self):
        assert octodns_cloudns.client.ClouDNSClientException is not None
        self.assertIsInstance(
            octodns_cloudns.client.ClouDNSClientException('msg'),
            ProviderException)
        assert octodns_cloudns.provider.ClouDNSConfigurationException\
            is not None
        self.assertIsInstance(
            octodns_cloudns.provider.ClouDNSConfigurationException(
                'msg', ['auth_id']),
            ProviderException)

    def test_has_classes(self):
        assert octodns_cloudns.provider.ClouDNSProvider is not None
        self.assertIsInstance(octodns_cloudns.provider.ClouDNSProvider('test'),
                              BaseProvider)
