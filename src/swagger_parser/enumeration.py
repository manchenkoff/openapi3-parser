from enum import Enum, unique


@unique
class DataType(Enum):
    integer = 'integer'
    number = 'number'
    string = 'string'
    boolean = 'boolean'
    array = 'array'
    object = 'object'


@unique
class IntegerFormat(Enum):
    int32 = 'int32'
    int64 = 'int64'


@unique
class NumberFormat(Enum):
    float = 'float'
    double = 'double'


@unique
class StringFormat(Enum):
    byte = 'byte'
    binary = 'binary'
    date = 'date'
    datetime = 'date-time'
    password = 'password'
    uuid = 'uuid'
    email = 'email'


@unique
class OperationMethod(Enum):
    GET = 'get'
    PUT = 'put'
    POST = 'post'
    DELETE = 'delete'
    OPTIONS = 'options'
    HEAD = 'head'
    PATCH = 'patch'
    TRACE = 'trace'


@unique
class BaseLocation(Enum):
    header = 'header'
    query = 'query'
    cookie = 'cookie'


@unique
class ParameterLocation(Enum):
    header = 'header'
    query = 'query'
    cookie = 'cookie'
    path = 'path'


@unique
class MediaType(Enum):
    json = 'application/json'
    xml = 'application/xml'
    form = 'application/x-www-form-urlencoded'
    multipart_form = 'multipart_form/form-data'
    plain_text = 'text/plain; charset=utf-8'
    html = 'text/html'
    pdf = 'application/pdf'
    png = 'image/png'


@unique
class SecurityType(Enum):
    api_key = 'apiKey'
    http = 'http'
    oauth2 = 'oauth2'
    open_id_connect = 'openIdConnect'


@unique
class AuthenticationScheme(Enum):
    basic = 'Basic'
    bearer = 'Bearer'
    digest = 'Digest'
    hoba = 'HOBA'
    mutual = 'Mutual'
    negotiate = 'Negotiate'
    oauth = 'OAuth'
    scram_sha1 = 'SCRAM-SHA-1'
    scram_sha256 = 'SCRAM-SHA-256'
    vapid = 'vapid'


@unique
class OAuthFlowType(Enum):
    implicit = 'implicit'
    password = 'password'
    client_credentials = 'clientCredentials'
    authorization_code = 'authorizationCode'
