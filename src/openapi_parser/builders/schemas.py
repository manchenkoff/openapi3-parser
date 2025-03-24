import logging

from .schema import SchemaFactory
from ..specification import Schema

logger = logging.getLogger(__name__)


class SchemasBuilder:
    schema_factory: SchemaFactory

    def __init__(self, schema_factory: SchemaFactory) -> None:
        self.schema_factory = schema_factory

    def build_collection(self, schemas: dict) -> dict[str, Schema]:
        logger.debug(f"Schemas parsing: {schemas.keys()}")

        return {
            key: self.schema_factory.create(value)
            for key, value in schemas.items()
        }
