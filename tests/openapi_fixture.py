from openapi_parser.enumeration import AuthenticationScheme, DataType, MediaType, OperationMethod, ParameterLocation, \
    SecurityType, StringFormat
from openapi_parser.specification import Array, Contact, Content, Info, Integer, \
    License, Object, Operation, Parameter, Path, PathItem, PathList, Property, \
    RequestBody, Response, Security, Server, Specification, String, Tag

schema_user = Object(
    type=DataType.OBJECT,
    required=["uuid", "login", "email"],
    properties=[
        Property(
            name="uuid",
            schema=String(
                type=DataType.STRING,
                description="Unique user id",
                example="12345678-1234-5678-1234-567812345678",
                format=StringFormat.UUID,
            )
        ),
        Property(
            name="login",
            schema=String(
                type=DataType.STRING,
                description="User login or nickname",
                example="super-admin",
            )
        ),
        Property(
            name="email",
            schema=String(
                type=DataType.STRING,
                description="User E-mail address",
                example="user@mail.com",
                format=StringFormat.EMAIL,
            )
        ),
    ],
)

user_list_schema = Object(
    type=DataType.OBJECT,
    required=["total_count", "users"],
    properties=[
        Property(
            name="total_count",
            schema=Integer(
                type=DataType.INTEGER,
                description="Total count of users",
            )
        ),
        Property(
            name="users",
            schema=Array(
                type=DataType.ARRAY,
                items=schema_user,
            )
        ),
    ]
)

get_user_list_response = Response(
    description="Successful user list response",
    content={
        MediaType.JSON: Content(
            schema=user_list_schema
        ),
    }
)

bad_request_response = Response(
    description="Bad request or parameters",
    content={
        MediaType.JSON: Content(
            schema=Object(
                type=DataType.OBJECT,
                required=["code", "error"],
                properties=[
                    Property(
                        name="code",
                        schema=Integer(
                            type=DataType.INTEGER,
                            example=1044,
                            description="Internal error code",
                        )
                    ),
                    Property(
                        name="error",
                        schema=String(
                            type=DataType.STRING,
                            example="Invalid user id value",
                            description="Error details",
                        )
                    ),
                ],
            )
        ),
    },
)

internal_error_response = Response(
    description="Internal error",
    content={
        MediaType.JSON: Content(
            schema=Object(
                type=DataType.OBJECT,
                required=["code", "error"],
                properties=[
                    Property(
                        name="code",
                        schema=Integer(
                            type=DataType.INTEGER,
                            example=1,
                            description="Internal error code",
                        )
                    ),
                    Property(
                        name="error",
                        schema=String(
                            type=DataType.STRING,
                            example="Unexpected server error",
                            description="Error details",
                        )
                    ),
                ],
            )
        ),
    },
)


def create_specification() -> Specification:
    info = Info(title="User example service",
                version="1.0.0",
                description="Example service specification to work with user storage",
                license=License(name="MIT"),
                contact=Contact(name="manchenkoff", email="artyom@manchenkoff.me"))

    server_list = [
        Server(url="https://users.app",
               description="production"),
        Server(url="http://stage.users.app",
               description="staging"),
        Server(url="http://users.local",
               description="development"),
    ]

    tag_list = [
        Tag(name="Users", description="User operations"),
    ]

    security_schemes = {
        "Basic": Security(
            type=SecurityType.HTTP,
            scheme=AuthenticationScheme.BASIC
        ),
    }

    security = [
        {"Basic": []}
    ]

    path_list: PathList = [
        Path(
            pattern="/users",
            item=PathItem(
                operations={
                    OperationMethod.GET: Operation(
                        summary="Get user list",
                        description="Method to get user list",
                        operation_id="GetUserList",
                        tags=["Users"],
                        parameters=[
                            Parameter(
                                name="limit",
                                location=ParameterLocation.QUERY,
                                description="Result items limit",
                                required=True,
                                schema=Integer(type=DataType.INTEGER)
                            ),
                            Parameter(
                                name="offset",
                                location=ParameterLocation.QUERY,
                                description="Result items start offset",
                                required=True,
                                schema=Integer(type=DataType.INTEGER)
                            ),
                        ],
                        responses={
                            200: get_user_list_response,
                            400: bad_request_response,
                            500: internal_error_response,
                        }
                    ),
                    OperationMethod.POST: Operation(
                        summary="Add new user",
                        description="Method to add new user",
                        operation_id="AddUser",
                        tags=["Users"],
                        request_body=RequestBody(
                            description="New user model request",
                            content={
                                MediaType.JSON: Content(schema=user_list_schema),
                            }
                        ),
                        responses={
                            201: Response(
                                description="Successful addition user response",
                                content={
                                    MediaType.JSON: Content(
                                        schema=Object(
                                            type=DataType.OBJECT,
                                            required=["user"],
                                            properties=[
                                                Property(
                                                    name="user",
                                                    schema=user_list_schema,
                                                ),
                                            ],
                                        ),
                                    ),
                                }
                            ),
                            400: bad_request_response,
                            500: internal_error_response,
                        },
                    ),
                }
            )
        ),
        Path(
            pattern="/users/{uuid}",
            item=PathItem(
                parameters=[
                    Parameter(
                        name="uuid",
                        location=ParameterLocation.PATH,
                        description="User unique id",
                        required=True,
                        schema=String(
                            type=DataType.STRING,
                            format=StringFormat.UUID,
                        ),
                    ),
                ],
                operations={
                    OperationMethod.GET: Operation(
                        summary="Get user model",
                        description="Method to get user details",
                        operation_id="GetUser",
                        tags=["Users"],
                        responses={
                            200: Response(
                                description="Successful user response",
                                content={
                                    MediaType.JSON: Content(
                                        schema=Object(
                                            type=DataType.OBJECT,
                                            required=["user"],
                                            properties=[
                                                Property(
                                                    name="user",
                                                    schema=user_list_schema,
                                                ),
                                            ],
                                        ),
                                    ),
                                }
                            ),
                            400: bad_request_response,
                            500: internal_error_response,
                        },
                    ),
                    OperationMethod.PUT: Operation(
                        summary="Update existed user model",
                        operation_id="UpdateUser",
                        tags=["Users"],
                        responses={
                            200: Response(description="Empty successful response"),
                            400: bad_request_response,
                            500: internal_error_response,
                        },
                    ),
                }
            )
        ),
    ]

    return Specification(version="3.0.0",
                         info=info,
                         servers=server_list,
                         tags=tag_list,
                         paths=path_list,
                         security_schemas=security_schemes,
                         security=security)
