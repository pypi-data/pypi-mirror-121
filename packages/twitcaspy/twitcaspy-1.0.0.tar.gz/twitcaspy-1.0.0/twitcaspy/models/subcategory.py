# Twitcaspy
# Copyright 2021 Alma-field
# See LICENSE for details.

from .model import Model

class SubCategory(Model):
    """SubCategory Object

    Attributes
    ----------
    id: :class:`str`
        | SubCategory ID
    name: :class:`str`
        | SubCategory name
    count: :class:`int`
        | Number of subcategory streams

    References
    ----------
    https://apiv2-doc.twitcasting.tv/#sub-category-object
    """

    @classmethod
    def parse(cls, api, json):
        subcategory = cls(api)
        setattr(subcategory, '_json', json)
        for k, v in json.items():
            setattr(subcategory, k, v)
        return subcategory
