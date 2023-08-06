# Twitcaspy
# Copyright 2021 Alma-field
# See LICENSE for details.

"""
Twitcaspy : Twitcasting API library
"""
__version__ = '1.0.0'
__author__ = 'Alma-field'
__license__ = 'MIT'

from twitcaspy.api import API
from twitcaspy.auth import (
    GrantAuthHandler, ImplicitAuthHandler, AppAuthHandler
)
from twitcaspy.errors import (
    BadRequest, Forbidden, HTTPException, NotFound, TooManyRequests,
    TwitcaspyException, TwitcastingServerError, Unauthorized
)
from twitcaspy.models import (
    App, Category, Comment, ModelFactory, Gift, LateLimit,
    Live, Movie, Raw, SubCategory, Supporter, User, WebHook
)

# Global, unauthenticated instance of API
api = API()
