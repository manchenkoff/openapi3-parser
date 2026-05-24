"""Operation builder for API path operations."""

import logging
from typing import Any

from openapi_parser.builders.common import (
    PropertyMeta,
    extract_extension_attributes,
    extract_typed_props,
)
from openapi_parser.builders.external_doc import ExternalDocBuilder
from openapi_parser.builders.parameter import ParameterBuilder
from openapi_parser.builders.request import RequestBuilder
from openapi_parser.builders.response import ResponseBuilder
from openapi_parser.enumeration import OperationMethod
from openapi_parser.logging import log_ctx
from openapi_parser.specification import Operation, Response

logger = logging.getLogger(__name__)


class OperationBuilder:
    """Builds operation objects from raw specification data."""

    _response_builder: ResponseBuilder
    _external_doc_builder: ExternalDocBuilder
    _request_builder: RequestBuilder
    _parameter_builder: ParameterBuilder

    def __init__(
        self,
        response_builder: ResponseBuilder,
        external_doc_builder: ExternalDocBuilder,
        request_builder: RequestBuilder,
        parameter_builder: ParameterBuilder,
    ):
        """Initialize operation builder.

        Args:
            response_builder: Builder for response objects
            external_doc_builder: Builder for external docs
            request_builder: Builder for request bodies
            parameter_builder: Builder for parameters
        """
        self._response_builder = response_builder
        self._external_doc_builder = external_doc_builder
        self._request_builder = request_builder
        self._parameter_builder = parameter_builder

    def build(
        self,
        method: OperationMethod,
        data: dict[str, Any],
    ) -> Operation:
        """Build an Operation from a method and raw data dict."""
        with log_ctx(method.value):
            logger.info(
                f"Operation item parsing [method={method.value}, id={data.get('operationId')}]",
            )

            attrs_map = {
                "summary": PropertyMeta(name="summary", cast=str),
                "description": PropertyMeta(name="description", cast=str),
                "operation_id": PropertyMeta(name="operationId", cast=str),
                "external_docs": PropertyMeta(
                    name="externalDocs",
                    cast=self._external_doc_builder.build,
                ),
                "request_body": PropertyMeta(
                    name="requestBody",
                    cast=self._request_builder.build,
                ),
                "deprecated": PropertyMeta(name="deprecated", cast=bool),
                "parameters": PropertyMeta(
                    name="parameters",
                    cast=self._parameter_builder.build_list,
                ),
                "tags": PropertyMeta(name="tags", cast=list),
                "security": PropertyMeta(name="security", cast=None),
                "callbacks": PropertyMeta(name="callbacks", cast=None),
            }

            attrs = extract_typed_props(data, attrs_map)

            if data.get("responses") is not None:
                attrs["responses"] = self._get_response_list(data["responses"])

            attrs["extensions"] = extract_extension_attributes(data)

            if attrs["extensions"]:
                logger.debug(
                    f"Extracted custom properties [{attrs['extensions'].keys()}]"
                )

            attrs["method"] = method

            return Operation(**attrs)

    def _get_response_list(
        self,
        data: dict[str, dict[str, Any]],
    ) -> list[Response]:
        return [
            self._response_builder.build(http_code, response)
            for http_code, response in data.items()
        ]
