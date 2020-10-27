import prance

from .builders import InfoBuilder, ServerBuilder, TagBuilder
from .specification import *


class ParserException(Exception):
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
        servers = self.server_builder.build_server_list(data['servers'])
        tags = self.tag_builder.build_tag_list(data['tags'])

        return Specification(
            openapi=version,
            info=info,
            servers=servers,
            tags=tags
        )


def parse(uri: str) -> Specification:
    """
    Parse specification document by URL or filepath
    """
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

    specification = swagger_resolver.specification

    parser = Parser()  # TODO: fix arguments

    return parser.load_specification(specification)
