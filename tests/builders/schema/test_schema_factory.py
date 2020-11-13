from typing import Dict
from unittest.mock import MagicMock

import pytest

from openapi_parser.builders.schema import SchemaFactory
from openapi_parser.enumeration import DataType
from openapi_parser.errors import ParserError


@pytest.fixture()
def container():
    return {
        data_type: MagicMock()
        for data_type in
        (DataType.INTEGER, DataType.NUMBER, DataType.STRING, DataType.ARRAY, DataType.OBJECT)
    }


data_provider = (
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


@pytest.mark.parametrize(['data', 'expected_type'], data_provider)
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
