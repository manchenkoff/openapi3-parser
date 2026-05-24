"""OpenAPI specification parser entry point."""

import logging
from typing import Any

from openapi_parser.builders.common import PropertyMeta, extract_typed_props
from openapi_parser.builders.content import ContentBuilder
from openapi_parser.builders.encoding import EncodingBuilder
from openapi_parser.builders.external_doc import ExternalDocBuilder
from openapi_parser.builders.header import HeaderBuilder
from openapi_parser.builders.info import InfoBuilder
from openapi_parser.builders.link import LinkBuilder
from openapi_parser.builders.oauth_flow import OAuthFlowBuilder
from openapi_parser.builders.operation import OperationBuilder
from openapi_parser.builders.parameter import ParameterBuilder
from openapi_parser.builders.path import PathBuilder
from openapi_parser.builders.request import RequestBuilder
from openapi_parser.builders.response import ResponseBuilder
from openapi_parser.builders.schema import SchemaFactory
from openapi_parser.builders.schemas import SchemasBuilder
from openapi_parser.builders.security import SecurityBuilder
from openapi_parser.builders.server import ServerBuilder
from openapi_parser.builders.tag import TagBuilder
from openapi_parser.errors import ParserError
from openapi_parser.logging import log_ctx
from openapi_parser.resolver import OpenAPIResolver
from openapi_parser.specification import Specification

logger = logging.getLogger(__name__)


class Parser:
    """Builds Specification objects from parsed OpenAPI data."""

    info_builder: InfoBuilder
    server_builder: ServerBuilder
    tag_builder: TagBuilder
    external_doc_builder: ExternalDocBuilder
    path_builder: PathBuilder
    security_builder: SecurityBuilder
    schemas_builder: SchemasBuilder

    def __init__(
        self,
        info_builder: InfoBuilder,
        server_builder: ServerBuilder,
        tag_builder: TagBuilder,
        external_doc_builder: ExternalDocBuilder,
        path_builder: PathBuilder,
        security_builder: SecurityBuilder,
        schemas_builder: SchemasBuilder,
    ) -> None:
        """Initialize parser with specialized builders.

        Args:
            info_builder: Builder for info metadata
            server_builder: Builder for server definitions
            tag_builder: Builder for tag definitions
            external_doc_builder: Builder for external docs
            path_builder: Builder for path definitions
            security_builder: Builder for security schemes
            schemas_builder: Builder for component schemas
        """
        self.info_builder = info_builder
        self.server_builder = server_builder
        self.tag_builder = tag_builder
        self.external_doc_builder = external_doc_builder
        self.path_builder = path_builder
        self.security_builder = security_builder
        self.schemas_builder = schemas_builder

    def load_specification(self, data: dict[str, Any]) -> Specification:
        """Load OpenAPI Specification object from a file or a remote URI.

        Args:
            data (dict): Parsed YAML/JSON dictionary of OpenAPI specification

        Returns:
            Specification: Specification object

        Raises:
            ParserError: If OpenAPI schema is invalid
        """
        with log_ctx("spec"):
            logger.debug("Building Specification objects")

            try:
                version = data["openapi"]
            except KeyError:
                raise ParserError(
                    "Invalid OpenAPI version, check 'openapi' property in the document",
                ) from None

            attrs_map = {
                "servers": PropertyMeta(
                    name="servers",
                    cast=self.server_builder.build_list,
                ),
                "tags": PropertyMeta(
                    name="tags",
                    cast=self.tag_builder.build_list,
                ),
                "external_docs": PropertyMeta(
                    name="externalDocs",
                    cast=self.external_doc_builder.build,
                ),
                "paths": PropertyMeta(
                    name="paths",
                    cast=self.path_builder.build_list,
                ),
                "security": PropertyMeta(name="security", cast=None),
            }

            attrs = extract_typed_props(data, attrs_map)

            attrs["version"] = version

            info_data = data.get("info")

            if info_data is None:
                raise ParserError(
                    "OpenAPI document is missing required 'info' property"
                )

            attrs["info"] = self.info_builder.build(info_data)

            components = data.get("components") or {}

            if "securitySchemes" in components:
                attrs["security_schemas"] = self.security_builder.build_collection(
                    components["securitySchemes"],
                )

            if "schemas" in components:
                attrs["schemas"] = self.schemas_builder.build_collection(
                    components["schemas"],
                )

            logger.debug("Specification parsed successfully")

            return Specification(**attrs)


def _create_parser(strict_enum: bool = True) -> Parser:
    logger.info("Initializing parser")

    info_builder = InfoBuilder()
    server_builder = ServerBuilder()
    external_doc_builder = ExternalDocBuilder()
    tag_builder = TagBuilder(external_doc_builder)
    schema_factory = SchemaFactory(strict_enum=strict_enum)
    header_builder = HeaderBuilder(schema_factory)
    encoding_builder = EncodingBuilder(header_builder)
    content_builder = ContentBuilder(
        schema_factory,
        encoding_builder,
        strict_enum=strict_enum,
    )
    parameter_builder = ParameterBuilder(schema_factory, content_builder)
    schemas_builder = SchemasBuilder(schema_factory)
    link_builder = LinkBuilder()
    response_builder = ResponseBuilder(content_builder, header_builder, link_builder)
    request_builder = RequestBuilder(content_builder)
    operation_builder = OperationBuilder(
        response_builder,
        external_doc_builder,
        request_builder,
        parameter_builder,
    )
    path_builder = PathBuilder(operation_builder, parameter_builder)
    oauth_flow_builder = OAuthFlowBuilder()
    security_builder = SecurityBuilder(oauth_flow_builder)

    return Parser(
        info_builder,
        server_builder,
        tag_builder,
        external_doc_builder,
        path_builder,
        security_builder,
        schemas_builder,
    )


def parse(
    uri: str | None = None,
    spec_string: str | None = None,
    strict_enum: bool = True,
    recursion_limit: int = 1,
) -> Specification:
    """Parse specification document by URL/filepath or as a string.

    Args:
        uri (str): Path or URL to OpenAPI file
        spec_string (str): OpenAPI specification as a string to parse
        strict_enum (bool): Validate content types and string formats against the
          enums defined in openapi-parser. Note that the OpenAPI specification allows
          for custom values in these properties.
        recursion_limit (int): Maximum recursion depth for resolving references
    """
    resolver = OpenAPIResolver(uri, spec_string, recursion_limit=recursion_limit)
    specification = resolver.resolve()

    parser = _create_parser(strict_enum=strict_enum)

    return parser.load_specification(specification)
