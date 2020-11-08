from typing import List
from unittest import mock

import pytest

from openapi_parser.specification import ExternalDoc, Tag
from openapi_parser.builders import ExternalDocBuilder, TagBuilder

data_provider = (
    (
        None,
        [],
    ),
    (
        [],
        [],
    ),
    (
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
    ),
)


def _create_external_doc_builder_mock(expected_tags: List[Tag]) -> ExternalDocBuilder:
    mock_object = mock.MagicMock()
    mock_object.build.side_effect = [item.external_docs for item in expected_tags]

    return mock_object


@pytest.mark.parametrize(['data', 'expected'], data_provider)
def test_build_list(data: list, expected: List[Tag]):
    external_doc_builder = _create_external_doc_builder_mock(expected)
    builder = TagBuilder(external_doc_builder)

    assert expected == builder.build_list(data)
