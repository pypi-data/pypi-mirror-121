#
# Copyright 2019 Venafi, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from __future__ import (absolute_import, division, generators, unicode_literals, print_function, nested_scopes,
                        with_statement)

import logging as log
import re
import time

import requests

from .common import MIME_JSON, CertField, ZoneConfig, Policy, KeyType
from .connection_tpp_abstract import AbstractTPPConnection, URLS
from .errors import (ServerUnexptedBehavior, ClientBadData, AuthenticationError)
from .http import HTTPStatus

TOKEN_HEADER_NAME = "x-venafi-api-key"  # nosec


class TPPConnection(AbstractTPPConnection):
    def __init__(self, user, password, url, http_request_kwargs=None):
        """
        :param str user:
        :param str password:
        :param str url:
        :param dict[str,Any] http_request_kwargs:
        """
        self._base_url = url  # type: str
        self._user = user  # type: str
        self._password = password  # type: str
        self._token = None  # type: tuple
        if http_request_kwargs is None:
            http_request_kwargs = {"timeout": 180}
        elif "timeout" not in http_request_kwargs:
            http_request_kwargs["timeout"] = 180
        self._http_request_kwargs = http_request_kwargs or {}

    def __setattr__(self, key, value):
        if key == "_base_url":
            value = self._normalize_and_verify_base_url(value)
        self.__dict__[key] = value

    def __str__(self):
        return "[TPP] %s" % self._base_url

    def _get(self, url="", params=None):
        if not self._token or self._token[1] < time.time() + 1:
            self.auth()
            log.debug("Token is %s, timeout is %s" % (self._token[0], self._token[1]))

        r = requests.get(self._base_url + url, headers={TOKEN_HEADER_NAME: self._token[0], 'content-type':
                         MIME_JSON, 'cache-control': 'no-cache'}, params=params, **self._http_request_kwargs)
        return self.process_server_response(r)

    def _post(self, url, data=None):
        if not self._token or self._token[1] < time.time() + 1:
            self.auth()
            log.debug("Token is %s, timeout is %s" % (self._token[0], self._token[1]))

        if isinstance(data, dict):
            r = requests.post(self._base_url + url, headers={TOKEN_HEADER_NAME: self._token[0], 'content-type':
                              MIME_JSON, "cache-control": "no-cache"}, json=data, **self._http_request_kwargs)
        else:
            log.error("Unexpected client data type: %s for %s" % (type(data), url))
            raise ClientBadData
        return self.process_server_response(r)

    @staticmethod
    def _normalize_and_verify_base_url(u):
        if u.startswith("http://"):
            u = "https://" + u[7:]
        elif not u.startswith("https://"):
            u = "https://" + u
        if not u.endswith("/"):
            u += "/"
        if u.endswith(URLS.API_BASE_URL):
            u = u[:len(u)-7]  # "vedsdk/"
        if not re.match(r"^https://[a-z\d]+[-a-z\d.]+[a-z\d][:\d]*/$", u):
            raise ClientBadData
        return u

    def auth(self):
        data = {"Username": self._user, "Password": self._password}
        r = requests.post(self._base_url + URLS.AUTHORIZE, json=data,
                          headers={'content-type': MIME_JSON, "cache-control": "no-cache"},
                          **self._http_request_kwargs)

        status, user = self.process_server_response(r)
        if status == HTTPStatus.OK:
            valid_until = int(re.sub(r"\D", "", user["ValidUntil"]))
            self._token = user["APIKey"], valid_until
            return user
        else:
            log.error("Authentication status is not %s but %s. Exiting" % (HTTPStatus.OK, status[0]))
            raise AuthenticationError

    def revoke_cert(self, request):
        if not (request.id or request.thumbprint):
            raise ClientBadData
        d = {
            "Disable": request.disable
        }
        if request.reason:
            d["Reason"] = request.reason
        if request.id:
            d["CertificateDN"] = request.id
        elif request.thumbprint:
            d["Thumbprint"] = request.thumbprint
        else:
            raise ClientBadData
        if request.comments:
            d["Comments"] = request.comments
        status, data = self._post(URLS.CERTIFICATE_REVOKE, data=d)
        if status in (HTTPStatus.OK, HTTPStatus.ACCEPTED):
            return data

        raise ServerUnexptedBehavior

    @staticmethod
    def _parse_zone_config_to_policy(data):
        # todo: parse over values to regexps (dont forget tests!)
        p = data["Policy"]
        if p["KeyPair"]["KeyAlgorithm"]["Locked"]:
            if p["KeyPair"]["KeyAlgorithm"]["Value"] == "RSA":
                if p["KeyPair"]["KeySize"]["Locked"]:
                    key_types = [KeyType(KeyType.RSA, p["KeyPair"]["KeySize"]["Value"])]
                else:
                    key_types = [KeyType(KeyType.RSA, x) for x in KeyType.ALLOWED_SIZES]
            elif p["KeyPair"]["KeyAlgorithm"]["Value"] == "ECC":
                if p["KeyPair"]["EllipticCurve"]["Locked"]:
                    key_types = [KeyType(KeyType.ECDSA, p["KeyPair"]["EllipticCurve"]["Value"])]
                else:
                    key_types = [KeyType(KeyType.ECDSA, x) for x in KeyType.ALLOWED_CURVES]
            else:
                raise ServerUnexptedBehavior
        else:
            key_types = []
            if p["KeyPair"].get("KeySize", {}).get("Locked"):
                key_types += [KeyType(KeyType.RSA, p["KeyPair"]["KeySize"]["Value"])]
            else:
                key_types += [KeyType(KeyType.RSA, x) for x in KeyType.ALLOWED_SIZES]
            if p["KeyPair"].get("EllipticCurve", {}).get("Locked"):
                key_types += [KeyType(KeyType.ECDSA, p["KeyPair"]["EllipticCurve"]["Value"])]
            else:
                key_types += [KeyType(KeyType.ECDSA, x) for x in KeyType.ALLOWED_CURVES]
        return Policy(key_types=key_types)

    @staticmethod
    def _parse_zone_data_to_object(data):
        s = data["Policy"]["Subject"]
        ou = s['OrganizationalUnit'].get('Values')
        policy = TPPConnection._parse_zone_config_to_policy(data)
        if data["Policy"]["KeyPair"]["KeyAlgorithm"]["Value"] == "RSA":
            key_type = KeyType(KeyType.RSA, data["Policy"]["KeyPair"]["KeySize"]["Value"])
        elif data["Policy"]["KeyPair"]["KeyAlgorithm"]["Value"] == "ECC":
            key_type = KeyType(KeyType.ECDSA, data["Policy"]["KeyPair"]["EllipticCurve"]["Value"])
        else:
            key_type = None
        z = ZoneConfig(
            organization=CertField(s['Organization']['Value'], locked=s['Organization']['Locked']),
            organizational_unit=CertField(ou, locked=s['OrganizationalUnit']['Locked']),
            country=CertField(s['Country']['Value'], locked=s['Country']['Locked']),
            province=CertField(s['State']['Value'], locked=s['State']['Locked']),
            locality=CertField(s['City']['Value'], locked=s['City']['Locked']),
            policy=policy,
            key_type=key_type,
        )
        return z

    def read_zone_conf(self, tag):
        status, data = self._post(URLS.ZONE_CONFIG, {"PolicyDN": self._normalize_zone(tag)})
        if status != HTTPStatus.OK:
            raise ServerUnexptedBehavior("Server returns %d status on reading zone configuration." % status)
        return self._parse_zone_data_to_object(data)

    def import_cert(self, request):
        raise NotImplementedError

    def _read_config_dn(self, dn, attribute_name):
        status, data = self._post(URLS.CONFIG_READ_DN, {
            "ObjectDN": dn,
            "AttributeName": attribute_name,
        })
        if status != HTTPStatus.OK:
            raise ServerUnexptedBehavior("")
        return data

    def _get_certificate_details(self, cert_guid):
        status, data = self._get(URLS.CERTIFICATE_SEARCH + cert_guid)
        if status != HTTPStatus.OK:
            raise ServerUnexptedBehavior("")
        return data
