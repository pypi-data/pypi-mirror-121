# Copyright (c) Qotto, 2021
import json
from typing import Optional

import avro.schema
from avro.schema import RecordSchema

from eventy.serialization import SerializationError

_common_fields = [
    {'name': 'type', 'type': 'string'},
    {'name': 'protocol_version', 'type': 'string'},
    {'name': 'schema', 'type': 'string'},
    {'name': 'version', 'type': 'string'},
    {'name': 'source', 'type': 'string'},
    {'name': 'uuid', 'type': 'string'},
    {'name': 'correlation_id', 'type': 'string'},
    {'name': 'partition_key', 'type': ['string', 'null']},
    {'name': 'date_timestamp', 'type': 'long'},
    {'name': 'date_iso8601', 'type': 'string'},
]

_fields_map = {
    'EVENT': _common_fields,
    'REQUEST': _common_fields,
    'RESPONSE': _common_fields + [
        {'name': 'destination', 'type': 'string'},
        {'name': 'request_uuid', 'type': 'string'},
        {'name': 'ok', 'type': 'boolean'},
        {'name': 'error_code', 'type': ['null', 'int']},
        {'name': 'error_message', 'type': ['null', 'string']},
    ],
}


def gen_schema(
    record_type: str,
    record_schema_urn: str,
    data_fields: Optional[list]
) -> RecordSchema:
    common_fields = _fields_map.get(record_type.upper())
    if not common_fields:
        raise SerializationError(f"Cannot find common fields for {record_type}.")
    schema_urn_split = record_schema_urn.split(':')
    namespace = '.'.join(schema_urn_split[0:-1])
    name = schema_urn_split[-1]

    schema_dict = {
        'name': name,
        'namespace': namespace,
        'type': 'record',
        'fields': common_fields + [
            {
                'name': 'context', 'type':
                {
                    'type': 'map', 'values':
                    {
                        'type': 'map',
                        'values': ['string', 'double', 'float', 'long', 'int', 'boolean', 'null']
                    }
                }
            },
            {
                'name': 'data', 'type':
                {
                    'type': 'record', 'name': f'{name}_data', 'namespace': namespace, 'fields':
                    data_fields or []
                }
            }
        ]
    }
    return avro.schema.parse(json.dumps(schema_dict))
