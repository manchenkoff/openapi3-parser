from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .enumeration import *


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
    description: Optional[str]


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
    title: Optional[str]
    type: DataType
    enum: Optional[List[Any]]
    example: Optional[Any]
    description: Optional[str]
    default: Optional[Any]
    nullable: Optional[bool]
    read_only: Optional[bool]
    write_only: Optional[bool]
    deprecated: Optional[bool]
    external_docs: Optional[ExternalDoc]

    # all_of: Any
    # one_of: Any
    # any_of: Any
    # not: Any

    def __post_init__(self):
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
    multiple_of: Optional[int]
    maximum: Optional[int]
    exclusive_maximum: Optional[int]
    minimum: Optional[int]
    exclusive_minimum: Optional[int]
    format: Optional[IntegerFormat]


@dataclass
class Number(Schema):
    """
    {
      "type": "number",
      "format": "float"
    }
    """
    multiple_of: Optional[float]
    maximum: Optional[float]
    exclusive_maximum: Optional[float]
    minimum: Optional[float]
    exclusive_minimum: Optional[float]
    format: Optional[NumberFormat]


@dataclass
class String(Schema):
    """
    {
      "type": "string",
      "format": "email"
    }
    """
    max_length: Optional[int]
    min_length: Optional[int]
    pattern: Optional[str]
    format: Optional[StringFormat]


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
    max_items: Optional[int]
    min_items: Optional[int]
    unique_items: Optional[bool]
    items: Schema


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
    max_properties: Optional[int]
    min_properties: Optional[int]
    required: List[str] = field(default_factory=list)
    properties: List[Property] = field(default_factory=list)
    # additional_properties: Optional[Union[bool, Schema]] = field(default=True)


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
    location: str
    required: bool
    schema: Schema
    description: Optional[str]
    # example: Optional[Any]
    # examples: List[Any] = field(default_factory=list)
    deprecated: Optional[bool] = field(default=False)
    # style: str
    # explode: bool
    # allow_reserved: bool


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
    # example: Optional[Any]
    # examples: List[Any] = field(default_factory=list)
    # encoding: Dict[str, Encoding]


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
    content: Dict[MediaType, Content]
    description: Optional[str]
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
    required: bool
    schema: Schema
    description: Optional[str]
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
    content: Dict[MediaType, Content]
    headers: Dict[str, Header] = field(default_factory=dict)
    # links: Dict[str, Link]


@dataclass
class Security:
    """
    {
      "type": "apiKey",
      "name": "api_key",
      "in": "header",
      "description": "authorization key to communicate with API"
    }
    """
    type: SecurityType
    description: Optional[str]


@dataclass
class ApiKeySecurity(Security):
    """
    {
      "type": "apiKey",
      "name": "api_key",
      "in": "header"
    }
    """
    name: str
    location: BaseLocation


@dataclass
class HttpSecurity(Security):
    """
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
    """
    scheme: AuthenticationScheme
    bearer_format: Optional[str]


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
    refresh_url: Optional[str]
    authorization_url: Optional[str]
    token_url: Optional[str]
    scopes: Dict[str, str] = field(default_factory=dict)


@dataclass
class OAuth2Security(Security):
    """
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
    """
    flows: Dict[OAuthFlowType, OAuthFlow]


@dataclass
class OpenIdConnectSecurity(Security):
    """
    {
        "openIdConnect": {
          "openIdConnectUrl": "https://example.com/api/openid",
        }
    }
    """
    url: str


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
    summary: Optional[str]
    description: Optional[str]
    external_docs: Optional[ExternalDoc]
    operation_id: Optional[str]
    request_body: Optional[RequestBody]
    deprecated: Optional[bool] = field(default=False)
    responses: Dict[int, Response] = field(default_factory=dict)
    parameters: List[Parameter] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    security: List[Security] = field(default_factory=list)
    # callbacks: Dict[str, Callback] = field(default_factory=dict)


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
    summary: Optional[str]
    description: Optional[str]
    operations: Dict[OperationMethod, Operation] = field(default_factory=dict)
    parameters: List[Parameter] = field(default_factory=list)


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
    description: Optional[str]
    external_docs: Optional[ExternalDoc]


@dataclass
class Specification:
    openapi: str
    info: Info
    servers: List[Server] = field(default_factory=list)
    paths: List[Path] = field(default_factory=list)
    security: List[Security] = field(default_factory=list)
    tags: List[Tag] = field(default_factory=list)
    external_docs: List[ExternalDoc] = field(default_factory=list)
