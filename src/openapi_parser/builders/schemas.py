"""Component schemas builder."""

import logging
from typing import Any

from openapi_parser.builders.schema import SchemaFactory
from openapi_parser.specification import Schema

logger = logging.getLogger(__name__)


class SchemasBuilder:
    """Builds a collection of named schemas from component definitions."""

    _schema_factory: SchemaFactory

    def __init__(self, schema_factory: SchemaFactory) -> None:
        """Initialize schemas builder.

        Args:
            schema_factory: Factory for creating schema objects
        """
        self._schema_factory = schema_factory

    def build_collection(self, schemas: dict[str, Any]) -> dict[str, Schema]:
        """Build a dict of named Schema objects."""
        logger.debug(f"Schemas parsing: {schemas.keys()}")

        return {
            key: self._schema_factory.create(value) for key, value in schemas.items()
        }
