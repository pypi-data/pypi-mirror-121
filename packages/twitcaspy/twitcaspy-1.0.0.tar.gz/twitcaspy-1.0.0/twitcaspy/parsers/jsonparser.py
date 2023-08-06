# Twitcaspy
# Copyright 2021 Alma-field
# See LICENSE for details.

from .parser import Parser

class JsonParser(Parser):
    def __init__(self):
        pass

    @classmethod
    def parse(self, payload, *args, **kwargs):
        return payload.json()
