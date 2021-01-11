from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .enumeration import *

PropertyList = List['Property']
ContentType = Dict[MediaType, 'Content']
HeaderCollection = Dict[str, 'Header']
ResponseCollection = Dict[int, 'Response']
SecurityCollection = Dict[str, 'Security']
SecurityList = List[Dict[str, Any]]
OperationCollection = Dict[OperationMethod, 'Operation']
ParameterList = List['Parameter']
ServerList = List['Server']
TagList = List['Tag']
PathList = List['Path']


@dataclass
class Contact:
    """
    {
      "name": "API Support",
      "url": "http://www.example.com/support",
      "email": "support@example.com"
    }
    """
    name: Optional[str] = None
    url: Optional[str] = None
    email: Optional[str] = None


@dataclass
class License:
    """
    {
      "name": "Apache 2.0",
      "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
    }
    """
    name: str
    url: Optional[str] = None


@dataclass
class Info:
    """
    {
      "title": "Sample Pet Store App",
      "description": "This is a sample server for a pet store.",
      "termsOfService": "http://example.com/terms/",
      "contact": {
        "name": "API Support",
        "url": "http://www.example.com/support",
        "email": "support@example.com"
      },
      "license": {
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
      },
      "version": "1.0.1"
    }
    """
    title: str
    version: str
    description: Optional[str] = None
    terms_of_service: Optional[str] = None
    contact: Optional[Contact] = None
    license: Optional[License] = None


@dataclass
class Server:
    """
    {
      "servers": [
        {
          "url": "https://development.gigantic-server.com/v1",
          "description": "Development server"
        },
        {
          "url": "https://staging.gigantic-server.com/v1",
          "description": "Staging server"
        },
        {
          "url": "https://api.gigantic-server.com/v1",
          "description": "Production server"
        }
      ]
    }
    """
    url: str
    description: Optional[str] = None
    variables: Optional[dict] = field(default_factory=dict)


@dataclass
class ExternalDoc:
    """
    {
      "description": "Find more info here",
      "url": "https://example.com"
    }
    """
    url: str
    description: Optional[str] = None


@dataclass
class Schema:
    """
    {
      "type": "object",
      "required": [
        "name"
      ],
      "properties": {
        "name": {
          "type": "string"
        },
        "address": {
          "$ref": "#/components/schemas/Address"
        },
        "age": {
          "type": "integer",
          "format": "int32",
          "minimum": 0
        }
      }
    }
    """
    type: DataType
    title: Optional[str] = None
    enum: Optional[List[Any]] = None
    example: Optional[Any] = None
    description: Optional[str] = None
    default: Optional[Any] = None
    nullable: Optional[bool] = None
    read_only: Optional[bool] = None
    write_only: Optional[bool] = None
    deprecated: Optional[bool] = None
    extensions: Optional[dict] = field(default_factory=dict)

    # all_of: Any  # TODO
    # one_of: Any  # TODO
    # any_of: Any  # TODO
    # not: Any  # TODO

    def __post_init__(self) -> None:
        """
        Fix to load default values in inherited classes
        """
        if self.enum is None:
            self.enum = []
        if self.nullable is None:
            self.nullable = False
        if self.read_only is None:
            self.read_only = False
        if self.write_only is None:
            self.write_only = False
        if self.deprecated is None:
            self.deprecated = False


@dataclass
class Integer(Schema):
    """
    {
      "type": "integer",
      "format": "int32"
    }
    """
    multiple_of: Optional[int] = None
    maximum: Optional[int] = None
    exclusive_maximum: Optional[int] = None
    minimum: Optional[int] = None
    exclusive_minimum: Optional[int] = None
    format: Optional[IntegerFormat] = None


@dataclass
class Number(Schema):
    """
    {
      "type": "number",
      "format": "float"
    }
    """
    multiple_of: Optional[float] = None
    maximum: Optional[float] = None
    exclusive_maximum: Optional[float] = None
    minimum: Optional[float] = None
    exclusive_minimum: Optional[float] = None
    format: Optional[NumberFormat] = None


@dataclass
class String(Schema):
    """
    {
      "type": "string",
      "format": "email"
    }
    """
    max_length: Optional[int] = None
    min_length: Optional[int] = None
    pattern: Optional[str] = None
    format: Optional[StringFormat] = None


@dataclass
class Boolean(Schema):
    """
    {
      "type": "boolean",
    }
    """


@dataclass
class Array(Schema):
    """
    {
      "animals": {
        "type": "array",
        "items": {
          "type": "string",
        }
      }
    }
    """
    max_items: Optional[int] = None
    min_items: Optional[int] = None
    unique_items: Optional[bool] = None
    items: Schema = None  # type: ignore


@dataclass
class Property:
    """
    {
        "name": {
          "type": "string"
        }
    }
    """
    name: str
    schema: Schema


@dataclass
class Object(Schema):
    """
    {
      "type": "object",
      "required": [
        "name"
      ],
      "properties": {
        "name": {
          "type": "string"
        },
        "age": {
          "type": "integer",
          "format": "int32",
          "minimum": 0
        }
      }
    }
    """
    max_properties: Optional[int] = None
    min_properties: Optional[int] = None
    required: List[str] = field(default_factory=list)
    properties: PropertyList = field(default_factory=list)
    # additional_properties: Optional[Union[bool, Schema]] = field(default=True)  # TODO


@dataclass
class Parameter:
    """
    {
      "name": "token",
      "in": "header",
      "description": "token to be passed as a header",
      "required": true,
      "schema": {
        "type": "array",
        "items": {
          "type": "integer",
          "format": "int64"
        }
      },
      "style": "simple"
    }
    OR
    {
      "name": "username",
      "in": "path",
      "description": "username to fetch",
      "required": true,
      "schema": {
        "type": "string"
      }
    }
    OR
    {
      "name": "id",
      "in": "query",
      "description": "ID of the object to fetch",
      "required": false,
      "schema": {
        "type": "array",
        "items": {
          "type": "string"
        }
      },
      "style": "form",
      "explode": true
    }
    """
    name: str
    location: ParameterLocation
    required: bool
    schema: Schema
    description: Optional[str] = None
    # example: Optional[Any]  # TODO
    # examples: List[Any] = field(default_factory=list)  # TODO
    deprecated: Optional[bool] = field(default=False)
    # style: str  # TODO
    # explode: bool  # TODO
    # allow_reserved: bool  # TODO


@dataclass
class Content:
    """
    {
      "application/json": {
        "schema": {
             "$ref": "#/components/schemas/Pet"
        },
        "examples": {
          "cat" : {
            "summary": "An example of a cat",
            "value":
              {
                "name": "Fluffy",
                "petType": "Cat",
                "color": "White",
                "gender": "male",
                "breed": "Persian"
              }
          },
          "dog": {
            "summary": "An example of a dog with a cat's name",
            "value" :  {
              "name": "Puma",
              "petType": "Dog",
              "color": "Black",
              "gender": "Female",
              "breed": "Mixed"
            },
          "frog": {
              "$ref": "#/components/examples/frog-example"
            }
          }
        }
      }
    }
    """
    schema: Schema
    # example: Optional[Any]  # TODO
    # examples: List[Any] = field(default_factory=list)  # TODO
    # encoding: Dict[str, Encoding]  # TODO


@dataclass
class RequestBody:
    """
    {
      "description": "user to add to the system",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/User"
          },
          "examples": {
              "user" : {
                "summary": "User Example",
                "externalValue": "http://foo.bar/examples/user-example.json"
              }
            }
        },
        "*/*": {
          "examples": {
            "user" : {
                "summary": "User example in other format",
                "externalValue": "http://foo.bar/examples/user-example.whatever"
            }
          }
        }
      }
    }
    """
    content: ContentType
    description: Optional[str] = None
    required: Optional[bool] = field(default=False)


@dataclass
class Header:
    """
    {
      "description": "The number of allowed requests in the current period",
      "schema": {
        "type": "integer"
      }
    }
    """
    schema: Schema
    description: Optional[str] = None
    required: Optional[bool] = field(default=False)
    deprecated: Optional[bool] = field(default=False)


@dataclass
class Response:
    """
    {
      "description": "A complex object array response",
      "content": {
        "application/json": {
          "schema": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/VeryComplexType"
            }
          }
        }
      },
      "headers": {
        "X-Rate-Limit-Limit": {
          "description": "The number of allowed requests in the current period",
          "schema": {
            "type": "integer"
          }
        }
      }
    }
    """
    description: str
    content: Optional[ContentType] = None
    headers: HeaderCollection = field(default_factory=dict)
    # links: Dict[str, Link]  # TODO


@dataclass
class OAuthFlow:
    """
    {
        "implicit": {
          "authorizationUrl": "https://example.com/api/oauth/dialog",
          "scopes": {
            "write:pets": "modify pets in your account",
            "read:pets": "read your pets"
          }
        }
    }
    """
    refresh_url: Optional[str] = None
    authorization_url: Optional[str] = None
    token_url: Optional[str] = None
    scopes: Dict[str, str] = field(default_factory=dict)


@dataclass
class Security:
    """
    {
      "type": "apiKey",
      "name": "api_key",
      "in": "header",
      "description": "authorization key to communicate with API"
    }
    OR
    {
      "type": "http",
      "scheme": "basic"
    }
    OR
    {
      "type": "http",
      "scheme": "bearer",
      "bearerFormat": "JWT",
    }
    OR
    {
      "type": "oauth2",
      "flows": {
        "implicit": {
          "authorizationUrl": "https://example.com/api/oauth/dialog",
          "scopes": {
            "write:pets": "modify pets in your account",
            "read:pets": "read your pets"
          }
        },
        "authorizationCode": {
          "authorizationUrl": "https://example.com/api/oauth/dialog",
          "tokenUrl": "https://example.com/api/oauth/token",
          "scopes": {
            "write:pets": "modify pets in your account",
            "read:pets": "read your pets"
          }
        }
      }
    }
    OR
    {
      "type": "openIdConnect",
      "openIdConnectUrl": "https://example.com/api/openid",
    }
    """
    type: SecurityType
    location: Optional[BaseLocation] = None
    description: Optional[str] = None
    name: Optional[str] = None
    scheme: Optional[AuthenticationScheme] = None
    bearer_format: Optional[str] = None
    flows: Dict[OAuthFlowType, OAuthFlow] = field(default_factory=dict)
    url: Optional[str] = None


@dataclass
class Operation:
    """
    {
      "tags": [
        "pet"
      ],
      "summary": "Updates a pet in the store with form data",
      "operationId": "updatePetWithForm",
      "parameters": [
        {
          "name": "petId",
          "in": "path",
          "description": "ID of pet that needs to be updated",
          "required": true,
          "schema": {
            "type": "string"
          }
        }
      ],
      "requestBody": {
        "content": {
          "application/x-www-form-urlencoded": {
            "schema": {
              "type": "object",
              "properties": {
                "name": {
                  "description": "Updated name of the pet",
                  "type": "string"
                },
                "status": {
                  "description": "Updated status of the pet",
                  "type": "string"
                }
              },
              "required": ["status"]
            }
          }
        }
      },
      "responses": {
        "200": {
          "description": "Pet updated.",
          "content": {
            "application/json": {},
            "application/xml": {}
          }
        },
        "405": {
          "description": "Method Not Allowed",
          "content": {
            "application/json": {},
            "application/xml": {}
          }
        }
      },
      "security": [
        {
          "pet_store_auth": [
            "write:pets",
            "read:pets"
          ]
        }
      ]
    }
    """
    responses: ResponseCollection
    summary: Optional[str] = None
    description: Optional[str] = None
    operation_id: Optional[str] = None
    external_docs: Optional[ExternalDoc] = None
    request_body: Optional[RequestBody] = None
    deprecated: Optional[bool] = field(default=False)
    parameters: ParameterList = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    security: SecurityList = field(default_factory=list)
    # callbacks: Dict[str, Callback] = field(default_factory=dict)  # TODO


@dataclass
class PathItem:
    """
    {
      "get": {
        "description": "Returns pets based on ID",
        "summary": "Find pets by ID",
        "operationId": "getPetsById",
        "responses": {
          "200": {
            "description": "pet response",
            "content": {
              "*/*": {
                "schema": {
                  "type": "array",
                  "items": {
                    "$ref": "#/components/schemas/Pet"
                  }
                }
              }
            }
          },
          "default": {
            "description": "error payload",
            "content": {
              "text/html": {
                "schema": {
                  "$ref": "#/components/schemas/ErrorModel"
                }
              }
            }
          }
        }
      },
      "parameters": [
        {
          "name": "id",
          "in": "path",
          "description": "ID of pet to use",
          "required": true,
          "schema": {
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "style": "simple"
        }
      ]
    }
    """
    summary: Optional[str] = None
    description: Optional[str] = None
    operations: OperationCollection = field(default_factory=dict)
    parameters: ParameterList = field(default_factory=list)


@dataclass
class Path:
    """
    {
      "/pets": {
        "get": {
          "description": "Returns all pets from the system that the user has access to",
          "responses": {
            "200": {
              "description": "A list of pets.",
              "content": {
                "application/json": {
                  "schema": {
                    "type": "array",
                    "items": {
                      "$ref": "#/components/schemas/pet"
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
    """
    pattern: str
    item: PathItem


@dataclass
class Tag:
    """
    {
        "name": "pet",
        "description": "Pets operations"
    }
    """
    name: str
    description: Optional[str] = None
    external_docs: Optional[ExternalDoc] = None


@dataclass
class Specification:
    version: str
    info: Info
    servers: ServerList = field(default_factory=list)
    tags: TagList = field(default_factory=list)
    security_schemas: SecurityCollection = field(default_factory=dict)
    security: SecurityList = field(default_factory=list)
    external_docs: Optional[ExternalDoc] = None
    paths: PathList = field(default_factory=list)
