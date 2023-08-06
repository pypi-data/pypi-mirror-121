# Twitcaspy
# Copyright 2021 Alma-field
# See LICENSE for details.

from .model import Model

class App(Model):
    """Application Object

    Attributes
    ----------
    client_id: :class:`str`
        | Application client ID
    name: :class:`str`
        | Application name
    owner_user_id: :class:`str`
        | Application developer user ID

    References
    ----------
    https://apiv2-doc.twitcasting.tv/#app-object
    """

    @classmethod
    def parse(cls, api, json):
        app = cls(api)
        setattr(app, '_json', json)
        for k, v in json.items():
            setattr(app, k, v)
        return app
