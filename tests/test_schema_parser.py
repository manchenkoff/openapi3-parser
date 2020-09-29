import pytest

from swagger_parser import ArraySchema, BooleanSchema, IntSchema, NumberSchema, ObjectSchema, Schema, StringSchema
from swagger_parser.parser import SchemaParser


def test_fail_without_type():
    with pytest.raises(KeyError):
        SchemaParser().parse({})


def test_fail_unsupported_type():
    with pytest.raises(ValueError):
        SchemaParser().parse({'type': 'float'})


parse_data_provider = [
    ({'type': 'integer'}, IntSchema()),
    ({'type': 'number'}, NumberSchema()),
    ({'type': 'string'}, StringSchema()),
    ({'type': 'boolean'}, BooleanSchema()),
    ({'type': 'array', 'items': {'type': 'string'}}, ArraySchema(StringSchema())),
    ({'type': 'object'}, ObjectSchema(tuple())),
]


@pytest.mark.parametrize(['schema_dict', 'expected_schema'], parse_data_provider)
def test_parse(schema_dict: dict, expected_schema: Schema):
    actual_schema = SchemaParser().parse(schema_dict)

    assert actual_schema == expected_schema


def test_full_integer():
    data = {
        'type': 'integer',
        'title': 'Name of integer value',
        'deprecated': False,
        'nullable': False,
        'description': 'Some integer value',
        'format': 'int32',
        'required': True,
        'example': 4,
        'minimum': 0,
        'maximum': 10,
        'default': 0,
        'enum': [],
    }

    expected = IntSchema(
        title=data['title'],
        deprecated=data['deprecated'],
        nullable=data['nullable'],
        description=data['description'],
        format=data['format'],
        required=data['required'],
        example=data['example'],
        minimum=data['minimum'],
        maximum=data['maximum'],
        default=data['default'],
        enum=data['enum'],
    )

    assert expected == SchemaParser().parse(data)


def test_full_number():
    data = {
        'type': 'number',
        'title': 'Name of number value',
        'deprecated': False,
        'nullable': False,
        'description': 'Some number value',
        'format': 'float',
        'required': True,
        'example': 4.0,
        'minimum': 0.0,
        'maximum': 10.0,
        'default': 0.0,
        'enum': [],
    }

    expected = NumberSchema(
        title=data['title'],
        deprecated=data['deprecated'],
        nullable=data['nullable'],
        description=data['description'],
        format=data['format'],
        required=data['required'],
        example=data['example'],
        minimum=data['minimum'],
        maximum=data['maximum'],
        default=data['default'],
        enum=data['enum'],
    )

    assert expected == SchemaParser().parse(data)


def test_full_string():
    data = {
        'type': 'string',
        'title': 'Name of number value',
        'deprecated': False,
        'nullable': False,
        'description': 'Some number value',
        'format': None,
        'example': 'some-string-value',
        'minLength': 0,
        'maxLength': 10,
        'default': 'none',
        'enum': [],
    }

    expected = StringSchema(
        title=data['title'],
        deprecated=data['deprecated'],
        nullable=data['nullable'],
        description=data['description'],
        format=data['format'],
        example=data['example'],
        min_length=data['minLength'],
        max_length=data['maxLength'],
        default=data['default'],
        enum=data['enum'],
    )

    assert expected == SchemaParser().parse(data)


def test_full_bool():
    data = {
        'type': 'boolean',
        'title': 'Name of boolean value',
        'deprecated': False,
        'nullable': False,
        'description': 'Some boolean value',
        'example': False,
        'default': False,
    }

    expected = BooleanSchema(
        title=data['title'],
        deprecated=data['deprecated'],
        nullable=data['nullable'],
        description=data['description'],
        example=data['example'],
        default=data['default'],
    )

    assert expected == SchemaParser().parse(data)


def test_full_array():
    data = {
        'type': 'array',
        'title': 'Name of array value',
        'deprecated': False,
        'nullable': False,
        'description': 'Some array value',
        'minItems': 0,
        'maxItems': 5,
        'items': {'type': 'string'},
    }

    expected = ArraySchema(
        title=data['title'],
        deprecated=data['deprecated'],
        nullable=data['nullable'],
        description=data['description'],
        min_items=data['minItems'],
        max_items=data['maxItems'],
        items_schema=StringSchema()
    )

    assert expected == SchemaParser().parse(data)


def test_full_object():
    data = {
        'type': 'object',
        'title': 'Name of object value',
        'deprecated': False,
        'nullable': False,
        'description': 'Some object value',
        'required': ['property_name'],
        'properties': {
            'property_name': {'type': 'string'}
        },
    }

    object_property = StringSchema(title='property_name')
    object_property.required = True

    expected = ObjectSchema(
        title=data['title'],
        deprecated=data['deprecated'],
        nullable=data['nullable'],
        description=data['description'],
        properties=(object_property,)
    )

    assert expected == SchemaParser().parse(data)
