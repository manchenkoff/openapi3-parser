from typing import Dict
from unittest.mock import MagicMock

import pytest

from openapi_parser.builders.common import extract_extension_attributes
from openapi_parser.builders.schema import merge_all_of_schemas, SchemaFactory
from openapi_parser.enumeration import DataType
from openapi_parser.errors import ParserError


@pytest.fixture()
def container():
    return {
        data_type: MagicMock()
        for data_type in
        (DataType.INTEGER, DataType.NUMBER, DataType.STRING, DataType.ARRAY, DataType.OBJECT)
    }


schema_data_provider = (
    (
        {"type": "integer"},
        DataType.INTEGER
    ),
    (
        {"type": "number"},
        DataType.NUMBER
    ),
    (
        {"type": "string"},
        DataType.STRING
    ),
    (
        {"type": "array"},
        DataType.ARRAY
    ),
    (
        {"type": "object"},
        DataType.OBJECT
    ),
)


@pytest.mark.parametrize(['data', 'expected_type'], schema_data_provider)
def test_create(data: dict, expected_type: DataType, container: Dict[DataType, MagicMock]):
    factory = SchemaFactory()
    factory._builders = container

    factory.create(data)

    container[expected_type].assert_called_once()


def test_create_error():
    data = {"type": "unsupported"}
    factory = SchemaFactory()

    with pytest.raises(ParserError, match="Invalid schema type"):
        factory.create(data)


def test_container_error():
    data = {"type": "integer"}
    factory = SchemaFactory()
    factory._builders = {}

    with pytest.raises(ParserError, match="Unsupported schema type"):
        factory.create(data)


merge_schemas_data_provider = (
    (
        {
            "allOf": [
                {
                    "type": "object",
                },
                {
                    "title": "UserDTO",
                    "description": "User Data Transfer Object",
                },
                {
                    "title": "UserDTO",
                    "description": "Replaced Description",
                },
            ],
        },
        {
            "type": "object",
            "title": "UserDTO",
            "description": "Replaced Description",
        }
    ),
    (
        {
            "allOf": [
                {
                    "type": "object",
                },
                {
                    "title": "UserDTO",
                    "description": "User Data Transfer Object",
                },
                {
                    "description": "Replaced Description",
                },
                {
                    "properties": {
                        "login": {"type": "string"},
                        "email": {"type": "string"},
                    },
                },
                {
                    "properties": {
                        "firstname": {"type": "string"},
                        "lastname": {"type": "string"},
                    },
                },
            ],
        },
        {
            "type": "object",
            "title": "UserDTO",
            "description": "Replaced Description",
            "properties": {
                "login": {"type": "string"},
                "email": {"type": "string"},
                "firstname": {"type": "string"},
                "lastname": {"type": "string"},
            }
        }
    ),
    (
        {
            "allOf": [
                {
                    "type": "object",
                    "title": "UserDTO",
                    "description": "User Data Transfer Object",
                },
                {
                    "properties": {
                        "login": {"type": "string"},
                        "email": {"type": "object"},
                        "info": {
                            "type": "object",
                            "properties": {
                                "first_name": {"type": "string"},
                                "last_name": {"type": "string"},
                                "card": {
                                    "type": "object",
                                    "properties": {
                                        "holder": {"type": "string", "required": True},
                                        "number": {"type": "integer", "required": True},
                                    }
                                },
                            },
                        },
                    },
                },
                {
                    "properties": {
                        "email": {"type": "string", "example": "john@doe.com"},
                        "info": {
                            "properties": {
                                "last_name": {"type": "string", "required": True},
                                "card": {
                                    "properties": {
                                        "cvc": {"type": "integer", "required": True},
                                    }
                                }
                            },
                        },
                    },
                },
            ],
        },
        {
            "type": "object",
            "title": "UserDTO",
            "description": "User Data Transfer Object",
            "properties": {
                "login": {"type": "string"},
                "email": {"type": "string", "example": "john@doe.com"},
                "info": {
                    "type": "object",
                    "properties": {
                        "first_name": {"type": "string"},
                        "last_name": {"type": "string", "required": True},
                        "card": {
                            "type": "object",
                            "properties": {
                                "holder": {"type": "string", "required": True},
                                "number": {"type": "integer", "required": True},
                                "cvc": {"type": "integer", "required": True},
                            }
                        },
                    },
                },
            }
        }
    ),
)


@pytest.mark.parametrize(['original_data', 'expected'], merge_schemas_data_provider)
def test_merge_all_of_schemas(original_data: dict, expected: dict):
    assert merge_all_of_schemas(original_data) == expected


extension_schema_provider = (
    (
        {
            "type": "object",
            "title": "Object with extension attributes",
            "x-number-attribute": 123,
            "x-boolean-attribute": False,
            "x-object-attribute": {
                "key1": "value",
                "key2": "another value"
            },
        },
        {
            "number_attribute": 123,
            "boolean_attribute": False,
            "object_attribute": {
                "key1": "value",
                "key2": "another value"
            },
        },
    ),
)


@pytest.mark.parametrize(['original_data', 'expected'], extension_schema_provider)
def test_extension_attributes_extracting(original_data: dict, expected: dict):
    assert extract_extension_attributes(original_data) == expected
