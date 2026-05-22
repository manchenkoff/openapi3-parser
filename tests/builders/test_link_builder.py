from typing import Any

import pytest

from openapi_parser.builders.link import LinkBuilder
from openapi_parser.specification import Link, Server

data_provider = (
    (
        {
            "operationId": "getUser",
            "parameters": {
                "userId": "{$request.body#/id}",
            },
        },
        Link(
            operation_id="getUser",
            parameters={"userId": "{$request.body#/id}"},
        ),
    ),
    (
        {
            "operationRef": "#/paths/~1users~1{userId}/get",
            "description": "Get user details",
        },
        Link(
            operation_ref="#/paths/~1users~1{userId}/get",
            description="Get user details",
        ),
    ),
    (
        {
            "operationId": "getUser",
            "requestBody": "{$request.body#/id}",
            "server": {
                "url": "https://example.com/api",
            },
        },
        Link(
            operation_id="getUser",
            request_body="{$request.body#/id}",
            server=Server(url="https://example.com/api"),
        ),
    ),
)


@pytest.mark.parametrize(["data", "expected"], data_provider)
def test_build(data: dict[str, Any], expected: Link) -> None:
    builder = LinkBuilder()

    result = builder._build(data)

    assert expected == result


def test_build_with_extensions() -> None:
    builder = LinkBuilder()

    result = builder._build(
        {
            "operationId": "getUser",
            "x-custom-link": "value",
        }
    )

    assert result.operation_id == "getUser"
    assert result.extensions == {"custom_link": "value"}


def test_build_dict() -> None:
    builder = LinkBuilder()

    result = builder.build_dict(
        {
            "getUserById": {
                "operationId": "getUser",
                "parameters": {"userId": "{$request.body#/id}"},
            },
            "getUserByEmail": {
                "operationId": "getUserByEmail",
            },
        }
    )

    assert result == {
        "getUserById": Link(
            operation_id="getUser",
            parameters={"userId": "{$request.body#/id}"},
        ),
        "getUserByEmail": Link(operation_id="getUserByEmail"),
    }
