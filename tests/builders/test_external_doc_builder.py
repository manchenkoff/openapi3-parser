from typing import List

import pytest

from openapi_parser.builders import ExternalDocBuilder
from openapi_parser.specification import ExternalDoc

data_provider = (
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
