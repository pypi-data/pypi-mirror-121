# Twitcaspy
# Copyright 2021 Alma-field
# See LICENSE for details.

from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import MobileApplicationClient

from ..errors import TwitcaspyException

from .auth import AuthHandler

from .oauth import OAuth2Bearer

class ImplicitAuthHandler(AuthHandler):
    """
    Implicit Code Grant handler

    Parameters
    ----------
    client_id: :class:`str`
        |client_id|
    client_secret: :class:`str`
        |client_secret|
    callback: :class:`str`
        |callback|
    state: :class:`str`
        |csrf_token|

    References
    ----------
    https://apiv2-doc.twitcasting.tv/#implicit
    """

    def __init__(self, client_id, client_secret, callback=None, *, state=None):
        super().__init__(client_id, client_secret)
        self.callback = callback
        self.state = state
        self.auth = None

        self.oauth = OAuth2Session(
            client=MobileApplicationClient(client_id=client_id),
            #redirect_uri=callback,
            state=state
        )

    def get_authorization_url(self):
        """Get the authorization URL to redirect the user"""
        try:
            url = self._get_oauth_url('authorize')
            authorization_url, self.state = self.oauth.authorization_url(url)
            return authorization_url
        except Exception as e:
            raise TwitcaspyException(e)

    def fetch_token(self, authorization_response):
        try:
            self.oauth.token_from_fragment(authorization_response)
            self.auth = OAuth2Bearer(self.oauth.token['access_token'])
        except Exception as e:
            raise TwitcaspyException(e)
