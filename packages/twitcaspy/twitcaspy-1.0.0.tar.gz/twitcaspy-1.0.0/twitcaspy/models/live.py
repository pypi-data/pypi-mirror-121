# Twitcaspy
# Copyright 2021 Alma-field
# See LICENSE for details.

from .model import Model

from .movie import Movie

from .user import User

class Live(Model):
    """Live Object

    Attributes
    ----------
    movie: :class:`~twitcaspy.models.Movie`
    broadcaster: :class:`~twitcaspy.models.User`
    tags: :class:`list`
    """

    @classmethod
    def parse(cls, api, json):
        live = cls(api)
        setattr(live, '_json', json)
        for k, v in json.items():
            if k == 'movie':
                setattr(live, k, Movie.parse(api, v))
            elif k == 'broadcaster':
                setattr(live, k, User.parse(api, v))
            else:
                setattr(live, k, v)
        return live
