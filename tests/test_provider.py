#
#
#

from os import environ

from itertools import permutations

from unittest import TestCase
# from unittest.mock import patch
# from requests_mock import ANY, mock as requests_mock
#
# import octodns_cloudns
#
# from octodns.provider import ProviderException
# from octodns.provider.base import BaseProvider
#
# from octodns_cloudns.client import ClouDNSClient, ClouDNSClientException,\
#     ClouDNSClientBadRequest, ClouDNSClientUnauthorized, ClouDNSClientNotFound

from octodns_cloudns.provider import \
    ClouDNSProvider, ClouDNSConfigurationException


class TestClouDNSProvider(TestCase):

    def setUp(self):
        # start with a clean env
        environ['CLOUDNS_API_AUTH_PASSWORD'] = ''
        environ['CLOUDNS_API_AUTH_ID'] = ''
        environ['CLOUDNS_API_SUB_AUTH_ID'] = ''
        environ['CLOUDNS_API_SUB_AUTH_USER'] = ''

    def test_config_needs_password(self):
        environ['CLOUDNS_API_AUTH_ID'] = '11111'
        environ['CLOUDNS_API_AUTH_PASSWORD'] = ''
        with self.assertRaises(ClouDNSConfigurationException) as ctx:
            ClouDNSProvider('test')
        self.assertEquals('Please configure auth_password or in environment '
                          'CLOUDNS_API_AUTH_PASSWORD', ctx.exception.message)

    def test_config_prefers_config_password(self):
        environ['CLOUDNS_API_AUTH_ID'] = '11111'
        environ['CLOUDNS_API_AUTH_PASSWORD'] = 'unused'
        ClouDNSProvider('test', auth_password='password')
        self.assertEquals('password', environ['CLOUDNS_API_AUTH_PASSWORD'])

    def test_config_needs_at_least_one_id(self):
        environ['CLOUDNS_API_AUTH_ID'] = ''
        environ['CLOUDNS_API_AUTH_PASSWORD'] = 'test_auth_password'
        with self.assertRaises(ClouDNSConfigurationException) as ctx:
            ClouDNSProvider('test')
        self.assertEquals('Please configure one of auth_id, '
                          'sub_auth_id, sub_auth_user or in environment '
                          'CLOUDNS_API_AUTH_ID, CLOUDNS_API_SUB_AUTH_ID, '
                          'CLOUDNS_API_SUB_AUTH_USER', ctx.exception.message)

    def test_config_accepts_at_most_one_id(self):
        environ['CLOUDNS_API_AUTH_PASSWORD'] = 'test_auth_password'
        for combination in permutations([
                'CLOUDNS_API_AUTH_ID', 'CLOUDNS_API_SUB_AUTH_ID',
                'CLOUDNS_API_SUB_AUTH_USER'], 2
        ):
            environ[combination[0]] = '11111'
            environ[combination[1]] = '22222'
            with self.assertRaises(ClouDNSConfigurationException) as ctx:
                ClouDNSProvider('test')
            self.assertEquals('Please configure at most one of auth_id, '
                              'sub_auth_id, sub_auth_user or in environment '
                              'CLOUDNS_API_AUTH_ID, CLOUDNS_API_SUB_AUTH_ID, '
                              'CLOUDNS_API_SUB_AUTH_USER',
                              ctx.exception.message)
        environ['CLOUDNS_API_AUTH_ID'] = '11111'
        environ['CLOUDNS_API_SUB_AUTH_ID'] = '22222'
        environ['CLOUDNS_API_SUB_AUTH_USER'] = '33333'
        with self.assertRaises(ClouDNSConfigurationException) as ctx:
            ClouDNSProvider('test')
        self.assertEquals('Please configure at most one of auth_id, '
                          'sub_auth_id, sub_auth_user or in environment '
                          'CLOUDNS_API_AUTH_ID, CLOUDNS_API_SUB_AUTH_ID, '
                          'CLOUDNS_API_SUB_AUTH_USER',
                          ctx.exception.message)

    def test_config_only_accepts_numeric_auth_id(self):
        environ['CLOUDNS_API_AUTH_ID'] = 'some_text'
        environ['CLOUDNS_API_AUTH_PASSWORD'] = 'test_auth_password'
        with self.assertRaises(ClouDNSConfigurationException) as ctx:
            ClouDNSProvider('test')
            self.assertEquals('Please use a decimal number for auth_id',
                              ctx.exception.message)

    def test_config_only_accepts_numeric_sub_auth_id(self):
        environ['CLOUDNS_API_SUB_AUTH_ID'] = 'some_text'
        environ['CLOUDNS_API_AUTH_PASSWORD'] = 'test_auth_password'
        with self.assertRaises(ClouDNSConfigurationException) as ctx:
            ClouDNSProvider('test')
            self.assertEquals('Please use a decimal number for sub_auth_id',
                              ctx.exception.message)
