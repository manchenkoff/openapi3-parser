from typing import Dict

from . import ExternalDocBuilder, ParameterBuilder, RequestBuilder, ResponseBuilder
from .common import extract_typed_props, PropertyMeta
from ..specification import Operation, ResponseCollection


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

    def build(self, data: dict) -> Operation:
        attrs_map = {
            "responses": PropertyMeta(name="responses", cast=self._get_response_collection),
            "summary": PropertyMeta(name="summary", cast=str),
            "description": PropertyMeta(name="description", cast=str),
            "operation_id": PropertyMeta(name="operationId", cast=str),
            "external_docs": PropertyMeta(name="externalDocs", cast=self.external_doc_builder.build),
            "request_body": PropertyMeta(name="requestBody", cast=self.request_builder.build),
            "deprecated": PropertyMeta(name="deprecated", cast=None),
            "parameters": PropertyMeta(name="parameters", cast=self.parameter_builder.build_collection),
            "tags": PropertyMeta(name="tags", cast=None),
            "security": PropertyMeta(name="security", cast=None),
        }

        attrs = extract_typed_props(data, attrs_map)

        return Operation(**attrs)

    def _get_response_collection(self, data: Dict[int, dict]) -> ResponseCollection:
        return {
            int(http_code): self.response_builder.build(response)
            for http_code, response in data.items()
        }
