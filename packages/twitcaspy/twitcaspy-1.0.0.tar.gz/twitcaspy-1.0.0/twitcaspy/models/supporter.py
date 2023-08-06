# Twitcaspy
# Copyright 2021 Alma-field
# See LICENSE for details.

from .model import Model

class Supporter(Model):
    """Supporter Object

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
        | Returns a fixed value of 0.
        | This parameter is deprecated.
    supporting_count(deprecated): :class:`int`
        | Number supported user by the user.
        | Returns a fixed value of 0.
        | This parameter is deprecated.
    point: :class:`int`
        | Item score
    total_point: :class:`int`
        | Cumulative score
    created(deprecated): :class:`int`
        | Date and time when this account was created.
        | Returns a fixed value of 0.
        | This parameter is deprecated.

    References
    ----------
    https://apiv2-doc.twitcasting.tv/#supporteruser-object
    """

    @classmethod
    def parse(cls, api, json):
        supporter = cls(api)
        setattr(supporter, '_json', json)
        for k, v in json.items():
            setattr(supporter, k, v)
        return supporter
