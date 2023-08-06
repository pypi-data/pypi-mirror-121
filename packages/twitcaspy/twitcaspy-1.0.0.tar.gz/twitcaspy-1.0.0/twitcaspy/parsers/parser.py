# Twitcaspy
# Copyright 2021 Alma-field
# See LICENSE for details.

class Parser:
    def parse(self, payload, *args, **kwargs):
        """
        Parse the response payload and return the result.
        Returns a tuple that contains the result data
        (or None if not present).
        """
        raise NotImplementedError
