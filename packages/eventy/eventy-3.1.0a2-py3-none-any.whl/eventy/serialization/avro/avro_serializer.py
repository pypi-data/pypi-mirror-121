# Copyright (c) Qotto, 2021

from io import BytesIO
from typing import Union

from avro.datafile import DataFileWriter, DataFileReader
from avro.io import DatumWriter, AvroTypeException, DatumReader
from avro.schema import RecordSchema

from eventy.record import Record, Event, Request, Response
from eventy.serialization import RecordSerializer, SerializationError
from eventy.serialization.common import create_dict_from_record, create_record_from_dict


class AvroSerializer(RecordSerializer):

    def __init__(
        self,
        avro_schemas: dict[str, RecordSchema] = None
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
        record_datum = create_dict_from_record(record)

        try:
            bytes_io = BytesIO()
            with DataFileWriter(bytes_io, DatumWriter(), avro_schema) as writer:
                writer.append(record_datum)
                writer.flush()
                output_bytes = bytes_io.getvalue()
            return output_bytes
        except AvroTypeException as avro_exception:
            raise SerializationError(avro_exception)

    def decode(self, encoded: bytes) -> Union[Event, Request, Response]:
        reader = DataFileReader(BytesIO(encoded), DatumReader())
        record_dict = next(reader)
        return create_record_from_dict(record_dict)
