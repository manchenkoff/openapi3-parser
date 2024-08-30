import copy
from random import sample
from unittest.mock import MagicMock

import pytest

from openapi_parser.builders import OperationBuilder, ParameterBuilder, PathBuilder
from openapi_parser.enumeration import ContentType, DataType, OperationMethod, ParameterLocation
from openapi_parser.specification import Array, Content, Operation, Parameter, Path, Response, String


def _get_builder_mock(expected_value):
    mock_object = MagicMock()
    mock_object.build.return_value = expected_value

    return mock_object


def _get_builder_list_mock(expected_value):
    mock_object = MagicMock()
    mock_object.build_list.return_value = expected_value

    return mock_object


array_schema = Array(type=DataType.ARRAY, items=String(type=DataType.STRING))

parameters_list = [
    Parameter(
        name="id",
        location=ParameterLocation.PATH,
        description="ID of pet to use",
        required=True,
        schema=array_schema
    )
]

operation_object = Operation(
    method=OperationMethod.GET,
    description="Returns pets based on ID",
    summary="Find pets by ID",
    operation_id="getPetsById",
    responses=[
        Response(
            code=200,
            description="pet response",
            content=[Content(type=ContentType.JSON, schema=array_schema, example="an example", examples=[])],
            is_default=False,
        )
    ],
)

expected_operation_object = copy.deepcopy(operation_object)


def add_parameters_to_operation(operation, parameters):
    operation_copy = copy.deepcopy(operation)
    operation_copy.parameters = parameters
    return operation_copy


data_provider = (
    (
        {
            "/pets": {
                "get": {
                    "description": "Returns pets based on ID",
                    "summary": "Find pets by ID",
                    "operationId": "getPetsById",
                    "responses": {
                        "200": {
                            "description": "pet response",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "type": "string",
                                        }
                                    }
                                }
                            }
                        },
                    }
                },
            }
        },
        [
            Path(
                url="/pets",
                operations=[expected_operation_object]
            )
        ],
        _get_builder_mock(operation_object),
        _get_builder_list_mock(None),
    ),
    (
        {
            "/pets": {
                "x-python-class": "Pet",
                "get": {
                    "description": "Returns pets based on ID",
                    "summary": "Find pets by ID",
                    "operationId": "getPetsById",
                    "responses": {
                        "200": {
                            "description": "pet response",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "type": "string",
                                        }
                                    }
                                }
                            }
                        },
                    }
                },
            }
        },
        [
            Path(
                url="/pets",
                operations=[expected_operation_object],
                extensions={"python_class": "Pet"}
            )
        ],
        _get_builder_mock(operation_object),
        _get_builder_list_mock(None),
    ),
    (
        {
            "/pets/{id}": {
                "summary": "Summary description",
                "description": "Long description",
                "get": {
                    "description": "Returns pets based on ID",
                    "summary": "Find pets by ID",
                    "operationId": "getPetsById",
                    "responses": {
                        "200": {
                            "description": "pet response",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "type": "string",
                                        }
                                    }
                                }
                            }
                        },
                    }
                },
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "description": "ID of pet to use",
                        "required": True,
                        "schema": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        },
                    }
                ]
            }
        },
        [
            Path(
                url="/pets/{id}",
                summary="Summary description",
                description="Long description",
                parameters=parameters_list,
                operations=[add_parameters_to_operation(expected_operation_object, parameters_list)]
            )
        ],
        _get_builder_mock(operation_object),
        _get_builder_list_mock(parameters_list),
    ),
)


@pytest.mark.parametrize(['data', 'expected', 'operation_builder', 'parameter_builder'], data_provider)
def test_build(data: dict,
               expected: list[Path],
               operation_builder: OperationBuilder,
               parameter_builder: ParameterBuilder):
    builder = PathBuilder(operation_builder, parameter_builder)

    assert expected == builder.build_list(data)
