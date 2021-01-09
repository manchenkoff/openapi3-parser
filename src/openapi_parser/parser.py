from .builders import *
from .builders.common import extract_typed_props, PropertyMeta
from .errors import ParserError
from .resolver import OpenAPIResolver
from .specification import *


class Parser:
    info_builder: InfoBuilder
    server_builder: ServerBuilder
    tag_builder: TagBuilder
    external_doc_builder: ExternalDocBuilder
    path_builder: PathBuilder
    security_builder: SecurityBuilder

    def __init__(self,
                 info_builder: InfoBuilder,
                 server_builder: ServerBuilder,
                 tags_builder: TagBuilder,
                 external_doc_builder: ExternalDocBuilder,
                 path_builder: PathBuilder,
                 security_builder: SecurityBuilder) -> None:
        self.info_builder = info_builder
        self.server_builder = server_builder
        self.tag_builder = tags_builder
        self.external_doc_builder = external_doc_builder
        self.path_builder = path_builder
        self.security_builder = security_builder

    def load_specification(self, data: dict) -> Specification:
        """
        Load OpenAPI Specification object from a file or a remote URI.
        :param data: JSON (dict) of specification data
        :return: Specification object
        """

        try:
            version = data['openapi']
        except KeyError:
            raise ParserError("Invalid OpenAPI schema version")

        attrs_map = {
            "servers": PropertyMeta(name="servers", cast=self.server_builder.build_list),
            "tags": PropertyMeta(name="tags", cast=self.tag_builder.build_list),
            "external_docs": PropertyMeta(name="externalDocs", cast=self.external_doc_builder.build),
            "paths": PropertyMeta(name="paths", cast=self.path_builder.build_collection),
            "security": PropertyMeta(name="security", cast=None),
        }

        attrs = extract_typed_props(data, attrs_map)

        attrs["version"] = version
        attrs["info"] = self.info_builder.build(data['info'])

        if data.get('components') and data['components'].get('securitySchemes'):
            attrs["security_schemas"] = self.security_builder.build_collection(data['components']['securitySchemes'])

        return Specification(**attrs)


def _create_parser() -> Parser:
    info_builder = InfoBuilder()
    server_builder = ServerBuilder()
    external_doc_builder = ExternalDocBuilder()
    tag_builder = TagBuilder(external_doc_builder)
    schema_factory = SchemaFactory()
    content_builder = ContentBuilder(schema_factory)
    header_builder = HeaderBuilder(schema_factory)
    parameter_builder = ParameterBuilder(schema_factory)
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
                  security_builder)


def parse(uri: str) -> Specification:
    """
    Parse specification document by URL or filepath
    """
    resolver = OpenAPIResolver(uri)
    specification = resolver.resolve()

    parser = _create_parser()

    return parser.load_specification(specification)
