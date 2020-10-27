from typing import List
from unittest import mock

import pytest

from swagger_parser.specification import ExternalDoc, Tag
from swagger_parser.builders import ExternalDocBuilder, TagBuilder

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


def _create_external_doc_builder_mock(expected_tags: List[Tag]) -> ExternalDocBuilder:
    idx = 0

    def get_return_value(*args):
        nonlocal idx

        return_value = expected_tags[idx].external_docs
        idx += 1

        return return_value

    mock_object = mock.MagicMock()
    mock_object.build.side_effect = get_return_value

    return mock_object


@pytest.mark.parametrize(['tag_list_data', 'expected_tags'], data_provider)
def test_build_tag_list(tag_list_data: list, expected_tags: List[Tag]):
    external_doc_builder = _create_external_doc_builder_mock(expected_tags)
    builder = TagBuilder(external_doc_builder)

    assert expected_tags == builder.build_tag_list(tag_list_data)
