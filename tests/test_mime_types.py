import pytest
from openapi_parser.mime_types import ContentType

media_type_provider = (
    ("application/json", ContentType.JSON),
    ("application/*+json", ContentType.JSON_ANY),
    ("application/problem+json", ContentType.JSON_PROBLEM),
    ("text/json", ContentType.JSON_TEXT),
    ("application/xml", ContentType.XML),
    ("application/x-www-form-urlencoded", ContentType.FORM),
    ("multipart/form-data", ContentType.MULTIPART_FORM),
    ("text/plain", ContentType.PLAIN_TEXT),
    ("text/html", ContentType.HTML),
    ("application/pdf", ContentType.PDF),
    ("image/png", ContentType.PNG),
    ("image/jpeg", ContentType.JPEG),
    ("image/gif", ContentType.GIF),
    ("image/svg+xml", ContentType.SVG),
    ("image/avif", ContentType.AVIF),
    ("image/bmp", ContentType.BMP),
    ("image/webp", ContentType.WEBP),
    ("image/*", ContentType.Image),
    ("application/octet-stream", ContentType.BINARY),
)


@pytest.mark.parametrize(['string_value', 'expected'], media_type_provider)
def test_media_type(string_value: str, expected: ContentType) -> None:
    assert ContentType(string_value) == expected


def test_media_type_error() -> None:
    with pytest.raises(ValueError):
        ContentType("invalid")
