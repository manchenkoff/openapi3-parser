from typing import List

import pytest

from openapi_parser.builders.server import ServerBuilder
from openapi_parser.specification import Server

data_provider = (
    (
        [],
        [],
    ),
    (
        [
            {
                "url": "https://development.gigantic-server.com/v1",
            },
            {
                "url": "https://staging.gigantic-server.com/v1",
            },
            {
                "url": "https://api.gigantic-server.com/v1",
            }
        ],
        [
            Server(url="https://development.gigantic-server.com/v1"),
            Server(url="https://staging.gigantic-server.com/v1"),
            Server(url="https://api.gigantic-server.com/v1"),
        ],
    ),
    (
        [
            {
                "url": "https://development.gigantic-server.com/v1",
                "description": "Development server"
            },
            {
                "url": "https://staging.gigantic-server.com/v1",
                "description": "Staging server"
            },
            {
                "url": "https://api.gigantic-server.com/v1",
                "description": "Production server"
            }
        ],
        [
            Server(url="https://development.gigantic-server.com/v1",
                   description="Development server"),
            Server(url="https://staging.gigantic-server.com/v1",
                   description="Staging server"),
            Server(url="https://api.gigantic-server.com/v1",
                   description="Production server"),
        ],
    ),
    (
        [
            {
                "url": "https://development.gigantic-server.com/v1",
                "x-internal": True,
                "description": "Development server"
            },
            {
                "url": "https://staging.gigantic-server.com/v1",
                "description": "Staging server"
            },
            {
                "url": "https://api.gigantic-server.com/v1",
                "description": "Production server"
            }
        ],
        [
            Server(url="https://development.gigantic-server.com/v1",
                   description="Development server",
                   extensions={"internal": True}),
            Server(url="https://staging.gigantic-server.com/v1",
                   description="Staging server"),
            Server(url="https://api.gigantic-server.com/v1",
                   description="Production server"),
        ],
    ),
)


@pytest.mark.parametrize(['data', 'expected'], data_provider)
def test_build_list(data: list, expected: List[Server]):
    builder = ServerBuilder()

    assert expected == builder.build_list(data)
