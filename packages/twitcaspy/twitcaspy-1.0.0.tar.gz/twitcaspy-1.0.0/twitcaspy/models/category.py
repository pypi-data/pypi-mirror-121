# Twitcaspy
# Copyright 2021 Alma-field
# See LICENSE for details.

from .model import Model

from .subcategory import SubCategory

class Category(Model):
    """Category Object

    Attributes
    ----------
    id: :class:`str`
        | Category ID
    name: :class:`str`
        | Category name
    sub_categories: :class:`list` of :class:`~twitcaspy.models.SubCategory`

    References
    ----------
    https://apiv2-doc.twitcasting.tv/#category-object
    """

    @classmethod
    def parse(cls, api, json):
        category = cls(api)
        setattr(category, '_json', json)
        for k, v in json.items():
            if k == 'sub_categories':
                sub_categories = []
                for subcategory in v:
                    sub_categories.append(SubCategory.parse(api, subcategory))
                setattr(category, k, sub_categories)
            else:
                setattr(category, k, v)
        return category
