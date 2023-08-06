# Twitcaspy
# Copyright 2021 Alma-field
# See LICENSE for details.

from .app import App

from .category import Category

from .comment import Comment

from .gift import Gift

from .live import Live

from .movie import Movie

from .raw import Raw

from .subcategory import SubCategory

from .supporter import Supporter

from .user import User

from .webhook import WebHook

class ModelFactory:
    """
    | Used by parsers for creating instances of models.
    | You may subclass this factory to add your own extended models.
    """

    app = App
    category = Category
    comment = Comment
    gift = Gift
    live = Live
    movie = Movie
    raw = Raw
    subcategory = SubCategory
    supporter = Supporter
    user = User
    webhook = WebHook
