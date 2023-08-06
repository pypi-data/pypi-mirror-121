# Copyright (c) Qotto, 2021

import json
from typing import Union

from eventy.record import Record, Event, Request, Response
from eventy.serialization import RecordSerializer, SerializationError
from eventy.serialization.common import create_dict_from_record, create_record_from_dict


class JsonSerializer(RecordSerializer):

    def encode(self, record: Record) -> bytes:
        record_dict = create_dict_from_record(record)
        return bytes(json.dumps(record_dict), encoding='utf-8')

    def decode(self, encoded: bytes) -> Union[Event, Request, Response]:
        try:
            record_dict = json.loads(encoded)
            return create_record_from_dict(record_dict)
        except Exception as e:
            raise SerializationError from e
