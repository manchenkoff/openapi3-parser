from typing import List

import pytest

from src.swagger_parser import ExternalDoc, Tag
from src.swagger_parser.parser import TagBuilder

data_provider = [
    [
        [],
        [],
    ],
    [
        [
            {
                "name": "Users",
            },
            {
                "name": "Users",
                "description": "User operations"
            },
            {
                "name": "Users",
                "description": "User operations",
                "externalDocs": {
                    "description": "Find more info here",
                    "url": "https://example.com"
                }
            },
        ],
        [
            Tag(name="Users"),
            Tag(name="Users", description="User operations"),
            Tag(name="Users",
                description="User operations",
                external_docs=ExternalDoc(url="https://example.com", description="Find more info here")),
        ],
    ],
]


@pytest.mark.parametrize(['tag_list_data', 'expected_tags'], data_provider)
def test_build_tag_list(tag_list_data: list, expected_tags: List[Tag]):
    builder = TagBuilder()
    assert expected_tags == builder.build_tag_list(tag_list_data)
