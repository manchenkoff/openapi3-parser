from unittest import mock

from swagger_parser import Content, ContentType, IntSchema
from swagger_parser.parser import ContentParser


def _get_schema_parser_mock():
    schema_parser_mock = mock.Mock()
    schema_parser_mock.parse = mock.MagicMock(return_value=IntSchema())

    return schema_parser_mock


def test_parse():
    data = {
        'application/json': {
            'schema': {
                'type': 'integer',
            }
        }
    }

    expected = Content(ContentType.application_json, IntSchema())

    schema_parser_mock = _get_schema_parser_mock()
    content_parser = ContentParser(schema_parser_mock)

    assert expected == content_parser.parse(data)[ContentType.application_json]

    schema_parser_mock.parse.assert_called_once_with(
        data['application/json']['schema']
    )
