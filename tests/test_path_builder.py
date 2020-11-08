from typing import List

import pytest

from openapi_parser.builders import PathBuilder
from openapi_parser.specification import Path, PathItem

data_provider = (
    (
        None,
        []
    ),
    (
        {},
        []
    ),
    (
        {
            "/pets": {
                "summary": "common summary string",
                "description": "common description string",
                "get": {
                    "description": "Returns all pets from the system that the user has access to",
                    "responses": {
                        "200": {
                            "description": "A list of pets.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "$ref": "#/components/schemas/pet"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        [
            Path(pattern='/pets',
                 item=PathItem(summary="common summary string",
                               description="common description string",
                               operations={},
                               parameters=[])
                 )
        ],
    ),
)


@pytest.mark.parametrize(['data', 'expected'], data_provider)
def test_build_list(data: dict, expected: List[Path]):
    builder = PathBuilder()

    # TODO: use Operation and Parameter parsers

    assert expected == builder.build_list(data)
