from unittest.mock import MagicMock

import pytest

from openapi_parser.builders import ExternalDocBuilder, OperationBuilder, ParameterBuilder, RequestBuilder, \
    ResponseBuilder
from openapi_parser.enumeration import DataType, MediaType, ParameterLocation
from openapi_parser.specification import Content, ExternalDoc, Object, Operation, Parameter, Property, RequestBody, \
    Response, String


def _get_builder_mock(expected):
    mock_object = MagicMock()
    mock_object.build.return_value = expected

    return mock_object


def _get_collection_builder_mock(expected):
    mock_object = MagicMock()
    mock_object.build_collection.return_value = expected

    return mock_object


response_schema = Response(
    description="Pet updated.",
    content={MediaType.JSON: Content(schema=Object(type=DataType.OBJECT))}
)

parameter_list = [
    Parameter(
        name="petId",
        location=ParameterLocation.PATH,
        description="ID of pet that needs to be updated",
        required=True,
        schema=String(type=DataType.STRING),
    )
]

external_doc = ExternalDoc(description="Find more info here", url="https://example.com")

request_body = RequestBody(
    content={
        MediaType.FORM: Content(
            schema=Object(
                type=DataType.OBJECT, required=["status"],
                properties=[
                    Property(
                        name="name",
                        schema=String(
                            type=DataType.STRING,
                            description="Updated name of the pet"
                        )
                    ),
                    Property(
                        name="status",
                        schema=String(
                            type=DataType.STRING,
                            description="Updated status of the pet")
                    ),
                ],
            )
        ),
    }
)


data_provider = (
    (
        {
            "responses": {
                "200": {
                    "description": "Pet updated.",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                            }
                        },
                    }
                },
            },
        },
        Operation(
            responses={
                200: response_schema
            }
        ),
        _get_builder_mock(response_schema),
        _get_builder_mock(None),
        _get_builder_mock(None),
        _get_collection_builder_mock(None),
    ),
    (
        {
            "responses": {
                "200": {
                    "description": "Pet updated.",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                            }
                        },
                    }
                },
            },
            "tags": [
                "pet",
            ],
            "security": [
                {"Basic": []}
            ],
            "summary": "Updates a pet in the store with form data",
            "operationId": "updatePetWithForm",
            "parameters": [
                {
                    "name": "petId",
                    "in": "path",
                    "description": "ID of pet that needs to be updated",
                    "required": True,
                    "schema": {
                        "type": "string"
                    }
                }
            ],
            "requestBody": {
                "content": {
                    "application/x-www-form-urlencoded": {
                        "schema": {
                            "type": "object",
                            "properties": {
                                "name": {
                                    "description": "Updated name of the pet",
                                    "type": "string"
                                },
                                "status": {
                                    "description": "Updated status of the pet",
                                    "type": "string"
                                }
                            },
                            "required": ["status"]
                        }
                    }
                }
            },
            "externalDocs": {
                "description": "Find more info here",
                "url": "https://example.com"
            }
        },
        Operation(
            responses={
                200: response_schema
            },
            tags=["pet"],
            security=[{"Basic": []}],
            summary="Updates a pet in the store with form data",
            operation_id="updatePetWithForm",
            parameters=parameter_list,
            request_body=request_body,
            external_docs=external_doc
        ),
        _get_builder_mock(response_schema),
        _get_builder_mock(external_doc),
        _get_builder_mock(request_body),
        _get_collection_builder_mock(parameter_list),
    ),
)


@pytest.mark.parametrize(
    [
        'data', 'expected_operation', 'response_builder',
        'external_doc_builder', 'request_builder', 'parameter_builder'
    ],
    data_provider
)
def test_build(data: dict,
               expected_operation: Operation,
               response_builder: ResponseBuilder,
               external_doc_builder: ExternalDocBuilder,
               request_builder: RequestBuilder,
               parameter_builder: ParameterBuilder):
    builder = OperationBuilder(
        response_builder,
        external_doc_builder,
        request_builder,
        parameter_builder
    )

    assert expected_operation == builder.build(data)
