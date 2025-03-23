import logging
from typing import Optional  # noqa: F401

from .builders.common import extract_typed_props, PropertyMeta
from .builders.content import ContentBuilder
from .builders.external_doc import ExternalDocBuilder
from .builders.header import HeaderBuilder
from .builders.info import InfoBuilder
from .builders.oauth_flow import OAuthFlowBuilder
from .builders.operation import OperationBuilder
from .builders.parameter import ParameterBuilder
from .builders.path import PathBuilder
from .builders.request import RequestBuilder
from .builders.response import ResponseBuilder
from .builders.schema import SchemaFactory
from .builders.schemas import SchemasBuilder
from .builders.security import SecurityBuilder
from .builders.server import ServerBuilder
from .builders.tag import TagBuilder
from .errors import ParserError
from .resolver import OpenAPIResolver
from .specification import *

logger = logging.getLogger(__name__)


class Parser:
    info_builder: InfoBuilder
    server_builder: ServerBuilder
    tag_builder: TagBuilder
    external_doc_builder: ExternalDocBuilder
    path_builder: PathBuilder
    security_builder: SecurityBuilder
    schemas_builder: SchemasBuilder

    def __init__(self,
                 info_builder: InfoBuilder,
                 server_builder: ServerBuilder,
                 tags_builder: TagBuilder,
                 external_doc_builder: ExternalDocBuilder,
                 path_builder: PathBuilder,
                 security_builder: SecurityBuilder,
                 schemas_builder: SchemasBuilder) -> None:
        self.info_builder = info_builder
        self.server_builder = server_builder
        self.tag_builder = tags_builder
        self.external_doc_builder = external_doc_builder
        self.path_builder = path_builder
        self.security_builder = security_builder
        self.schemas_builder = schemas_builder

    def load_specification(self, data: dict) -> Specification:
        """Load OpenAPI Specification object from a file or a remote URI.

        Args:
            data (dict): Parsed YAML/JSON dictionary of OpenAPI specification

        Returns:
            Specification: Specification object

        Raises:
            ParserError: If OpenAPI schema is invalid
        """

        logger.debug("Building Specification objects")

        try:
            version = data['openapi']
        except KeyError:
            raise ParserError("Invalid OpenAPI version, check 'openapi' property in the document") from None

        attrs_map = {
            "servers": PropertyMeta(name="servers", cast=self.server_builder.build_list),
            "tags": PropertyMeta(name="tags", cast=self.tag_builder.build_list),
            "external_docs": PropertyMeta(name="externalDocs", cast=self.external_doc_builder.build),
            "paths": PropertyMeta(name="paths", cast=self.path_builder.build_list),
            "security": PropertyMeta(name="security", cast=None),
        }

        attrs = extract_typed_props(data, attrs_map)

        attrs["version"] = version
        attrs["info"] = self.info_builder.build(data['info'])

        if data.get('components') and data['components'].get('securitySchemes'):
            attrs["security_schemas"] = self.security_builder.build_collection(data['components']['securitySchemes'])

        if data.get('components') and data['components'].get('schemas'):
            attrs["schemas"] = self.schemas_builder.build_collection(data['components']['schemas'])

        logger.debug("Specification parsed successfully")

        return Specification(**attrs)


def _create_parser(strict_enum: bool = True) -> Parser:
    logger.info("Initializing parser")

    info_builder = InfoBuilder()
    server_builder = ServerBuilder()
    external_doc_builder = ExternalDocBuilder()
    tag_builder = TagBuilder(external_doc_builder)
    schema_factory = SchemaFactory(strict_enum=strict_enum)
    content_builder = ContentBuilder(schema_factory, strict_enum=strict_enum)
    header_builder = HeaderBuilder(schema_factory)
    parameter_builder = ParameterBuilder(schema_factory, content_builder)
    schemas_builder = SchemasBuilder(schema_factory)
    response_builder = ResponseBuilder(content_builder, header_builder)
    request_builder = RequestBuilder(content_builder)
    operation_builder = OperationBuilder(response_builder,
                                         external_doc_builder,
                                         request_builder,
                                         parameter_builder)
    path_builder = PathBuilder(operation_builder, parameter_builder)
    oauth_flow_builder = OAuthFlowBuilder()
    security_builder = SecurityBuilder(oauth_flow_builder)

    return Parser(info_builder,
                  server_builder,
                  tag_builder,
                  external_doc_builder,
                  path_builder,
                  security_builder,
                  schemas_builder)


def parse(
        uri: Optional[str] = None,
        spec_string: Optional[str] = None,
        strict_enum: bool = True
) -> Specification:
    """Parse specification document by URL/filepath or as a string.

    Args:
        uri (str): Path or URL to OpenAPI file
        spec_string (str): OpenAPI specification as a string to parse
        strict_enum (bool): Validate content types and string formats against the
          enums defined in openapi-parser. Note that the OpenAPI specification allows
          for custom values in these properties.
    """
    resolver = OpenAPIResolver(uri, spec_string)
    specification = resolver.resolve()

    parser = _create_parser(strict_enum=strict_enum)

    return parser.load_specification(specification)
