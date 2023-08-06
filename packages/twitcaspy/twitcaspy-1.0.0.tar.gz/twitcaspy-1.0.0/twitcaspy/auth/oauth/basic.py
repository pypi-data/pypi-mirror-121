# Twitcaspy
# Copyright 2021 Alma-field
# See LICENSE for details.

from base64 import b64encode

from requests.auth import AuthBase

class OAuth2Basic(AuthBase):
    """Basic Authentication

    Parameters
    ----------
    client_id: :class:`str`
        |client_id|
    client_secret: :class:`str`
        |client_secret|

    Raises
    ------
    TypeError
        If the given client id and/or secret is not a string instance
    """
    def __init__(self, client_id, client_secret):
        if not isinstance(client_id, str):
            raise TypeError("ClientID must be string, not "
                            + type(client_id).__name__)
        if not isinstance(client_secret, str):
            raise TypeError("Client secret must be string, not "
                            + type(client_secret).__name__)

        self.token = b64encode(f'{client_id}:{client_secret}'.encode('utf-8'))
        self.token = self.token.decode('utf-8')

    def __call__(self, request):
        request.headers['Authorization'] = 'Basic ' + self.token
        return request
