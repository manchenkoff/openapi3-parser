from .builders import *
from openapi_parser.builders.schema import SchemaFactory
from .resolver import OpenAPIResolver
from .specification import *


class Parser:
    info_builder: InfoBuilder
    server_builder: ServerBuilder
    tag_builder: TagBuilder

    def __init__(self,
                 info_builder: InfoBuilder,
                 server_builder: ServerBuilder,
                 tags_builder: TagBuilder) -> None:
        self.info_builder = info_builder
        self.server_builder = server_builder
        self.tag_builder = tags_builder

    def load_specification(self, data: dict) -> Specification:
        """
        Load OpenAPI Specification object from a file or a remote URI.
        :param data: JSON (dict) of specification data
        :return: Specification object
        """

        version = data['openapi']

        info = self.info_builder.build(data['info'])
        servers = self.server_builder.build_list(data.get('servers', []))
        tags = self.tag_builder.build_list(data.get('tags', []))

        return Specification(
            openapi=version,
            info=info,
            servers=servers,
            tags=tags,
        )


def _create_parser() -> Parser:
    info_builder = InfoBuilder()
    server_builder = ServerBuilder()
    external_doc_builder = ExternalDocBuilder()
    tag_builder = TagBuilder(external_doc_builder)
    schema_factory = SchemaFactory()

    return Parser(info_builder,
                  server_builder,
                  tag_builder)


def parse(uri: str) -> Specification:
    """
    Parse specification document by URL or filepath
    """
    resolver = OpenAPIResolver(uri)
    specification = resolver.resolve()

    parser = _create_parser()

    return parser.load_specification(specification)
