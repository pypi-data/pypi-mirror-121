# Copyright (c) Qotto, 2021
import json
import os
from datetime import datetime
from io import BytesIO
from typing import Union, Dict, Any, Optional, Iterator, Iterable

import avro.schema
import yaml
from avro.datafile import DataFileWriter, DataFileReader
from avro.io import DatumWriter, AvroTypeException, DatumReader
from avro.schema import RecordSchema

from eventy.record import Record, Event, Request, Response
from eventy.serialization import RecordSerializer

__all__ = [
    'AvroSerializer',
    'gen_avro_schema',
]

from eventy.serialization.errors import SerializationError, UnknownRecordTypeError


class AvroSerializer(RecordSerializer):

    def __init__(
        self,
        avro_schemas: Iterable[RecordSchema] = None
    ):
        self.avro_schemas = {}
        if avro_schemas is not None:
            for avro_schema in avro_schemas:
                schema_urn = _namespace_name_to_schema_urn(avro_schema.namespace, avro_schema.name)
                self.avro_schemas[schema_urn] = avro_schema

    @classmethod
    def from_schemas_folder(cls, schemas_folder: str) -> 'AvroSerializer':
        return AvroSerializer(_load_schema_files(schemas_folder, schemas_ext='.evsc.yaml', recursive=True))

    def encode(self, record: Record) -> bytes:
        record_schema_urn = record.schema
        avro_schema = self.avro_schemas.get(record_schema_urn)
        if not avro_schema:
            raise SerializationError(f"Could not find avro schema for record {record_schema_urn}.")

        record_dict: Dict[str, Any] = {
            'type': record.type,
            'protocol_version': record.protocol_version,
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

        try:
            bytes_io = BytesIO()
            with DataFileWriter(bytes_io, DatumWriter(), avro_schema) as writer:
                writer.append(record_dict)
                writer.flush()
                output_bytes = bytes_io.getvalue()
            return output_bytes
        except AvroTypeException as avro_exception:
            raise SerializationError(avro_exception)

    def decode(self, encoded: bytes) -> Union[Event, Request, Response]:
        try:
            reader = DataFileReader(BytesIO(encoded), DatumReader())

            schema = json.loads(reader.meta.get('avro.schema').decode('utf-8'))
            name = schema['name']
            namespace = schema['namespace']

            record_dict = next(reader)

            record_type = record_dict.pop('type')
            date = datetime.fromisoformat(record_dict.pop('date_iso8601'))
            record_dict.pop('date_timestamp')

            record_dict['date'] = date
            record_dict['schema'] = _namespace_name_to_schema_urn(namespace, name)

            if record_type == 'EVENT':
                return Event(**record_dict)
            elif record_type == 'REQUEST':
                return Request(**record_dict)
            elif record_type == 'RESPONSE':
                return Response(**record_dict)
            else:
                raise UnknownRecordTypeError(record_type)
        except Exception as e:
            raise SerializationError from e


def gen_avro_schema(
    protocol_version: str,
    schema: str,
    type: str,
    doc: Optional[str] = None,
    data_fields: Optional[list] = None,
) -> RecordSchema:
    name = schema.split(':')[-1]
    namespace = '.'.join(schema.split(':')[1:-1])
    if type not in ['EVENT', 'REQUEST', 'RESPONSE']:
        raise ValueError(f'Cannot parse eventy schema {schema}, type must be EVENT, REQUEST, or RESPONSE.')

    fields = [
        {
            'name': 'type',
            'type': {
                'name': 'RecordType',
                'type': 'enum',
                'symbols': [type]
            },
            'doc': 'Type of of record: one of EVENT, REQUEST or RESPONSE',
        },
        {
            'name': 'protocol_version',
            'type': 'string',
            'doc': 'Version of the Eventy protocol used for encoding this message (semver format: X.Y.Z)',
        },
        {
            'name': 'version',
            'type': 'string',
            'doc': 'Version of the schema used for encoding this message (semver format: X.Y.Z)',
        },
        {
            'name': 'source', 'type': 'string',
            'doc': 'Source of the record (URN of the producing service)',
        },
        {
            'name': 'uuid', 'type': 'string', 'logicalType': 'uuid',
            'doc': 'UUID for this record',
        },
        {
            'name': 'correlation_id', 'type': 'string',
            'doc': 'Identifier propagated across the system and to link associated records together',
        },
        {
            'name': 'partition_key', 'type': ['string', 'null'],
            'doc': 'A string determining to which partition your record will be assigned',
        },
        {
            'name': 'date_timestamp', 'type': 'long', 'logicalType': 'timestamp-millis',
            'doc': 'UNIX timestamp in milliseconds',
        },
        {
            'name': 'date_iso8601', 'type': 'string',
            'doc': 'ISO 8601 date with timezone',
        },
    ]
    if type == 'RESPONSE':
        fields += [
            {
                'name': 'destination', 'type': 'string',
                'doc': 'URN of the destination service',
            },
            {
                'name': 'request_uuid', 'type': 'string',
                'doc': 'UUID of the associated request',
            },
            {
                'name': 'ok', 'type': 'boolean',
                'doc': 'Status: True if there was no error, false otherwise',
            },
            {
                'name': 'error_code', 'type': ['null', 'int'],
                'doc': 'Numeric code for the error, if ok is False, null otherwise',
            },
            {
                'name': 'error_message', 'type': ['null', 'string'],
                'doc': 'Description for the error, if ok is False, null otherwise',
            },
        ]
    fields += [
        {
            'name': 'context', 'type':
            {
                'type': 'map', 'values':
                {
                    'type': 'map',
                    'values': ['string', 'double', 'float', 'long', 'int', 'boolean', 'null']
                }
            },
            'doc': 'Context data, always propagated'
        },
        {
            'name': 'data', 'type':
            {
                'type': 'record', 'name': f'{name}_data', 'namespace': namespace, 'fields':
                data_fields or []
            },
            'doc': 'Record payload',
        }
    ]
    schema_dict = {
        'name': name,
        'namespace': namespace,
        'doc': doc or f'{name} {type} Record',
        'type': 'record',
        'fields': fields,
    }
    return avro.schema.parse(json.dumps(schema_dict))


def _load_schema_files(
    schemas_folder: str,
    schemas_ext: str,
    recursive: bool,
) -> Iterator[RecordSchema]:
    with os.scandir(schemas_folder) as entries:
        entry: os.DirEntry
        for entry in entries:

            # load in sub folder if recursive option set
            if entry.is_dir():
                if recursive:
                    yield from _load_schema_files(entry.path, schemas_ext, recursive)
                else:
                    continue

            # ignores everything that is not a file
            if not entry.is_file():
                continue  # pragma: nocover

            # ignores hidden files
            if entry.name.startswith("."):
                continue  # pragma: nocover

            # ignores everything files with wrong extension
            if not entry.name.endswith(schemas_ext):
                continue  # pragma: nocover

            with open(entry.path) as avro_yml:
                yaml_data = yaml.load(avro_yml.read(), Loader=yaml.SafeLoader)
                avro_schema = gen_avro_schema(**yaml_data)
                yield avro_schema


def _schema_urn_to_avro_namespace(schema_urn: str) -> str:
    if schema_urn.startswith('urn:'):
        schema_urn = schema_urn[4:]
    return '.'.join(schema_urn.split(':')[0:-1])


def _schema_urn_to_avro_name(schema_urn: str) -> str:
    return schema_urn.split(':')[-1]


def _namespace_name_to_schema_urn(namespace: str, name: str) -> str:
    return f'urn:{namespace.replace(".", ":")}:{name}'
