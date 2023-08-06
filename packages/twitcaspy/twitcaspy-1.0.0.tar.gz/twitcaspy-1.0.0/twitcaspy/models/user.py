# Twitcaspy
# Copyright 2021 Alma-field
# See LICENSE for details.

from .model import Model

class User(Model):
    """User Object

    Attributes
    ----------
    id: :class:`str`
        | |id|
    screen_id: :class:`str`
        | |screen_id|
        | **Note**: screen_id is subject to change by the user.
    name: :class:`str`
        | Human readable user name
    image: :class:`str`
        | URL of user icon
    profile: :class:`str`
        | Profile text
    level: :class:`int`
        | User level
    last_movie_id: :class:`str` or :class:`None`
        | The last live ID by the user
    is_live: :class:`bool`
        | Whether it is currently live streamed
    supporter_count(deprecated): :class:`int`
        | Number of user supporters.
        | `2018-09-03 update <https://github.com/twitcasting/PublicApiV2/blob/master/CHANGELOG.md#2018-09-03>`_
        | Returns a fixed value of 0.
        | This parameter is deprecated.
    supporting_count(deprecated): :class:`int`
        | Number supported user by the user.
        | `2018-09-03 update <https://github.com/twitcasting/PublicApiV2/blob/master/CHANGELOG.md#2018-09-03>`_
        | Returns a fixed value of 0.
        | This parameter is deprecated.
    created(deprecated): :class:`int`
        | Date and time when this account was created.
        | `2018-08-03 update <https://github.com/twitcasting/PublicApiV2/blob/master/CHANGELOG.md#2018-08-03>`_
        | Returns a fixed value of 0.
        | This parameter is deprecated.

    References
    ----------
    https://apiv2-doc.twitcasting.tv/#user-object
    """

    @classmethod
    def parse(cls, api, json):
        user = cls(api)
        setattr(user, '_json', json)
        for k, v in json.items():
            setattr(user, k, v)
        return user
