# Twitcaspy
# Copyright 2021 Alma-field
# See LICENSE for details.

from .model import Model

class Gift(Model):
    """Gift Object

    Attributes
    ----------
    id: :class:`str`
        | Item transmission ID
    message: :class:`str`
        | Message body when sending an item.
    item_image: :class:`str`
        | Item image URL
    item_sub_image: :class:`str` or :class:`None`
        | If there is an image selected when sending the item,
          the URL of the image.
    item_id: :class:`str`
        | Item ID
    item_mp: :class:`str`
        | Item MP
    item_name: :class:`str`
        | Item name
    user_image: :class:`str`
        | URL of user icon
    user_screen_id: :class:`str`
        | User's screen_id at the time the item was submitted.
    user_screen_name: :class:`str`
        | Human readable screen_id
    user_name: :class:`str`
        | Human readable user name

    References
    ----------
    https://apiv2-doc.twitcasting.tv/#gift-object
    """

    @classmethod
    def parse(cls, api, json):
        gift = cls(api)
        setattr(gift, '_json', json)
        for k, v in json.items():
            setattr(gift, k, v)
        return gift
