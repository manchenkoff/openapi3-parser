import pytest

from src.swagger_parser.parser import ParserException, SchemaResolver

schema_to_resolve = {
    'allOf': [
        {
            'type': 'object',
            'required': ['status'],
            'properties': {
                'status': {
                    'type': 'string',
                    'example': 'SUCCESS'
                }
            }
        },
        {
            'title': 'SuccessfulResponse',
            'required': ['status', 'users'],
            'properties': {
                'users': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'required': ['login'],
                        'properties': {
                            'login': {
                                'type': 'string',
                                'example': 'John Doe',
                                'description': 'User login'
                            }
                        }
                    }
                }
            }
        }
    ]
}

schema_after_resolve = {
    'title': 'SuccessfulResponse',
    'type': 'object',
    'required': ['status', 'users'],
    'properties': {
        'status': {
            'type': 'string',
            'example': 'SUCCESS'
        },
        'users': {
            'type': 'array',
            'items': {
                'type': 'object',
                'required': ['login'],
                'properties': {
                    'login': {
                        'type': 'string',
                        'example': 'John Doe',
                        'description': 'User login'
                    }
                }
            }
        }
    }
}

schema_with_exception = {
    'oneOf': [
        {
            'type': 'object',
            'required': ['status'],
            'properties': {
                'status': {
                    'type': 'string',
                    'example': 'SUCCESS'
                }
            }
        },
        {
            'title': 'SuccessfulResponse',
            'required': ['status', 'users'],
            'properties': {
                'users': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'required': ['login'],
                        'properties': {
                            'login': {
                                'type': 'string',
                                'example': 'John Doe',
                                'description': 'User login'
                            }
                        }
                    }
                }
            }
        }
    ]
}


@pytest.mark.parametrize(
    ['input_dict', 'expected_dict'],
    [(schema_to_resolve, schema_after_resolve)]
)
def test_resolve(input_dict: dict, expected_dict: dict):
    resolver = SchemaResolver()
    actual_dict = resolver.resolve(input_dict)

    assert actual_dict == expected_dict


@pytest.mark.parametrize(
    ['input_dict'],
    [(schema_with_exception,)]
)
def test_resolve_failed(input_dict: dict):
    with pytest.raises(ParserException):
        resolver = SchemaResolver()
        resolver.resolve(input_dict)
