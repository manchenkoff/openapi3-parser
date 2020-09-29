from typing import Dict
from unittest import mock

from src.swagger_parser import Content, ContentType, IntSchema, Operation, OperationMethod, Response
from src.swagger_parser.parser import OperationParser


def _get_content_parser_mock(expected_content: Dict[ContentType, Content]) -> mock.MagicMock:
    mock_object = mock.Mock()
    mock_object.parse = mock.MagicMock(return_value=expected_content)

    return mock_object


def test_parse():
    data = {
        'get': {
            'summary': 'Operation description',
            'operationId': 'someOperation',
            'responses': {
                '200': {
                    'description': 'Response description',
                    'content': {
                        'application/json': {
                            'schema': {
                                'type': 'integer',
                            },
                        },
                    },
                },
            },
        }
    }

    expected_operation = Operation(
        OperationMethod.GET,
        [],
        data['get']['summary'],
        data['get']['operationId'],
        tuple(),
        None,
        (
            Response(
                200,
                data['get']['responses']['200']['description'],
                {
                    ContentType.application_json: Content(ContentType.application_json, IntSchema()),
                }
            ),
        )
    )

    content_parser_mock = _get_content_parser_mock(expected_operation.responses[0].contents)
    operation_parser = OperationParser(content_parser_mock)

    assert expected_operation == operation_parser.parse('get', data['get'])

    content_parser_mock.parse.assert_called_once_with(
        data['get']['responses']['200']['content']
    )


def test_parse_list():
    pass
