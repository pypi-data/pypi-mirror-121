# Twitcaspy
# Copyright 2021 Alma-field
# See LICENSE for details.

from ..utils import fromtimestamp

from .model import Model

class LateLimit:
    """Late Limit Object

    Attributes
    ----------
    limit: :class:`int`
        | Maximum number of API executions
    remaining: :class:`int`
        | API remaining executable times
    reset: :class:`int`
        | Unix Timestamp at the time when the remaining API execution count is reset
    reset_time: :class:`datetime.datetime`
        | Converted reset to :class:`datetime.datetime` type

    References
    ----------
    https://apiv2-doc.twitcasting.tv/#response-headers
    """
    def __init__(self):
        self.limit = -1
        self.remaining = -1
        self.reset = None
        self.reset_time = None

    @classmethod
    def parse(cls, headers):
        latelimit = cls()
        latelimit.limit = int(headers['X-RateLimit-Limit'])
        latelimit.remaining = int(headers['X-RateLimit-Remaining'])
        latelimit.reset = int(headers['X-RateLimit-Reset'])
        latelimit.reset_time = fromtimestamp(latelimit.reset)
        return latelimit
