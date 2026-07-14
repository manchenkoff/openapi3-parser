"""Tests for Swagger 2.0 normalization."""

import os

from openapi_parser.models.v3_0 import Specification
from openapi_parser.parser import parse


def test_parse_swagger_v2_petstore() -> None:
    """Test full parsing and normalization of Swagger 2.0 petstore."""
    spec = parse("tests/data/swagger_v2.yaml")
    assert isinstance(spec, Specification)
    assert spec.openapi == "3.0.0"  # Normalized to 3.0
    assert spec.info.title == "Swagger Petstore"

    # host + basePath + schemes -> servers
    assert len(spec.servers) == 1
    assert spec.servers[0].url == "http://petstore.swagger.io/v1"

    # definitions -> components.schemas
    assert spec.components is not None
    assert spec.components.schemas is not None
    assert "Pet" in spec.components.schemas
    assert "NewPet" in spec.components.schemas
    assert "Error" in spec.components.schemas

    # body parameter -> requestBody
    post_pets = spec.paths["/pets"].post
    assert post_pets is not None
    assert post_pets.request_body is not None
    assert "application/json" in post_pets.request_body.content
    body_schema = post_pets.request_body.content["application/json"].schema
    assert body_schema is not None
    assert body_schema.ref_name == "#/components/schemas/NewPet"


def test_parse_swagger_v2_formdata() -> None:
    """Test normalization of formData parameters into requestBody."""
    spec_yaml = """
swagger: "2.0"
info:
  title: "Form API"
  version: "1.0.0"
paths:
  /submit:
    post:
      consumes:
        - "application/x-www-form-urlencoded"
      parameters:
        - name: "username"
          in: "formData"
          type: "string"
          required: true
        - name: "password"
          in: "formData"
          type: "string"
      responses:
        "200":
          description: "OK"
"""
    spec = parse(spec_string=spec_yaml)
    post_op = spec.paths["/submit"].post
    assert post_op is not None
    assert post_op.request_body is not None
    content = post_op.request_body.content["application/x-www-form-urlencoded"]
    schema = content.schema
    assert schema is not None
    assert schema.type == "object"
    assert schema.properties is not None
    assert "username" in schema.properties
    assert "password" in schema.properties
    assert schema.required == ["username"]


def test_parse_swagger_v2_file_ref(tmp_path: object) -> None:
    """File $refs in Swagger 2.0 resolve after normalization."""
    schemas_dir = os.path.join(str(tmp_path), "schemas")
    os.makedirs(schemas_dir, exist_ok=True)

    main_spec = """
swagger: "2.0"
info:
  title: "File Ref API"
  version: "1.0.0"
paths:
  /users:
    get:
      responses:
        "200":
          description: "OK"
          schema:
            $ref: "schemas/user.yaml"
"""

    user_spec = """
type: object
properties:
  name:
    $ref: "#/definitions/Name"
definitions:
  Name:
    type: string
"""

    main_path = os.path.join(str(tmp_path), "main.yaml")
    user_path = os.path.join(schemas_dir, "user.yaml")

    with open(main_path, "w") as f:
        f.write(main_spec)
    with open(user_path, "w") as f:
        f.write(user_spec)

    spec = parse(main_path)
    get_op = spec.paths["/users"].get
    assert get_op is not None
    media_type = get_op.responses["200"].content
    assert media_type is not None
    schema = media_type["application/json"].schema
    assert schema is not None
    assert schema.properties is not None
    assert schema.properties["name"].type == "string"
