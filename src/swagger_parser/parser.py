from abc import ABC, abstractmethod
from typing import Callable, KeysView

import prance

from .specification import *


class ParserException(Exception):
    """
    Base parser exception class.
    Throws when any error occurs.
    """
    pass


class ParserInterface(ABC):
    @abstractmethod
    def load_specification(self, uri: str) -> Specification:
        """
        Load Swagger Specification object from a file or a remote URI.
        :param uri: Path to a file or resource
        :return: Specification object
        """
        pass


class SchemaResolver:
    """
    Helper for merging Swagger 'allOf' sections into one dictionary
    """
    _resolving_key = 'allOf'
    _denied_keys = ('anyOf', 'oneOf', 'not')

    def resolve(self, data: dict) -> dict:
        """
        Normalize a schema dictionary with 'allOf' key
        """
        schema_keys = data.keys()

        self._validate_keys(schema_keys)

        if self._resolving_key not in schema_keys:
            return data

        schemas_to_resolve = data[self._resolving_key]
        merged = {}

        for schema in schemas_to_resolve:
            self._dict_merge(merged, schema)

        return merged

    def _validate_keys(self, schema_keys: KeysView):
        """
        Check if there are schema keys which are not supported
        """
        for denied_key in self._denied_keys:
            if denied_key in schema_keys:
                raise ParserException(f"Parsing of '{denied_key}' attribute is not supported")

    def _dict_merge(self, base: dict, other: dict) -> dict:
        """
        Recursive merge dictionaries instead of top-level ```dict.update()```
        """
        for key, value in other.items():
            base[key] = self._dict_merge(base.get(key, {}), value) if isinstance(value, dict) else value

        return base


class SchemaParser:
    resolver: SchemaResolver
    schema_type_builders: Dict[DataType, Callable]

    def __init__(self) -> None:
        self.resolver = SchemaResolver()

        self.schema_type_builders = {
            DataType.int: self.int,
            DataType.number: self.number,
            DataType.string: self.string,
            DataType.bool: self.bool,
            DataType.array: self.array,
            DataType.object: self.object,
        }

    def parse(self, data: dict) -> Schema:
        """
        Parse 'schema' section into object
        """
        resolved_schema = self.resolver.resolve(data)
        builder = self._get_schema_builder(resolved_schema)

        return builder(resolved_schema)

    def _get_schema_builder(self, data: dict) -> Callable:
        """
        Returns parser method based on 'type' field
        """
        data_type = DataType(data['type'])
        return self.schema_type_builders[data_type]

    @staticmethod
    def _parse_base_parameters(data: dict) -> dict:
        """
        Parse common schema attributes with default values
        """
        return {
            "type": data['type'],
            "title": data.get('title'),
            "deprecated": data.get('deprecated', False),
            "nullable": data.get('nullable', False),
            "description": data.get('description'),
            "format": data.get('format'),
        }

    def _parse_common_number_parameters(self, data: dict, assert_type: type) -> dict:
        """
        Parse common number schema attributes with type validation
        """
        parameters = self._parse_base_parameters(data)

        additional_parameters = {
            "example": data.get('example'),
            "minimum": data.get('minimum'),
            "maximum": data.get('maximum'),
            "default": data.get('default'),
            "enum": data.get('enum', []),
        }

        assertion_fields = ('example', 'minimum', 'maximum', 'default')

        for key, value in additional_parameters.items():
            if key in assertion_fields:
                assert value is None or isinstance(value, assert_type), f"Invalid number value: {value}"

        for enum_value in additional_parameters['enum']:
            assert isinstance(enum_value, assert_type), f"Invalid number enum value: {enum_value}"

        parameters.update(additional_parameters)

        return parameters

    def int(self, data: dict) -> IntSchema:
        """
        Integer number schema parser method
        """
        parameters = self._parse_common_number_parameters(data, int)

        return IntSchema(**parameters)

    def number(self, data: dict) -> NumberSchema:
        """
        Float number schema parser method
        """
        parameters = self._parse_common_number_parameters(data, float)

        return NumberSchema(**parameters)

    def string(self, data: dict) -> StringSchema:
        """
        Parse string schema with validation
        """
        parameters = self._parse_base_parameters(data)
        schema_parameters = {
            "example": data.get('example'),
            "min_length": data.get('minLength'),
            "max_length": data.get('maxLength'),
            "default": data.get('default'),
            "enum": data.get('enum', []),
        }

        for value in (schema_parameters['example'], schema_parameters['default']):
            assert value is None or isinstance(value, str), f"Invalid string value: {value}"

        for value in (schema_parameters['min_length'], schema_parameters['max_length']):
            assert value is None or isinstance(value, int), f"Invalid string length value: {value}"

        for enum_value in schema_parameters['enum']:
            assert isinstance(enum_value, str), f"Invalid string enum value: {enum_value}"

        parameters.update(schema_parameters)

        return StringSchema(**parameters)

    def bool(self, data: dict) -> BooleanSchema:
        """
        Parse boolean schema with validation
        """
        parameters = self._parse_base_parameters(data)
        schema_parameters = {
            "example": data.get('example'),
            "default": data.get('default'),
        }

        for key, value in schema_parameters.items():
            assert value is None or isinstance(value, bool), f"Invalid '{key}' bool value: {value}"

        parameters.update(schema_parameters)

        return BooleanSchema(**parameters)

    def array(self, data: dict) -> ArraySchema:
        """
        Parse array schema with validation
        """
        parameters = self._parse_base_parameters(data)
        schema_parameters = {
            "min_items": data.get('minItems'),
            "max_items": data.get('maxItems'),
        }

        for key, value in schema_parameters.items():
            assert value is None or isinstance(value, int), f"Invalid array '{key}' value: {value}"

        parameters.update(schema_parameters)

        items_schema: Schema = self.parse(data['items'])

        return ArraySchema(items_schema, **parameters)

    def object(self, data: dict) -> ObjectSchema:
        """
        Parse object schema and set 'required' attribute to inner properties
        """
        parameters = self._parse_base_parameters(data)

        required: List[str] = data.get('required', [])
        property_data_list: dict = data.get('properties', {})

        properties = []

        for property_name, property_schema in property_data_list.items():
            property_schema = self.parse(property_schema)

            property_schema.title = property_name

            if property_name in required:
                property_schema.required = True

            properties.append(property_schema)

        return ObjectSchema(tuple(properties), **parameters)


class ContentParser:
    schema_parser: SchemaParser

    def __init__(self, schema_parser: SchemaParser) -> None:
        self.schema_parser = schema_parser

    def parse(self, content_data: dict) -> Dict['ContentType', 'Content']:
        """
        Parse 'content' section into mapped dictionary
        """
        content_list = dict(
            self._parse_content(type_name, schema_data)
            for type_name, schema_data in content_data.items()
        )

        return content_list

    def _parse_content(self, type_name: str, schema_data: dict) -> Tuple[ContentType, Content]:
        """
        Parse schema section of parsed content
        """
        schema = schema_data['schema']

        content = Content(
            ContentType(type_name),
            self.schema_parser.parse(schema)
        )

        return content.type, content


class OperationParser:
    content_parser: ContentParser

    def __init__(self, content_parser: ContentParser) -> None:
        self.content_parser = content_parser

    def parse_list(self, data_list: dict) -> Tuple[Operation]:
        """
        Parse method to get list of operations
        """
        operations = tuple(
            self.parse(method, data)
            for method, data in data_list.items()
        )

        return operations

    def parse(self, method: str, data: dict) -> Operation:
        """
        Parse operations section including 'parameters', 'responses', 'requestBody', 'tags', etc
        """
        operation_method = OperationMethod(method)
        tags = data.get('tags', [])
        summary = data.get('summary')
        operation_id = data.get('operationId')

        parameters = tuple(
            self._parse_parameter(param_data)
            for param_data in data.get('parameters', [])
        )

        request_body = self._parse_request_body(data)

        responses = tuple(
            self._parse_response(int(response_code), response_data)
            for response_code, response_data in data['responses'].items()
        )

        return Operation(
            operation_method,
            tags,
            summary,
            operation_id,
            parameters,
            request_body,
            responses
        )

    def _parse_parameter(self, param_data: dict) -> Parameter:
        """
        Parse each operation 'parameter' with default values
        """
        schema = self.content_parser.schema_parser.parse(param_data['schema'])

        return Parameter(
            param_data['name'],
            param_data['in'],
            param_data.get('description'),
            param_data.get('required', False),
            param_data.get('deprecated', False),
            param_data.get('allowEmptyValue', False),
            schema,
        )

    def _parse_request_body(self, request_data: dict) -> RequestBody:
        """
        Parse 'requestBody' section if exists
        """
        request_parser = RequestBodyParser(self.content_parser)
        request_body = request_parser.parse(request_data)

        return request_body

    def _parse_response(self, response_code: int, response_data: dict) -> Response:
        """
        Parse 'responses' section with contents and schemas
        """
        description: str = response_data['description']
        content_list = self.content_parser.parse(response_data['content'])

        return Response(response_code, description, content_list)


class RequestBodyParser:
    content_parser: ContentParser

    def __init__(self, content_parser: ContentParser) -> None:
        self.content_parser = content_parser

    def parse(self, operation_data: dict) -> Optional[RequestBody]:
        """
        Parse 'requestBody' schema object with default values (if body exists)
        """
        request_data = operation_data.get('requestBody')

        if request_data is None:
            return None

        description: str = request_data.get('description')
        required: bool = request_data.get('required', False)
        content_list = self.content_parser.parse(request_data['content'])

        return RequestBody(content_list, required, description)


class SpecificationParser(ParserInterface):
    operation_parser: OperationParser

    def __init__(self, operation_parser: OperationParser) -> None:
        self.operation_parser = operation_parser

    def load_specification(self, specification: dict) -> Specification:
        """
        Load resolved Swagger specification dictionary into object
        """
        try:
            return self._build_specification(specification)
        except KeyError as key_error:
            raise ParserException(f"Invalid key name [{key_error}]")
        except AssertionError as assertion_error:
            raise ParserException(f"AssertionError '{assertion_error}'")

    def _build_specification(self, specification_data: dict) -> Specification:
        """
        Parse basic common blocks of Swagger API root document
        """
        version = specification_data['openapi']
        info = self._parse_info(specification_data)
        servers = self._parse_servers(specification_data)
        tags = self._parse_tags(specification_data)
        paths = self._parse_paths(specification_data)

        return Specification(version, info, servers, tags, paths)

    @staticmethod
    def _parse_info(specification_data: dict) -> Info:
        """
        Parse 'info' section attributes
        """
        data: dict = specification_data['info']

        title = data.get('title')
        version = data.get('version')
        description = data.get('description')
        license_item = None
        contact_item = None

        if data.get('license'):
            license_item = License(data['license']['name'])

        if data.get('contact'):
            contact_data = data['contact']
            contact_item = Contact(
                contact_data.get('name'),
                contact_data.get('email')
            )

        return Info(title, version, description, license_item, contact_item)

    @staticmethod
    def _parse_servers(specification_data: dict) -> Tuple[Server]:
        """
        Parse 'servers' section attributes
        """
        return tuple(
            Server(item['url'], item['description'])
            for item in specification_data['servers']
        )

    @staticmethod
    def _parse_tags(specification_data: dict) -> Tuple[Tag]:
        """
        Parse 'tags' section attributes
        """
        return tuple(
            Tag(item['name'], item['description'])
            for item in specification_data['tags']
        )

    def _parse_paths(self, specification_data: dict) -> Tuple[Path]:
        """
        Parse 'paths' section attributes with inner operations, etc
        """
        return tuple(
            Path(url, self.operation_parser.parse_list(operations_data))
            for url, operations_data
            in specification_data['paths'].items()
        )


def parse(uri: str) -> Specification:
    """
    Parse specification document by URL or filepath
    """
    schema_parser = SchemaParser()
    content_parser = ContentParser(schema_parser)
    operation_parser = OperationParser(content_parser)

    parser = SpecificationParser(operation_parser)

    swagger_resolver = prance.ResolvingParser(
        uri,
        backend='openapi-spec-validator',
        strict=False,
        lazy=True
    )

    try:
        swagger_resolver.parse()
    except prance.ValidationError:
        raise ParserException("Swagger specification validation error")

    return parser.load_specification(swagger_resolver.specification)
