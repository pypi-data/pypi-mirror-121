# Copyright (c) Qotto, 2021
from datetime import datetime
from typing import Any, Dict, Union

from eventy.record import Record, Response, Request, Event
from eventy.serialization import UnknownRecordTypeError


def create_dict_from_record(record: Record) -> Dict:
    record_dict: dict[str, Any] = {
        'type': record.type,
        'protocol_version': record.protocol_version,
        'schema': record.schema,
        'version': record.version,
        'source': record.source,
        'uuid': record.uuid,
        'correlation_id': record.correlation_id,
        'partition_key': record.partition_key,
        'date_timestamp': int(record.date.timestamp() * 1000),
        'date_iso8601': record.date.isoformat(),
    }
    if isinstance(record, Response):
        record_dict.update(
            {
                'destination': record.destination,
                'request_uuid': record.request_uuid,
                'ok': record.ok,
                'error_code': record.error_code,
                'error_message': record.error_message,
            }
        )
    record_dict.update(
        {
            'context': record.context,
            'data': record.data
        }
    )
    return record_dict


def create_record_from_dict(record_dict: Dict) -> Union[Event, Request, Response]:
    record_type = record_dict.pop('type')
    date = datetime.fromisoformat(record_dict.pop('date_iso8601'))
    record_dict.pop('date_timestamp')
    record_dict['date'] = date
    record: Union[Event, Request, Response]
    if record_type == 'EVENT':
        record = Event(**record_dict)
    elif record_type == 'REQUEST':
        record = Request(**record_dict)
    elif record_type == 'RESPONSE':
        record = Response(**record_dict)
    else:
        raise UnknownRecordTypeError(record_type)
    return record
