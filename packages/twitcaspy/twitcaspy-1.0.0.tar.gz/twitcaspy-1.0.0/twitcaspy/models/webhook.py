# Twitcaspy
# Copyright 2021 Alma-field
# See LICENSE for details.

from .model import Model

class WebHook(Model):
    """WebHook Object

    Attributes
    ----------
    user_id: :class:`str`
        | User ID
    event: :class:`str`
        | Event type to hook
        | `event` must be one of the following:
        | 'livestart' : Live start
        | 'liveend' : Live end

    References
    ----------
    https://apiv2-doc.twitcasting.tv/#webhook-object
    """

    @classmethod
    def parse(cls, api, json):
        webhook = cls(api)
        setattr(webhook, '_json', json)
        for k, v in json.items():
            setattr(webhook, k, v)
        return webhook
