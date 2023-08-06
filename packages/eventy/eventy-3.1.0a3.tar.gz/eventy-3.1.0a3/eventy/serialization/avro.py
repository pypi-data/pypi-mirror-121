# Copyright (c) Qotto, 2021
import json
import os
from datetime import datetime
from io import BytesIO
from typing import Union, Dict, Any, Optional, Iterator

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
        avro_schemas: Optional[Dict[str, RecordSchema]] = None
    ):
        if avro_schemas is None:
            self.avro_schemas = {}
        else:
            self.avro_schemas = avro_schemas

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
            record_dict['schema'] = namespace_name_to_schema(namespace, name)

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


def schema_to_avro_namespace(schema_urn: str) -> str:
    """
    Extract dot separated namespace from record schema.

    :param schema_urn: Record schema in URN format "urn:domain:service:event:EventName"
    :return: Namespace in Avro format "domain.service.event"
    """
    if schema_urn.startswith('urn:'):
        schema_urn = schema_urn[4:]
    return '.'.join(schema_urn.split(':')[0:-1])


def schema_to_avro_name(schema_urn: str) -> str:
    """
    Extract name from record schema.

    :param schema_urn: Record schema in URN format "urn:domain:service:event:EventName"
    :return: Name in Avro format "EventName"
    """
    return schema_urn.split(':')[-1]


def namespace_name_to_schema(namespace: str, name: str) -> str:
    """
    Create a schema in URN format from Avro namespace and name.

    :param namespace: Avro namespace in format "domain.service.event"
    :param name: Avro name in format "EventName"
    :return: Schema URN in format "urn:domain:service:event:EventName"
    """
    return f'urn:{namespace.replace(".", ":")}:{name}'


def gen_avro_schema(
    record_type: str,
    record_schema: str,
    data_fields: Optional[list]
) -> RecordSchema:
    name = record_schema.split(':')[-1]
    namespace = '.'.join(record_schema.split(':')[1:-1])

    fields = [
        {'name': 'type', 'type': 'string'},
        {'name': 'protocol_version', 'type': 'string'},
        {'name': 'version', 'type': 'string'},
        {'name': 'source', 'type': 'string'},
        {'name': 'uuid', 'type': 'string'},
        {'name': 'correlation_id', 'type': 'string'},
        {'name': 'partition_key', 'type': ['string', 'null']},
        {'name': 'date_timestamp', 'type': 'long'},
        {'name': 'date_iso8601', 'type': 'string'},
    ]
    if record_type == 'RESPONSE':
        fields += [
            {'name': 'destination', 'type': 'string'},
            {'name': 'request_uuid', 'type': 'string'},
            {'name': 'ok', 'type': 'boolean'},
            {'name': 'error_code', 'type': ['null', 'int']},
            {'name': 'error_message', 'type': ['null', 'string']},
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
    schema_dict = {
        'name': name,
        'namespace': namespace,
        'type': 'record',
        'fields': fields,
    }
    return avro.schema.parse(json.dumps(schema_dict))


def load_avro_schemas(
    avro_folder: str,
    avro_ext: Optional[str] = None,
    recursive: bool = False,
):
    def _parse_avro_schema_yml(avro_yml_file: str) -> RecordSchema:
        with open(avro_yml_file) as avro_yml:
            yaml_data = yaml.load(avro_yml.read(), Loader=yaml.SafeLoader)
            json_data = json.dumps(yaml_data)
            avro_schema = avro.schema.parse(json_data)

            return avro_schema

    def _iter_schemas(folder: str) -> Iterator[RecordSchema]:
        with os.scandir(folder) as entries:
            entry: os.DirEntry
            for entry in entries:

                # load in sub folder if recursive option set
                if entry.is_dir():
                    if recursive:
                        yield from _iter_schemas(entry.path)
                    else:
                        continue

                # ignores everything that is not a file
                if not entry.is_file():
                    continue  # pragma: nocover

                # ignores hidden files
                if entry.name.startswith("."):
                    continue  # pragma: nocover

                # ignores everything files with wrong extension
                if avro_ext is not None and not entry.name.endswith(avro_ext):
                    continue  # pragma: nocover

                yield _parse_avro_schema_yml(entry.path)

    avro_schema_dict = {
        namespace_name_to_schema(schema.namespace, schema.name): schema
        for schema in _iter_schemas(avro_folder)
    }
    return avro_schema_dict
