import logging
from typing import Dict

from .common import extract_typed_props, PropertyMeta, extract_extension_attributes
from .external_doc import ExternalDocBuilder
from .parameter import ParameterBuilder
from .request import RequestBuilder
from .response import ResponseBuilder
from ..enumeration import OperationMethod
from ..specification import Operation, Response

logger = logging.getLogger(__name__)


class OperationBuilder:
    response_builder: ResponseBuilder
    external_doc_builder: ExternalDocBuilder
    request_builder: RequestBuilder
    parameter_builder: ParameterBuilder

    def __init__(self,
                 response_builder: ResponseBuilder,
                 external_doc_builder: ExternalDocBuilder,
                 request_builder: RequestBuilder,
                 parameter_builder: ParameterBuilder):
        self.response_builder = response_builder
        self.external_doc_builder = external_doc_builder
        self.request_builder = request_builder
        self.parameter_builder = parameter_builder

    def build(self, method: OperationMethod, data: dict) -> Operation:
        logger.info(f"Operation item parsing [method={method.value}, id={data.get('operationId')}]")

        attrs_map = {
            "responses": PropertyMeta(name="responses", cast=self._get_response_list),
            "summary": PropertyMeta(name="summary", cast=str),
            "description": PropertyMeta(name="description", cast=str),
            "operation_id": PropertyMeta(name="operationId", cast=str),
            "external_docs": PropertyMeta(name="externalDocs", cast=self.external_doc_builder.build),
            "request_body": PropertyMeta(name="requestBody", cast=self.request_builder.build),
            "deprecated": PropertyMeta(name="deprecated", cast=None),
            "parameters": PropertyMeta(name="parameters", cast=self.parameter_builder.build_list),
            "tags": PropertyMeta(name="tags", cast=None),
            "security": PropertyMeta(name="security", cast=None),
        }

        attrs = extract_typed_props(data, attrs_map)
        attrs['extensions'] = extract_extension_attributes(data)

        if attrs['extensions']:
            logger.debug(f"Extracted custom properties [{attrs['extensions'].keys()}]")

        attrs['method'] = method

        return Operation(**attrs)

    def _get_response_list(self, data: Dict[int, dict]) -> list[Response]:
        return [
            self.response_builder.build(http_code, response)
            for http_code, response in data.items()
        ]
