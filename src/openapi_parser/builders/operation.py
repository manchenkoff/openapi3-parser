from typing import Dict

from . import ExternalDocBuilder, ParameterBuilder, RequestBuilder, ResponseBuilder
from .common import extract_attrs_by_map, PropertyInfoType
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
            "responses": PropertyInfoType(name="responses", type=self._get_response_collection),
            "summary": PropertyInfoType(name="summary", type=str),
            "description": PropertyInfoType(name="description", type=str),
            "operation_id": PropertyInfoType(name="operationId", type=str),
            "external_docs": PropertyInfoType(name="externalDocs", type=self.external_doc_builder.build),
            "request_body": PropertyInfoType(name="requestBody", type=self.request_builder.build),
            "deprecated": PropertyInfoType(name="deprecated", type=None),
            "parameters": PropertyInfoType(name="parameters", type=self.parameter_builder.build_collection),
            "tags": PropertyInfoType(name="tags", type=None),
        }

        attrs = extract_attrs_by_map(data, attrs_map)

        return Operation(**attrs)

    def _get_response_collection(self, data: Dict[int, dict]) -> ResponseCollection:
        return {
            int(http_code): self.response_builder.build(response)
            for http_code, response in data.items()
        }
