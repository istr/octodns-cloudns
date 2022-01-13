#
#
#

import logging

from octodns.provider import ProviderException

from cloudns_api import api as ClouDNSAPI, record as ClouDNSRecord,\
    soa as ClouDNSStartOfAuthority, zone as ClouDNSZone

__VERSION__ = '0.0.1'


class ClouDNSClientException(ProviderException):

    def __init__(self, message, response=None):
        self._message = message
        self._response = response
        super(ClouDNSClientException, self).__init__(message)

    @property
    def response(self):
        return self._response

    @property
    def message(self):
        return self._message


class ClouDNSClientBadRequest(ClouDNSClientException):

    def __init__(self, resp):
        super(ClouDNSClientBadRequest, self).__init__('Bad Request', resp)


class ClouDNSClientUnauthorized(ClouDNSClientException):

    def __init__(self, resp):
        super(ClouDNSClientUnauthorized, self).__init__('Unauthorized', resp)


class ClouDNSClientNotFound(ClouDNSClientException):

    def __init__(self, resp):
        super(ClouDNSClientNotFound, self).__init__('Not Found', resp)


class ClouDNSClient(object):

    def __init__(self):
        self.log = logging.getLogger('ClouDNSClient')
        self.log.debug('__init__')
        self.module = {
            'api': ClouDNSAPI,
            'zone': ClouDNSZone,
            'record': ClouDNSRecord,
            'soa': ClouDNSStartOfAuthority
        }
        # check that login works
        self._call('api', 'get_login')

    def _call(self, module, operation, data=None):
        mod = self.module.get(module)
        if not mod:
            raise ClouDNSClientException(f'illegal module {module}')
        fun = getattr(mod, operation, None)
        if not fun:
            raise ClouDNSClientException(
                f'{module} has no operation {operation}')
        resp = fun(data) if data else fun()
        if not resp:
            raise ClouDNSClientException(
                f'no response for {module}.{operation}')
        self.log.debug("RESP %s", resp)
        status_code = resp.status_code
        if 400 == status_code:
            raise ClouDNSClientBadRequest(resp)
        if 401 == status_code:
            raise ClouDNSClientUnauthorized(resp)
        if 404 == status_code:
            raise ClouDNSClientNotFound(resp)
        if 500 == status_code:
            raise ClouDNSClientException('Server Error', resp)
        if status_code is None:
            raise ClouDNSClientException('API Internal Error', resp)
        if not resp.success:
            raise ClouDNSClientException('No Success', resp)

        return resp.payload
