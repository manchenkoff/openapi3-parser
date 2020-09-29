from unittest import mock

from swagger_parser import Content, ContentType, RequestBody, StringSchema
from swagger_parser.parser import ContentParser, RequestBodyParser


def _get_content_parser_mock(data) -> ContentParser:
    content_parser_mock = mock.Mock()
    content_parser_mock.parse = mock.MagicMock(return_value=data)

    return content_parser_mock


def test_parse():
    data = {
        'requestBody': {
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'string'
                    }
                }
            }
        }
    }

    expected_request_body = RequestBody(
        {
            ContentType.application_json: Content(ContentType.application_json, StringSchema()),
        },
        False
    )

    content_parser = _get_content_parser_mock(expected_request_body.contents)
    request_parser = RequestBodyParser(content_parser)

    assert expected_request_body == request_parser.parse(data)
