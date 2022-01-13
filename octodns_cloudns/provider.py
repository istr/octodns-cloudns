#
#
#

from os import environ
import logging

# TODO from octodns.record import Record
from octodns.provider import ProviderException
from octodns.provider.base import BaseProvider

# TODO
# from octodns_cloudns.client import ClouDNSClient, ClouDNSClientException,\
#     ClouDNSClientBadRequest, ClouDNSClientUnauthorized, ClouDNSClientNotFound

__VERSION__ = '0.0.1'


class ClouDNSConfigurationException(ProviderException):

    def __init__(self, message, values):
        env_values = []
        for value in values:
            env_values.append(f'CLOUDNS_API_{value.upper()}')

        msg = ' '.join([
            message, ', '.join(values),
            'or in environment', ', '.join(env_values)
        ])
        self._message = msg
        super(ClouDNSConfigurationException, self).__init__(f'\n{msg}')

    @property
    def message(self):
        return self._message


class ClouDNSProvider(BaseProvider):
    SUPPORTS_GEO = False
    SUPPORTS_DYNAMIC = True
    SUPPORTS = set(('A', 'AAAA', 'ALIAS', 'CAA', 'CNAME', 'MX', 'NAPTR', 'NS',
                    'PTR', 'SPF', 'SRV', 'SSHFP', 'URLFWD', 'TXT'))

    '''
    ClouDNS provider

    ClouDNS allows sub accounts for resellers or to lock and limit access.
    For API authentication one of three options could be given exclusively:
    `auth_id` for a primary account id, `sub_auth_id` for a sub account,
    identified by id, or `sub_auth_user` for sub account, identified by name.

    cloudns:
        class: octodns_cloudns.ClouDNSProvider
        auth_password: env/CLOUDNS_API_AUTH_PASSWORD
        # use exactly one of auth_id, sub_auth_id, or sub_auth_user
        auth_id: env/CLOUDNS_API_AUTH_ID
        # sub_auth_id: env/CLOUDNS_API_SUB_AUTH_ID
        # sub_auth_user: env/CLOUDNS_API_SUB_AUTH_USER
    '''

    def __init__(self, id, auth_password=None, auth_id=None, sub_auth_id=None,
                 sub_auth_user=None, *args, **kwargs):
        self.log = logging.getLogger(f'ClouDNSProvider[{id}]')

        # cloudns_api expects credentials in environ
        if auth_password:
            environ['CLOUDNS_API_AUTH_PASSWORD'] = str(auth_password)

        if not environ.get('CLOUDNS_API_AUTH_PASSWORD'):
            raise ClouDNSConfigurationException(
                'Please configure', ['auth_password'])

        # Load defaults from environ
        auth_id = auth_id or environ.get('CLOUDNS_API_AUTH_ID')
        sub_auth_id = sub_auth_id or environ.get('CLOUDNS_API_SUB_AUTH_ID')
        sub_auth_user = sub_auth_user or \
            environ.get('CLOUDNS_API_SUB_AUTH_USER')

        # Assure type safety for IDs
        if auth_id:
            auth_id = str(auth_id)
            if not auth_id.isdecimal():
                raise ClouDNSConfigurationException(
                    'Please use a decimal number for', ['auth_id'])
        if sub_auth_id:
            sub_auth_id = str(auth_id)
            if not sub_auth_id.isdecimal():
                raise ClouDNSConfigurationException(
                    'Please use a decimal number for', ['sub_auth_id'])

        # Check if exactly one is given
        if (auth_id and sub_auth_id) or (auth_id and sub_auth_user) or \
                (sub_auth_id and sub_auth_user):
            raise ClouDNSConfigurationException(
                'Please configure at most one of',
                ['auth_id', 'sub_auth_id', 'sub_auth_user'])
        if not (auth_id or sub_auth_id or sub_auth_user):
            raise ClouDNSConfigurationException(
                'Please configure one of',
                ['auth_id', 'sub_auth_id', 'sub_auth_user'])

        # Set up the environment for cloudns_api module
        environ['CLOUDNS_API_AUTH_ID'] = auth_id or ''
        environ['CLOUDNS_API_SUB_AUTH_ID'] = sub_auth_id or ''
        environ['CLOUDNS_API_SUB_AUTH_USER'] = sub_auth_user or ''

    '''
    --- TODO ---

    def _data_for_multiple(self, _type, records):
        pass

    _data_for_A = _data_for_multiple
    _data_for_AAAA = _data_for_multiple
    _data_for_SPF = _data_for_multiple

    def _data_for_TXT(self, _type, records):
        pass

    def _data_for_CAA(self, _type, records):
        pass

    def _data_for_CNAME(self, _type, records):
        pass

    def _data_for_MX(self, _type, records):
        pass

    def _data_for_NAPTR(self, _type, records):
        pass

    def _data_for_NS(self, _type, records):
        pass

    def _data_for_PTR(self, _type, records):
        pass

    def _data_for_SRV(self, _type, records):
        pass

    def _data_for_SSHFP(self, _type, records):
        pass

    def zone_records(self, zone):
        pass

    def populate(self, zone, target=False, lenient=False):
        pass

    def supports(self, record):
        pass

    def _params_for_multiple(self, record):
        pass

    _params_for_A = _params_for_multiple
    _params_for_AAAA = _params_for_multiple
    _params_for_NS = _params_for_multiple
    _params_for_SPF = _params_for_multiple

    def _params_for_TXT(self, record):
        pass

    def _params_for_CAA(self, record):
        pass

    def _params_for_single(self, record):
        pass

    _params_for_ALIAS = _params_for_single
    _params_for_CNAME = _params_for_single
    _params_for_PTR = _params_for_single

    def _params_for_MX(self, record):
        pass

    def _params_for_NAPTR(self, record):
        pass

    def _params_for_SRV(self, record):
        pass

    def _params_for_SSHFP(self, record):
        pass

    def _apply_Create(self, change):
        pass

    def _apply_Update(self, change):
        pass

    def _apply_Delete(self, change):
        pass

    def _apply(self, plan):
        desired = plan.desired
        changes = plan.changes
        self.log.debug('_apply: zone=%s, len(changes)=%d', desired.name,
                       len(changes))

        domain_name = desired.name[:-1]
        result = ClouDNSZone.get(domain_name=domain_name)
        if 404 == result.status_code:
            self.log.debug('_apply:   no matching zone, creating domain')
            ClouDNSZone.create(domain_name=domain_name, zone_type='master')

        for change in changes:
            class_name = change.__class__.__name__
            getattr(self, f'_apply_{class_name}')(change)

        # Clear out the cache if any
        self._zone_records.pop(desired.name, None)
    --- TODO ---
    '''
