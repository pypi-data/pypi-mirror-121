# Twitcaspy
# Copyright 2021 Alma-field
# See LICENSE for details.

class Model:
    """Model Base Class

    Attributes
    ----------
    _api : :class:`~twitcaspy.api.API`
    """

    def __init__(self, api=None):
        self._api = api

    def __getstate__(self):
        # pickle
        pickle = dict(self.__dict__)
        try:
            del pickle['_api']  # do not pickle the API reference
        except KeyError:
            pass
        return pickle

    @classmethod
    def parse(cls, api, json):
        """Parse a JSON Model into a model instance."""
        raise NotImplementedError

    def __repr__(self):
        state = [f'{k}={v!r}' for (k, v) in vars(self).items()]
        return f'{self.__class__.__name__}({", ".join(state)})'
