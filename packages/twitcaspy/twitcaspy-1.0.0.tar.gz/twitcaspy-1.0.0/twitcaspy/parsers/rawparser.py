# Twitcaspy
# Copyright 2021 Alma-field
# See LICENSE for details.

from .parser import Parser

class RawParser(Parser):
    def __init__(self):
        pass

    @classmethod
    def parse(cls, payload, *args, **kwargs):
        return payload
