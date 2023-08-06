# Twitcaspy
# Copyright 2021 Alma-field
# See LICENSE for details.

class Raw:
    """Raw Object

    | The data will be returned as it is.
    | This class does not instantiate.
    """

    @classmethod
    def parse(cls, api, json):
        return json
