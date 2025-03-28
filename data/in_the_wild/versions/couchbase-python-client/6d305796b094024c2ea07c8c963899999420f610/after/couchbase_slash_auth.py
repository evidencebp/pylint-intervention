from enum import IntEnum
from typing import Optional


class Authenticator(dict):
    pass


class PasswordAuthenticator(Authenticator):
    def __init__(self,
                 username,          # type: str
                 password,          # type: str
                 cert_path=None     # type: Optional[str]
                 ):
        """
        Password authentication mechanism.

        Args:
            username (str): Username to use for authentication.
            password (str): Password to use for authentication.
            cert_path (str, optional): Path of the certificate trust store. Defaults to None.
        """
        self._username = username
        self._password = password
        self._cert_path = cert_path

        super().__init__(**self.as_dict())

    def valid_keys(self):
        return ['username', 'password', 'cert_path']

    def as_dict(self):
        d = {
            'username': self._username,
            'password': self._password
        }
        if self._cert_path is not None:
            # couchbase++ wants this to be the trust_certificate
            d['trust_store_path'] = self._cert_path

        return d


class CertificateAuthenticator(Authenticator):
    def __init__(self,
                 cert_path=None,            # type: str
                 key_path=None,             # type: str
                 trust_store_path=None     # type: Optional[str]
                 ):
        """
        Certificate authentication mechanism.

        Args:
            cert_path (str): Path to the client certificate. Defaults to None.
            key_path (str): Path to the client key. Defaults to None.
            trust_store_path (str, optional): Path of the certificate trust store. Defaults to None.
        """

        self._trust_store_path = trust_store_path
        self._cert_path = cert_path
        self._key_path = key_path

        super().__init__(**self.as_dict())

    def valid_keys(self):
        return ['cert_path', 'key_path', 'trust_store_path']

    def as_dict(self):
        d = {
            'cert_path': self._cert_path,
            'key_path': self._key_path
        }
        if self._trust_store_path is not None:
            d['trust_store_path'] = self._trust_store_path

        return d


class AuthDomain(IntEnum):
    """
    The Authentication domain for a user.
    Local: Users managed by Couchbase Server.
    External: Users managed by an external resource, eg LDAP.
    """
    Local = 0
    External = 1

    @classmethod
    def to_str(cls, value):
        if value == cls.External:
            return "external"
        else:
            return "local"

    @classmethod
    def from_str(cls, value):
        if value == "external":
            return cls.External
        else:
            return cls.Local
