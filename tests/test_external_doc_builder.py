from typing import List

import pytest

from swagger_parser.builders import ExternalDocBuilder
from swagger_parser.specification import ExternalDoc

data_provider = (
    (
        None,
        None,
    ),
    (
        {
            "url": "https://example.com"
        },
        ExternalDoc(url="https://example.com"),
    ),
    (
        {
            "description": "Find more info here",
            "url": "https://example.com"
        },
        ExternalDoc(url="https://example.com", description="Find more info here"),
    ),
)


@pytest.mark.parametrize(['data', 'expected'], data_provider)
def test_build(data: dict, expected: List[ExternalDoc]):
    builder = ExternalDocBuilder()

    assert expected == builder.build(data)
