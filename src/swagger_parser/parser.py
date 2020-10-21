import prance

from .specification import Specification


class ParserException(Exception):
    """
    Base parser exception class.
    Throws when any error occurs.
    """
    pass


class Parser:
    def load_specification(self, data: dict) -> Specification:
        """
        Load Swagger Specification object from a file or a remote URI.
        :param data: JSON (dict) of specification data
        :return: Specification object
        """
        pass


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

    parser = Parser()

    return parser.load_specification(specification)
