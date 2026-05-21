from typing import Any

import pytest

from openapi_parser.builders.info import InfoBuilder
from openapi_parser.errors import ParserError
from openapi_parser.specification import Contact, Info, License

data_provider = (
    (
        {"title": "Sample Pet Store App", "version": "1.0.1"},
        Info(title="Sample Pet Store App", version="1.0.1"),
    ),
    (
        {
            "title": "Sample Pet Store App",
            "version": "1.0.1",
            "x-rnd-team": "super team",
        },
        Info(
            title="Sample Pet Store App",
            version="1.0.1",
            extensions={"rnd_team": "super team"},
        ),
    ),
    (
        {
            "title": "Sample Pet Store App",
            "description": "This is a sample server for a pet store.",
            "termsOfService": "http://example.com/terms/",
            "contact": {
                "name": "API Support",
                "url": "http://www.example.com/support",
                "email": "support@example.com",
            },
            "license": {
                "name": "Apache 2.0",
                "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
            },
            "version": "1.0.1",
        },
        Info(
            title="Sample Pet Store App",
            version="1.0.1",
            description="This is a sample server for a pet store.",
            terms_of_service="http://example.com/terms/",
            contact=Contact(
                name="API Support",
                url="http://www.example.com/support",
                email="support@example.com",
            ),
            license=License(
                name="Apache 2.0",
                url="https://www.apache.org/licenses/LICENSE-2.0.html",
            ),
        ),
    ),
)


@pytest.mark.parametrize(["data", "expected"], data_provider)
def test_build(data: dict[str, Any], expected: Info) -> None:
    builder = InfoBuilder()

    assert expected == builder.build(data)


def test_build_missing_title() -> None:
    builder = InfoBuilder()

    with pytest.raises(ParserError, match="missing required 'title' property"):
        builder.build({"version": "1.0.0"})


def test_build_missing_license_name() -> None:
    builder = InfoBuilder()

    with pytest.raises(ParserError, match="missing required 'name' property"):
        builder.build(
            {
                "title": "Test",
                "version": "1.0",
                "license": {"url": "https://example.com"},
            }
        )
