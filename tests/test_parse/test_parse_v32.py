"""Tests for full OpenAPI 3.2 spec parsing.

Exercises 3.2-specific features: jsonSchemaDialect, webhooks, array type syntax.
"""

import os

from openapi_parser.enumeration import (
    ApiKeyLocation,
    DataType,
    ParameterLocation,
    QueryParameterStyle,
    SecurityType,
)
from openapi_parser.models.base import (
    Contact,
    Discriminator,
    ExternalDoc,
    Info,
    License,
    Link,
    Server,
    ServerVariable,
)
from openapi_parser.models.v3_0 import (
    SecurityScheme,
)
from openapi_parser.models.v3_0 import (
    Specification as SpecificationV3_0,
)
from openapi_parser.models.v3_1 import (
    Callback,
    Components,
    Encoding,
    MediaType,
    Operation,
    Parameter,
    PathItem,
    RequestBody,
    Response,
    Schema,
    Specification,
    Tag,
)

FIXTURE = os.path.join(os.path.dirname(__file__), "..", "data", "openapi_3.2.yaml")


_UUID_SCHEMA = Schema(
    type=DataType.OBJECT,
    additionalProperties=False,
    required=["uuid"],
    properties={
        "uuid": Schema(
            type=DataType.STRING,
            format="uuid",
            example="12345678-1234-5678-1234-567812345678",
            description="Unique object id",
        ),
    },
)

_USER_ALLOF = [
    _UUID_SCHEMA,
    Schema(required=["login", "email", "avatar"]),
    Schema(
        properties={
            "login": Schema(
                type=DataType.STRING,
                example="super-admin",
                description="User login or nickname",
            ),
            "email": Schema(
                type=DataType.STRING,
                format="email",
                example="user@mail.com",
                description="User E-mail address",
            ),
            "avatar": Schema(
                type=DataType.STRING,
                format="uri",
                example="https://github.com/manchenkoff/openapi3-parser",
                description="User Avatar URL",
            ),
        },
    ),
]


def _break_circular_refs(spec: SpecificationV3_0) -> None:
    """Break Equipment↔Feature circular reference for model_dump compatibility."""
    components = spec.components
    assert components is not None
    schemas = components.schemas
    assert schemas is not None
    if "Equipment" in schemas and "Feature" in schemas:
        fe = schemas["Feature"]
        assert fe.properties is not None
        fe.properties["Equipments"].items = Schema.model_construct()


def _strip_ref_name(d: object) -> object:
    """Recursively remove ref_name keys from model_dump output."""
    if isinstance(d, dict):
        return {k: _strip_ref_name(v) for k, v in d.items() if k != "ref_name"}
    if isinstance(d, list):
        return [_strip_ref_name(v) for v in d]
    return d


def test_openapi_3_2_full() -> None:
    from openapi_parser.parser import parse

    spec = parse(FIXTURE)
    expected = Specification(
        openapi="3.2.0",
        jsonSchemaDialect="https://json-schema.org/draft/2020-12/schema",
        security=[{"Basic": []}],
        info=Info(
            title="User example service",
            version="1.0.0",
            description="Example service specification to work with user storage",
            license=License(name="MIT"),
            contact=Contact(
                name="manchenkoff",
                email="artyom@manchenkoff.me",
            ),
        ),
        externalDocs=ExternalDoc(
            description="Find more info here",
            url="https://example.com/docs",
        ),
        servers=[
            Server(
                url="https://users.app/api/v{version}",
                description="production",
                variables={
                    "version": ServerVariable(default="1", description="API version"),
                },
            ),
            Server(url="https://stage.users.app", description="staging"),
            Server(url="https://users.local", description="development"),
        ],
        tags=[
            Tag(
                name="Users",
                summary="User API",
                parent="API",
                kind="domain",
                description="User operations",
                externalDocs=ExternalDoc(
                    description="User API docs",
                    url="https://example.com/users/docs",
                ),
            ),
        ],
        webhooks={
            "newPet": PathItem(
                post=Operation(
                    requestBody=RequestBody(
                        content={
                            "application/json": MediaType(
                                schema=Schema(
                                    type=DataType.ARRAY,
                                    items=Schema(
                                        type=[DataType.OBJECT, DataType.NULL],
                                        required=["id", "name"],
                                        properties={
                                            "id": Schema(type=DataType.INTEGER),
                                            "name": Schema(type=DataType.STRING),
                                        },
                                    ),
                                ),
                            ),
                        },
                    ),
                    responses={
                        "201": Response(description="Created"),
                    },
                ),
            ),
        },
        paths={
            "/users": PathItem(
                get=Operation(
                    summary="Get user list",
                    description="Method to get user list",
                    operationId="GetUserList",
                    tags=["Users"],
                    parameters=[
                        Parameter(
                            name="limit",
                            location=ParameterLocation.QUERY,
                            description="Result items limit",
                            allowEmptyValue=False,
                            example=10,
                            required=True,
                            allowReserved=True,
                            schema=Schema(
                                type=DataType.INTEGER,
                                not_schema=Schema(type=DataType.STRING),
                            ),
                        ),
                        Parameter(
                            name="offset",
                            location=ParameterLocation.QUERY,
                            description="Result items start offset",
                            allowEmptyValue=False,
                            example=0,
                            required=True,
                            schema=Schema(type=DataType.INTEGER),
                        ),
                        Parameter(
                            name="json",
                            location=ParameterLocation.QUERY,
                            description="Custom JSON parameter",
                            required=False,
                            content={
                                "application/json": MediaType(
                                    schema=Schema(
                                        type=DataType.OBJECT,
                                        properties={
                                            "key": Schema(
                                                type=DataType.STRING,
                                                example="test",
                                                description="Test parameter",
                                            ),
                                        },
                                    ),
                                ),
                            },
                        ),
                    ],
                    responses={
                        "200": Response(
                            description="Successful user list response",
                            content={
                                "application/json": MediaType(
                                    schema=Schema(
                                        type=DataType.OBJECT,
                                        required=["total_count", "users"],
                                        properties={
                                            "total_count": Schema(
                                                type=DataType.INTEGER,
                                                description="Total count of users",
                                            ),
                                            "users": Schema(
                                                type=DataType.ARRAY,
                                                items=Schema(allOf=_USER_ALLOF),
                                            ),
                                        },
                                    ),
                                ),
                            },
                        ),
                        "400": Response(
                            description="Bad request or parameters",
                            content={
                                "application/json": MediaType(
                                    schema=Schema(
                                        type=DataType.OBJECT,
                                        required=["code", "error"],
                                        properties={
                                            "code": Schema(
                                                type=DataType.INTEGER,
                                                example=1044,
                                                description="Internal error code",
                                            ),
                                            "error": Schema(
                                                type=DataType.STRING,
                                                example="Invalid user id value",
                                                description="Error details",
                                            ),
                                        },
                                    ),
                                ),
                            },
                        ),
                        "500": Response(
                            description="Internal error",
                            content={
                                "application/json": MediaType(
                                    schema=Schema(
                                        type=DataType.OBJECT,
                                        required=["code", "error"],
                                        properties={
                                            "code": Schema(
                                                type=DataType.INTEGER,
                                                example=1,
                                                description="Internal error code",
                                            ),
                                            "error": Schema(
                                                type=DataType.STRING,
                                                example="Unexpected server error",
                                                description="Error details",
                                            ),
                                        },
                                    ),
                                ),
                            },
                        ),
                    },
                ),
                post=Operation(
                    summary="Add new user",
                    description="Method to add new user",
                    operationId="AddUser",
                    security=[{"Basic": []}],
                    tags=["Users"],
                    requestBody=RequestBody(
                        description="New user model request",
                        content={
                            "application/json": MediaType(
                                schema=Schema(allOf=_USER_ALLOF),
                                encoding={
                                    "login": Encoding(
                                        contentType="text/plain",
                                        style=QueryParameterStyle.FORM,
                                    ),
                                    "email": Encoding(
                                        contentType="text/plain",
                                    ),
                                },
                            ),
                        },
                    ),
                    callbacks={
                        "onAdd": Callback(
                            expressions={
                                "{$request.body#/email}": PathItem(
                                    post=Operation(
                                        summary="Callback after user creation",
                                        responses={
                                            "200": Response(
                                                description="Callback processed successfully",
                                            ),
                                        },
                                    ),
                                ),
                            },
                        ),
                    },
                    responses={
                        "201": Response(
                            description="Successful addition user response",
                            content={
                                "application/json": MediaType(
                                    schema=Schema(
                                        type=DataType.OBJECT,
                                        required=["user"],
                                        properties={"user": Schema(allOf=_USER_ALLOF)},
                                    ),
                                ),
                            },
                        ),
                        "400": Response(
                            description="Bad request or parameters",
                            content={
                                "application/json": MediaType(
                                    schema=Schema(
                                        type=DataType.OBJECT,
                                        required=["code", "error"],
                                        properties={
                                            "code": Schema(
                                                type=DataType.INTEGER,
                                                example=1044,
                                                description="Internal error code",
                                            ),
                                            "error": Schema(
                                                type=DataType.STRING,
                                                example="Invalid user id value",
                                                description="Error details",
                                            ),
                                        },
                                    ),
                                ),
                            },
                        ),
                        "500": Response(
                            description="Internal error",
                            content={
                                "application/json": MediaType(
                                    schema=Schema(
                                        type=DataType.OBJECT,
                                        required=["code", "error"],
                                        properties={
                                            "code": Schema(
                                                type=DataType.INTEGER,
                                                example=1,
                                                description="Internal error code",
                                            ),
                                            "error": Schema(
                                                type=DataType.STRING,
                                                example="Unexpected server error",
                                                description="Error details",
                                            ),
                                        },
                                    ),
                                ),
                            },
                        ),
                    },
                ),
            ),
            "/users/{uuid}": PathItem(
                parameters=[
                    Parameter(
                        name="uuid",
                        location=ParameterLocation.PATH,
                        description="User unique id",
                        allowEmptyValue=False,
                        example="12345678-1234-5678-1234-567812345678",
                        required=True,
                        schema=Schema(type=DataType.STRING, format="uuid"),
                    ),
                ],
                get=Operation(
                    summary="Get user model",
                    description="Method to get user details",
                    operationId="GetUser",
                    tags=["Users"],
                    responses={
                        "200": Response(
                            description="Successful user response",
                            content={
                                "application/json": MediaType(
                                    schema=Schema(
                                        type=DataType.OBJECT,
                                        required=["user"],
                                        properties={"user": Schema(allOf=_USER_ALLOF)},
                                    ),
                                ),
                            },
                            links={
                                "UpdateUser": Link(
                                    operationId="UpdateUser",
                                    parameters={
                                        "uuid": "$response.body#/user/uuid",
                                    },
                                    description="Updates the user",
                                ),
                            },
                        ),
                        "400": Response(
                            description="Bad request or parameters",
                            content={
                                "application/json": MediaType(
                                    schema=Schema(
                                        type=DataType.OBJECT,
                                        required=["code", "error"],
                                        properties={
                                            "code": Schema(
                                                type=DataType.INTEGER,
                                                example=1044,
                                                description="Internal error code",
                                            ),
                                            "error": Schema(
                                                type=DataType.STRING,
                                                example="Invalid user id value",
                                                description="Error details",
                                            ),
                                        },
                                    ),
                                ),
                            },
                        ),
                        "500": Response(
                            description="Internal error",
                            content={
                                "application/json": MediaType(
                                    schema=Schema(
                                        type=DataType.OBJECT,
                                        required=["code", "error"],
                                        properties={
                                            "code": Schema(
                                                type=DataType.INTEGER,
                                                example=1,
                                                description="Internal error code",
                                            ),
                                            "error": Schema(
                                                type=DataType.STRING,
                                                example="Unexpected server error",
                                                description="Error details",
                                            ),
                                        },
                                    ),
                                ),
                            },
                        ),
                    },
                ),
                put=Operation(
                    summary="Update existed user model",
                    operationId="UpdateUser",
                    tags=["Users"],
                    responses={
                        "default": Response(description="Empty successful response"),
                        "200": Response(description="Empty successful response"),
                        "400": Response(
                            description="Bad request or parameters",
                            content={
                                "application/json": MediaType(
                                    schema=Schema(
                                        type=DataType.OBJECT,
                                        required=["code", "error"],
                                        properties={
                                            "code": Schema(
                                                type=DataType.INTEGER,
                                                example=1044,
                                                description="Internal error code",
                                            ),
                                            "error": Schema(
                                                type=DataType.STRING,
                                                example="Invalid user id value",
                                                description="Error details",
                                            ),
                                        },
                                    ),
                                ),
                            },
                        ),
                        "500": Response(
                            description="Internal error",
                            content={
                                "application/json": MediaType(
                                    schema=Schema(
                                        type=DataType.OBJECT,
                                        required=["code", "error"],
                                        properties={
                                            "code": Schema(
                                                type=DataType.INTEGER,
                                                example=1,
                                                description="Internal error code",
                                            ),
                                            "error": Schema(
                                                type=DataType.STRING,
                                                example="Unexpected server error",
                                                description="Error details",
                                            ),
                                        },
                                    ),
                                ),
                            },
                        ),
                    },
                ),
                patch=Operation(
                    summary="Patch user model",
                    operationId="PatchUser",
                    tags=["Users"],
                    requestBody=RequestBody(
                        content={
                            "application/json": MediaType(
                                schema=Schema(allOf=_USER_ALLOF),
                            ),
                        },
                    ),
                    responses={
                        "200": Response(
                            description="Successful user response",
                            content={
                                "application/json": MediaType(
                                    schema=Schema(
                                        type=DataType.OBJECT,
                                        required=["user"],
                                        properties={"user": Schema(allOf=_USER_ALLOF)},
                                    ),
                                ),
                            },
                            links={
                                "UpdateUser": Link(
                                    operationId="UpdateUser",
                                    parameters={
                                        "uuid": "$response.body#/user/uuid",
                                    },
                                    description="Updates the user",
                                ),
                            },
                        ),
                    },
                ),
                delete=Operation(
                    summary="Delete user",
                    operationId="DeleteUser",
                    tags=["Users"],
                    responses={
                        "204": Response(description="No content"),
                    },
                ),
            ),
            "/non-strict": PathItem(
                get=Operation(
                    responses={
                        "200": Response(
                            description="OK",
                            content={
                                "application/hal+json": MediaType(
                                    schema=Schema(
                                        type=DataType.OBJECT,
                                        properties={
                                            "expectedDeliveryDuration": Schema(
                                                type=DataType.STRING,
                                                format="duration",
                                            ),
                                        },
                                    ),
                                ),
                            },
                        ),
                        "400": Response(
                            description="Bad Request",
                            content={
                                "application/problem+json": MediaType(
                                    schema=Schema(
                                        type=DataType.OBJECT,
                                        properties={},
                                    ),
                                ),
                            },
                        ),
                    },
                ),
            ),
            "/equipment": PathItem(
                get=Operation(
                    responses={
                        "200": Response(
                            description="OK",
                            content={
                                "application/json": MediaType(
                                    schema=Schema(
                                        type=DataType.OBJECT,
                                        properties={
                                            "Features": Schema(
                                                type=DataType.ARRAY,
                                                items=Schema.model_construct(
                                                    ref_name="#/components/schemas/Feature",
                                                    type=DataType.OBJECT,
                                                    properties={
                                                        "Equipments": Schema(
                                                            type=DataType.ARRAY,
                                                            items=Schema.model_construct(
                                                                ref_name="#/components/schemas/Equipment",
                                                            ),
                                                        ),
                                                        "Id": Schema(
                                                            type=DataType.INTEGER,
                                                            format="int64",
                                                        ),
                                                    },
                                                ),
                                            ),
                                            "Id": Schema(
                                                type=DataType.INTEGER,
                                                format="int64",
                                            ),
                                        },
                                    ),
                                ),
                            },
                        ),
                    },
                ),
                additional_operations={
                    "query": Operation(
                        summary="Query equipment",
                        responses={
                            "200": Response(description="Equipment list"),
                        },
                    ),
                },
            ),
        },
        components=Components(
            securitySchemes={
                "Basic": SecurityScheme(
                    type=SecurityType.HTTP,
                    scheme="basic",
                ),
                "BearerAuth": SecurityScheme(
                    type=SecurityType.HTTP,
                    scheme="bearer",
                    bearerFormat="JWT",
                ),
                "ApiKey": SecurityScheme(
                    type=SecurityType.API_KEY,
                    location=ApiKeyLocation.HEADER,
                    name="X-API-Key",
                ),
            },
            parameters={
                "Limit": Parameter(
                    name="limit",
                    location=ParameterLocation.QUERY,
                    description="Result items limit",
                    allowEmptyValue=False,
                    example=10,
                    required=True,
                    allowReserved=True,
                    schema=Schema(
                        type=DataType.INTEGER,
                        not_schema=Schema(type=DataType.STRING),
                    ),
                ),
                "Offset": Parameter(
                    name="offset",
                    location=ParameterLocation.QUERY,
                    description="Result items start offset",
                    allowEmptyValue=False,
                    example=0,
                    required=True,
                    schema=Schema(type=DataType.INTEGER),
                ),
                "UserUUID": Parameter(
                    name="uuid",
                    location=ParameterLocation.PATH,
                    description="User unique id",
                    allowEmptyValue=False,
                    example="12345678-1234-5678-1234-567812345678",
                    required=True,
                    schema=Schema(type=DataType.STRING, format="uuid"),
                ),
                "JsonParameter": Parameter(
                    name="json",
                    location=ParameterLocation.QUERY,
                    description="Custom JSON parameter",
                    required=False,
                    content={
                        "application/json": MediaType(
                            schema=Schema(
                                type=DataType.OBJECT,
                                properties={
                                    "key": Schema(
                                        type=DataType.STRING,
                                        example="test",
                                        description="Test parameter",
                                    ),
                                },
                            ),
                        ),
                    },
                ),
            },
            responses={
                "BadRequest": Response(
                    description="Bad request or parameters",
                    content={
                        "application/json": MediaType(
                            schema=Schema(
                                type=DataType.OBJECT,
                                required=["code", "error"],
                                properties={
                                    "code": Schema(
                                        type=DataType.INTEGER,
                                        example=1044,
                                        description="Internal error code",
                                    ),
                                    "error": Schema(
                                        type=DataType.STRING,
                                        example="Invalid user id value",
                                        description="Error details",
                                    ),
                                },
                            ),
                        ),
                    },
                ),
                "InternalServerError": Response(
                    description="Internal error",
                    content={
                        "application/json": MediaType(
                            schema=Schema(
                                type=DataType.OBJECT,
                                required=["code", "error"],
                                properties={
                                    "code": Schema(
                                        type=DataType.INTEGER,
                                        example=1,
                                        description="Internal error code",
                                    ),
                                    "error": Schema(
                                        type=DataType.STRING,
                                        example="Unexpected server error",
                                        description="Error details",
                                    ),
                                },
                            ),
                        ),
                    },
                ),
                "Empty": Response(description="Empty successful response"),
                "GetUserListResponse": Response(
                    description="Successful user list response",
                    content={
                        "application/json": MediaType(
                            schema=Schema(
                                type=DataType.OBJECT,
                                required=["total_count", "users"],
                                properties={
                                    "total_count": Schema(
                                        type=DataType.INTEGER,
                                        description="Total count of users",
                                    ),
                                    "users": Schema(
                                        type=DataType.ARRAY,
                                        items=Schema(allOf=_USER_ALLOF),
                                    ),
                                },
                            ),
                        ),
                    },
                ),
                "AddUserResponse": Response(
                    description="Successful addition user response",
                    content={
                        "application/json": MediaType(
                            schema=Schema(
                                type=DataType.OBJECT,
                                required=["user"],
                                properties={"user": Schema(allOf=_USER_ALLOF)},
                            ),
                        ),
                    },
                ),
                "UserResponse": Response(
                    description="Successful user response",
                    content={
                        "application/json": MediaType(
                            schema=Schema(
                                type=DataType.OBJECT,
                                required=["user"],
                                properties={"user": Schema(allOf=_USER_ALLOF)},
                            ),
                        ),
                    },
                    links={
                        "UpdateUser": Link(
                            operationId="UpdateUser",
                            parameters={
                                "uuid": "$response.body#/user/uuid",
                            },
                            description="Updates the user",
                        ),
                    },
                ),
            },
            requestBodies={
                "AddUserRequest": RequestBody(
                    description="New user model request",
                    content={
                        "application/json": MediaType(
                            schema=Schema(allOf=_USER_ALLOF),
                            encoding={
                                "login": Encoding(
                                    contentType="text/plain",
                                    style=QueryParameterStyle.FORM,
                                ),
                                "email": Encoding(
                                    contentType="text/plain",
                                ),
                            },
                        ),
                    },
                ),
            },
            schemas={
                "BadRequestError": Schema(
                    type=DataType.OBJECT,
                    required=["code", "error"],
                    properties={
                        "code": Schema(
                            type=DataType.INTEGER,
                            example=1044,
                            description="Internal error code",
                        ),
                        "error": Schema(
                            type=DataType.STRING,
                            example="Invalid user id value",
                            description="Error details",
                        ),
                    },
                ),
                "InternalServerError": Schema(
                    type=DataType.OBJECT,
                    required=["code", "error"],
                    properties={
                        "code": Schema(
                            type=DataType.INTEGER,
                            example=1,
                            description="Internal error code",
                        ),
                        "error": Schema(
                            type=DataType.STRING,
                            example="Unexpected server error",
                            description="Error details",
                        ),
                    },
                ),
                "UUIDObject": _UUID_SCHEMA,
                "User": Schema(allOf=_USER_ALLOF),
                "Payload": Schema(
                    oneOf=[
                        Schema(type=DataType.STRING),
                        Schema(type=DataType.INTEGER),
                    ],
                    discriminator=Discriminator(
                        property_name="payloadType",
                        mapping={"str": "SomeTarget", "int": "OtherTarget"},
                    ),
                ),
                "Pet": Schema(
                    type=[DataType.OBJECT, DataType.NULL],
                    required=["id", "name"],
                    properties={
                        "id": Schema(type=DataType.INTEGER),
                        "name": Schema(type=DataType.STRING),
                    },
                ),
                "Equipment": Schema(
                    type=DataType.OBJECT,
                    properties={
                        "Features": Schema(
                            type=DataType.ARRAY,
                            items=Schema.model_construct(
                                ref_name="#/components/schemas/Feature",
                                type=DataType.OBJECT,
                                properties={
                                    "Equipments": Schema(
                                        type=DataType.ARRAY,
                                        items=Schema.model_construct(
                                            ref_name="#/components/schemas/Equipment",
                                        ),
                                    ),
                                    "Id": Schema(
                                        type=DataType.INTEGER,
                                        format="int64",
                                    ),
                                },
                            ),
                        ),
                        "Id": Schema(
                            type=DataType.INTEGER,
                            format="int64",
                        ),
                    },
                ),
                "Feature": Schema(
                    type=DataType.OBJECT,
                    properties={
                        "Equipments": Schema(
                            type=DataType.ARRAY,
                            items=Schema.model_construct(
                                ref_name="#/components/schemas/Equipment",
                            ),
                        ),
                        "Id": Schema(
                            type=DataType.INTEGER,
                            format="int64",
                        ),
                    },
                ),
            },
        ),
    )
    _break_circular_refs(spec)
    assert _strip_ref_name(spec.model_dump()) == _strip_ref_name(expected.model_dump())
