import prance

from .builders import *
from .resolver import SwaggerResolver
from .specification import *


class ParserError(Exception):
    """
    Base parser exception class.
    Throws when any error occurs.
    """
    pass


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
        Load Swagger Specification object from a file or a remote URI.
        :param data: JSON (dict) of specification data
        :return: Specification object
        """

        version = data['openapi']

        info = self.info_builder.build(data['info'])
        servers = self.server_builder.build_list(data['servers'])
        tags = self.tag_builder.build_list(data['tags'])

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

    return Parser(info_builder,
                  server_builder,
                  tag_builder)


def parse(uri: str) -> Specification:
    """
    Parse specification document by URL or filepath
    """

    swagger_resolver = SwaggerResolver(uri)

    swagger_resolver = prance.ResolvingParser(
        uri,
        backend='openapi-spec-validator',
        strict=False,
        lazy=True
    )

    try:
        swagger_resolver.parse()
    except prance.ValidationError:
        raise ParserError("Swagger specification validation error")

    specification = swagger_resolver.specification

    parser = _create_parser()

    return parser.load_specification(specification)
