#
#
#

from os import environ

from unittest import TestCase
from unittest.mock import patch
from requests_mock import ANY, mock as requests_mock

from cloudns_api.api import ApiResponse

from octodns_cloudns.client import ClouDNSClient, ClouDNSClientException,\
    ClouDNSClientBadRequest, ClouDNSClientUnauthorized, ClouDNSClientNotFound


class TestClouDNSClient(TestCase):

    def setUp(self):
        environ['CLOUDNS_API_AUTH_ID'] = '11111'
        environ['CLOUDNS_API_AUTH_PASSWORD'] = 'test_auth_password'
        with requests_mock() as mock:
            mock.get(ANY, status_code=200, json={
                'success': True,
                'status_code': 200,
                'payload': {
                    'status': 'Success',
                    'status_description': 'Success login.'
                }
            })
            self.client = ClouDNSClient()

    def test_illegal_module_call(self):
        with self.assertRaises(ClouDNSClientException) as ctx:
            self.client._call('nomod', 'noop')
        self.assertEquals('illegal module nomod', str(ctx.exception))

    def test_illegal_operation_call(self):
        with self.assertRaises(ClouDNSClientException) as ctx:
            self.client._call('api', 'noop')
        self.assertEquals('api has no operation noop', str(ctx.exception))

    def test_call_without_data(self):
        with requests_mock() as mock:
            mock.get(ANY, status_code=200, text='{}')
            self.client._call('record', 'get_available_record_types', 'domain')

    def test_call_without(self):
        with requests_mock() as mock:
            mock.get(ANY, status_code=200, text='{}')
            self.client._call('api', 'get_nameservers')

    @patch('octodns_cloudns.client.ClouDNSAPI.get_nameservers')
    def test_no_response(self, api):
        with self.assertRaises(ClouDNSClientException) as ctx:
            api.return_value = None
            self.client._call('api', 'get_nameservers')
        self.assertEquals('no response for api.get_nameservers',
                          ctx.exception.message)

    @patch('octodns_cloudns.client.ClouDNSAPI.api')
    def test_no_api_response(self, api):
        with self.assertRaises(ClouDNSClientException) as ctx:
            api.return_value = None
            self.client._call('api', 'get_nameservers')
        self.assertEquals(500, ctx.exception.response.status_code)
        self.assertEquals('Server Error', ctx.exception.message)

    def test_bad_request(self):
        with self.assertRaises(ClouDNSClientBadRequest) as ctx:
            with requests_mock() as mock:
                mock.get(ANY, status_code=400, json={})
                self.client._call('api', 'get_nameservers')
        self.assertEquals(400, ctx.exception.response.status_code)
        self.assertEquals('Bad Request', ctx.exception.message)

    def test_unauthorized_request(self):
        with self.assertRaises(ClouDNSClientUnauthorized) as ctx:
            with requests_mock() as mock:
                mock.get(ANY, status_code=401, json={})
                self.client._call('api', 'get_nameservers')
        self.assertEquals(401, ctx.exception.response.status_code)
        self.assertEquals('Unauthorized', ctx.exception.message)

    def test_not_found(self):
        with self.assertRaises(ClouDNSClientNotFound) as ctx:
            with requests_mock() as mock:
                mock.get(ANY, status_code=404, json={})
                self.client._call('api', 'get_nameservers')
        self.assertEquals(404, ctx.exception.response.status_code)
        self.assertEquals('Not Found', ctx.exception.message)

    def test_server_error(self):
        with self.assertRaises(ClouDNSClientException) as ctx:
            with requests_mock() as mock:
                mock.get(ANY, status_code=500, json={})
                self.client._call('api', 'get_nameservers')
        self.assertEquals(500, ctx.exception.response.status_code)
        self.assertEquals('Server Error', ctx.exception.message)

    def test_no_success(self):
        with self.assertRaises(ClouDNSClientException) as ctx:
            with requests_mock() as mock:
                mock.get(ANY, status_code=201, json={'success': False})
                self.client._call('api', 'get_nameservers')
        self.assertEquals(201, ctx.exception.response.status_code)
        self.assertEquals('No Success', ctx.exception.message)

    @patch('octodns_cloudns.client.ClouDNSAPI.get_nameservers')
    def test_no_status(self, api):
        with self.assertRaises(ClouDNSClientException) as ctx:
            api.return_value = ApiResponse()
            self.client._call('api', 'get_nameservers')
        self.assertEquals('API Internal Error', ctx.exception.message)
