import pytest

from openapi_parser.builders.schema import SchemaFactory
from openapi_parser.enumeration import IntegerFormat
from openapi_parser.specification import DataType, Discriminator, Integer, OneOf, String, StringFormat

data_provider = (
    (
        {
            "oneOf": [
                {
                    "type": "string",
                    "maxLength": 1,
                    "minLength": 0,
                    "pattern": "[0-9]",
                    "format": "uuid",
                },
                {
                    "type": "integer",
                    "format": "int32",
                }
            ],
        },
        OneOf(
            type=DataType.ONE_OF,
            schemas=[
                String(
                    type=DataType.STRING,
                    max_length=1,
                    min_length=0,
                    pattern="[0-9]",
                    format=StringFormat.UUID,
                ),
                Integer(
                    type=DataType.INTEGER,
                    format=IntegerFormat.INT32,
                ),
            ]
        )
    ),
    (
        {
            "oneOf": [
                {
                    "type": "string",
                    "maxLength": 1,
                    "minLength": 0,
                    "pattern": "[0-9]",
                    "format": "uuid",
                },
                {
                    "type": "integer",
                    "format": "int32",
                }
            ],
            "discriminator": {
                "propertyName": "objectType",
            },
        },
        OneOf(
            type=DataType.ONE_OF,
            schemas=[
                String(
                    type=DataType.STRING,
                    max_length=1,
                    min_length=0,
                    pattern="[0-9]",
                    format=StringFormat.UUID,
                ),
                Integer(
                    type=DataType.INTEGER,
                    format=IntegerFormat.INT32,
                ),
            ],
            discriminator=Discriminator(
                property_name="objectType",
            )
        )
    ),
    (
        {
            "oneOf": [
                {
                    "type": "string",
                    "maxLength": 1,
                    "minLength": 0,
                    "pattern": "[0-9]",
                    "format": "uuid",
                },
                {
                    "type": "integer",
                    "format": "int32",
                }
            ],
            "discriminator": {
                "propertyName": "objectType",
                "mapping": {
                    "objectType1": {
                        "type": "string",
                        "maxLength": 1,
                        "minLength": 0,
                        "pattern": "[0-9]",
                        "format": "uuid",
                    },
                    "objectType2": {
                        "type": "integer",
                        "format": "int32",
                    },
                },
            },
        },
        OneOf(
            type=DataType.ONE_OF,
            schemas=[
                String(
                    type=DataType.STRING,
                    max_length=1,
                    min_length=0,
                    pattern="[0-9]",
                    format=StringFormat.UUID,
                ),
                Integer(
                    type=DataType.INTEGER,
                    format=IntegerFormat.INT32,
                ),
            ],
            discriminator=Discriminator(
                property_name="objectType",
                mapping={
                    "objectType1": String(
                        type=DataType.STRING,
                        max_length=1,
                        min_length=0,
                        pattern="[0-9]",
                        format=StringFormat.UUID,
                    ),
                    "objectType2": Integer(
                        type=DataType.INTEGER,
                        format=IntegerFormat.INT32,
                    ),
                },
            )
        )
    ),
)


@pytest.mark.parametrize(['data', 'expected'], data_provider)
def test_string_builder(data: dict, expected: String):
    factory = SchemaFactory()
    assert expected == factory.create(data)
