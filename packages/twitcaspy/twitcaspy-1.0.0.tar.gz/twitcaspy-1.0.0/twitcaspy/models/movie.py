# Twitcaspy
# Copyright 2021 Alma-field
# See LICENSE for details.

from ..utils import fromtimestamp

from .model import Model

class Movie(Model):
    """Movie Object

    Attributes
    ----------
    id: :class:`str`
        | |movie_id|
    user_id: :class:`str`
        | |id|
    title: :class:`str`
        | Live title
    subtitle: :class:`str`
        | Live subtitle (telop)
    last_owner_comment: :class:`str` or :class:`None`
        | Live streamer's latest comment text
    category: :class:`str` or :class:`None`
        | category id
    link: :class:`str`
        | Link URL to live (or recording)
    is_live: :class:`bool`
        | Whether live streaming now
    is_recorded: :class:`bool`
        | Whether the recording is public
    comment_count: :class:`int`
        | Total number of comments
    large_thumbnail: :class:`str`
        | URL of thumbnail image (large)
    small_thumbnail: :class:`str`
        | URL of thumbnail image (small)
    country: :class:`str`
        | stream area (country code)
    duration: :class:`int`
        | stream time (seconds)
    created: :class:`datetime.datetime`
        | Converted Unix time stamp of stream start date and time to :class:`datetime.datetime` type
    is_collabo: :class:`bool`
        | Whether it is a collaboration stream
    is_protected: :class:`bool`
        | Whether to need the secret word
    max_view_count: :class:`int`
        | Maximum number of simultaneous viewers
        | (0 if streaming now.)
    current_view_count: :class:`int`
        | Current number of simultaneous viewers
        | (0 if not streaming now.)
    total_view_count: :class:`int`
        | Total number of viewers
    hls_url: :class:`str` or :class:`None`
        | URL for HTTP Live Streaming playback
        | `2019-04-17 update <https://github.com/twitcasting/PublicApiV2/blob/master/CHANGELOG.md#2019-04-17>`_
        | Changed the URL of the hls_url parameter from `http` to `https` |google_translate_ja_en|

    References
    ----------
    https://apiv2-doc.twitcasting.tv/#movie-object
    """

    @classmethod
    def parse(cls, api, json):
        movie = cls(api)
        setattr(movie, '_json', json)
        for k, v in json.items():
            if k == 'created':
                setattr(movie, k, fromtimestamp(v))
            else:
                setattr(movie, k, v)
        return movie
