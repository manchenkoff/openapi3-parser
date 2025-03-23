from typing import List

import pytest

from openapi_parser.builders.external_doc import ExternalDocBuilder
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
            "url": "https://example.com",
        },
        ExternalDoc(url="https://example.com", description="Find more info here"),
    ),
    (
        {
            "description": "Find more info here",
            "url": "https://example.com",
            "x-logo-url": "https://example.com/logo.png",
        },
        ExternalDoc(
            url="https://example.com",
            description="Find more info here",
            extensions={"logo_url": "https://example.com/logo.png"}
        ),
    ),
)


@pytest.mark.parametrize(['data', 'expected'], data_provider)
def test_build(data: dict, expected: List[ExternalDoc]):
    builder = ExternalDocBuilder()
    assert expected == builder.build(data)
