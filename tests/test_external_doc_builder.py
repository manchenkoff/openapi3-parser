from typing import List

import pytest

from swagger_parser.builders import ExternalDocBuilder
from swagger_parser.specification import ExternalDoc

data_provider = [
    [
        None,
        None,
    ],
    [
        {
            "url": "https://example.com"
        },
        ExternalDoc(url="https://example.com"),
    ],
    [
        {
            "description": "Find more info here",
            "url": "https://example.com"
        },
        ExternalDoc(url="https://example.com", description="Find more info here"),
    ],
]


@pytest.mark.parametrize(['doc_list_data', 'expected_docs'], data_provider)
def test_build(doc_list_data: dict, expected_docs: List[ExternalDoc]):
    builder = ExternalDocBuilder()

    assert expected_docs == builder.build(doc_list_data)
