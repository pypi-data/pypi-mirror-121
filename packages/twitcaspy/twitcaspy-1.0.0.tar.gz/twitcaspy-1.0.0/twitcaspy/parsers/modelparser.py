# Twitcaspy
# Copyright 2021 Alma-field
# See LICENSE for details.

from ..errors import TwitcaspyException

from ..models.result import Result

from ..models.latelimit import LateLimit

from ..models.factory import ModelFactory

from .parser import Parser

class ModelParser(Parser):
    def __init__(self, model_factory=None):
        self.model_factory = model_factory or ModelFactory

    def parse(self, payload, *, api=None, payload_type=None):
        if payload_type is None:
            return None

        if isinstance(payload_type, str):
            _payload_type = {payload_type: [payload_type, False]}
        elif isinstance(payload_type, list):
            _payload_type = {_item: [_item, False] for _item in payload_type}
        elif isinstance(payload_type, dict):
            _payload_type = payload_type
        else:
            raise TypeError("payload_type must be (str, list, dict). not "
                            + type(payload_type).__name__)
        for _item in _payload_type.values():
            _key = _item[0]
            if not hasattr(self.model_factory, _key):
                raise TwitcaspyException(
                    f'No model for this payload type: {_key}'
                )

        if hasattr(payload, 'json'):
            json = payload.json()
        else:
            json = payload

        result = Result(api)
        setattr(result, '_json', json)
        try:
            for _name, _item in _payload_type.items():
                _type, _list = _item
                model = getattr(self.model_factory, _type)
                if _name == 'raw_data':
                    parse_data = json
                    _name = _type
                else:
                    parse_data = json[_name]
                if _list:
                    data = [model.parse(api, _json) for _json in parse_data]
                else:
                    data = model.parse(api, parse_data)
                setattr(result, _name, data)
        except KeyError:
            raise TwitcaspyException(
                f"Unable to parse response payload: {json}"
            )

        if not hasattr(payload, 'headers'):
            pass
        elif 'X-RateLimit-Limit' in payload.headers:
            setattr(result, 'late_limit', LateLimit.parse(payload.headers))
        else:
            setattr(result, 'late_limit', LateLimit())

        return result
