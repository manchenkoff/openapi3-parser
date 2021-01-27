import logging

from . import SchemaFactory
from .common import extract_typed_props, PropertyMeta
from ..specification import Header

logger = logging.getLogger(__name__)


class HeaderBuilder:
    schema_factory: SchemaFactory

    def __init__(self, schema_factory: SchemaFactory) -> None:
        self.schema_factory = schema_factory

    def build_list(self, data: dict) -> list[Header]:
        return [
            self._build(header_name, header_value)
            for header_name, header_value
            in data.items()
        ]

    def _build(self, name: str, data: dict) -> Header:
        logger.debug(f"Header parsing: {name}")

        attrs_map = {
            "schema": PropertyMeta(name="schema", cast=self.schema_factory.create),
            "description": PropertyMeta(name="description", cast=str),
            "deprecated": PropertyMeta(name="deprecated", cast=None),
            "required": PropertyMeta(name="required", cast=None),
        }

        attrs = extract_typed_props(data, attrs_map)

        attrs['name'] = name

        return Header(**attrs)
