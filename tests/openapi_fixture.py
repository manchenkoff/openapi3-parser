from openapi_parser.specification import *

schema_user = Object(
    type=DataType.OBJECT,
    required=["uuid", "login", "email", "avatar"],
    properties=[
        Property(
            name="uuid",
            schema=String(
                type=DataType.STRING,
                description="Unique object id",
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
        Property(
            name="avatar",
            schema=String(
                type=DataType.STRING,
                description="User Avatar URL",
                example="https://github.com/manchenkoff/openapi3-parser",
                format=StringFormat.URI,
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
    code=200,
    description="Successful user list response",
    content=[
        Content(
            type=ContentType.JSON,
            schema=user_list_schema,
            example="An example",
            examples=[]
        ),
    ],
    is_default=False,
)

bad_request_response = Response(
    code=400,
    is_default=False,
    description="Bad request or parameters",
    content=[
        Content(
            type=ContentType.JSON,
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
            ),
            example="an example",
            examples=[]
        ),
    ],
)

internal_error_response = Response(
    code=500,
    is_default=False,
    description="Internal error",
    content=[
        Content(
            type=ContentType.JSON,
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
            ),
            example="an example",
            examples=[]
        ),
    ],
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
        Server(url="https://stage.users.app",
               description="staging"),
        Server(url="https://users.local",
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

    schemas = {
        "BadRequestError": Object(
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
        ),
        "InternalServerError": Object(
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
        ),
        "UUIDObject": Object(
            type=DataType.OBJECT,
            required=["uuid"],
            properties=[
                Property(
                    name="uuid",
                    schema=String(
                        type=DataType.STRING,
                        format=StringFormat.UUID,
                        example="12345678-1234-5678-1234-567812345678",
                        description="Unique object id",
                    )
                ),
            ],
        ),
        "User": Object(
            type=DataType.OBJECT,
            required=["uuid", "login", "email", "avatar"],
            properties=[
                Property(
                    name="uuid",
                    schema=String(
                        type=DataType.STRING,
                        format=StringFormat.UUID,
                        example="12345678-1234-5678-1234-567812345678",
                        description="Unique object id",
                    )
                ),
                Property(
                    name="login",
                    schema=String(
                        type=DataType.STRING,
                        example="super-admin",
                        description="User login or nickname",
                    )
                ),
                Property(
                    name="email",
                    schema=String(
                        type=DataType.STRING,
                        format=StringFormat.EMAIL,
                        example="user@mail.com",
                        description="User E-mail address",
                    )
                ),
                Property(
                    name="avatar",
                    schema=String(
                        type=DataType.STRING,
                        description="User Avatar URL",
                        example="https://github.com/manchenkoff/openapi3-parser",
                        format=StringFormat.URI,
                    )
                ),
            ],
        )
    }

    security = [
        {"Basic": []}
    ]

    uuid_parameters = [
        Parameter(
            name="uuid",
            location=ParameterLocation.PATH,
            description="User unique id",
            required=True,
            explode=False,
            style=PathParameterStyle.SIMPLE,
            schema=String(
                type=DataType.STRING,
                format=StringFormat.UUID,
            ),
        ),
    ]

    path_list: list[Path] = [
        Path(
            url="/users",
            operations=[
                Operation(
                    method=OperationMethod.GET,
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
                            explode=True,
                            style=QueryParameterStyle.FORM,
                            schema=Integer(type=DataType.INTEGER)
                        ),
                        Parameter(
                            name="offset",
                            location=ParameterLocation.QUERY,
                            description="Result items start offset",
                            required=True,
                            explode=True,
                            style=QueryParameterStyle.FORM,
                            schema=Integer(type=DataType.INTEGER)
                        ),
                    ],
                    responses=[
                        get_user_list_response,
                        bad_request_response,
                        internal_error_response,
                    ]
                ),
                Operation(
                    method=OperationMethod.POST,
                    summary="Add new user",
                    description="Method to add new user",
                    operation_id="AddUser",
                    tags=["Users"],
                    security=[
                        {'Basic': []}
                    ],
                    request_body=RequestBody(
                        description="New user model request",
                        content=[
                            Content(type=ContentType.JSON, schema=schema_user, example=None, examples=[])
                        ]
                    ),
                    responses=[
                        Response(
                            code=201,
                            is_default=False,
                            description="Successful addition user response",
                            content=[
                                Content(
                                    type=ContentType.JSON,
                                    schema=Object(
                                        type=DataType.OBJECT,
                                        required=["user"],
                                        properties=[
                                            Property(
                                                name="user",
                                                schema=schema_user,
                                            ),
                                        ],
                                    ),
                                    example=None,
                                    examples=[]
                                ),
                            ]
                        ),
                        bad_request_response,
                        internal_error_response,
                    ],
                ),
            ]
        ),
        Path(
            url="/users/{uuid}",
            parameters=uuid_parameters,
            operations=[
                Operation(
                    method=OperationMethod.GET,
                    summary="Get user model",
                    description="Method to get user details",
                    operation_id="GetUser",
                    tags=["Users"],
                    parameters=uuid_parameters,
                    responses=[
                        Response(
                            code=200,
                            is_default=False,
                            description="Successful user response",
                            content=[
                                Content(
                                    type=ContentType.JSON,
                                    schema=Object(
                                        type=DataType.OBJECT,
                                        required=["user"],
                                        properties=[
                                            Property(
                                                name="user",
                                                schema=schema_user,
                                            ),
                                        ],
                                    ),
                                    example=None,
                                    examples=[]
                                ),
                            ]
                        ),
                        bad_request_response,
                        internal_error_response,
                    ],
                ),
                Operation(
                    method=OperationMethod.PUT,
                    summary="Update existed user model",
                    operation_id="UpdateUser",
                    tags=["Users"],
                    parameters=uuid_parameters,
                    responses=[
                        Response(code=None, description="Empty successful response", is_default=True),
                        Response(code=200, description="Empty successful response", is_default=False),
                        bad_request_response,
                        internal_error_response,
                    ],
                ),
            ]
        ),
    ]

    return Specification(version="3.0.0",
                         info=info,
                         servers=server_list,
                         tags=tag_list,
                         paths=path_list,
                         security_schemas=security_schemes,
                         security=security,
                         schemas=schemas)
