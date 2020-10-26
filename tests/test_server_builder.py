from typing import List

import pytest

from src.swagger_parser import Server
from src.swagger_parser.parser import ServerBuilder

data_provider = [
    [
        [],
        [],
    ],
    [
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
    ],
    [
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
    ],
]


@pytest.mark.parametrize(['server_data_list', 'expected_server_list'], data_provider)
def test_build_server_list(server_data_list: list, expected_server_list: List[Server]):
    builder = ServerBuilder()
    assert expected_server_list == builder.build_server_list(server_data_list)
