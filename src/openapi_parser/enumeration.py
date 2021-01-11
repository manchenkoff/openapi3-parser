from enum import Enum, unique


@unique
class DataType(Enum):
    INTEGER = 'integer'
    NUMBER = 'number'
    STRING = 'string'
    BOOLEAN = 'boolean'
    ARRAY = 'array'
    OBJECT = 'object'


@unique
class IntegerFormat(Enum):
    INT32 = 'int32'
    INT64 = 'int64'


@unique
class NumberFormat(Enum):
    FLOAT = 'float'
    DOUBLE = 'double'


@unique
class StringFormat(Enum):
    BYTE = 'byte'
    BINARY = 'binary'
    DATE = 'date'
    DATETIME = 'date-time'
    PASSWORD = 'password'
    UUID = 'uuid'
    EMAIL = 'email'


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
    HEADER = 'header'
    QUERY = 'query'
    COOKIE = 'cookie'


@unique
class ParameterLocation(Enum):
    HEADER = 'header'
    QUERY = 'query'
    COOKIE = 'cookie'
    PATH = 'path'


@unique
class MediaType(Enum):
    JSON = 'application/json'
    XML = 'application/xml'
    FORM = 'application/x-www-form-urlencoded'
    MULTIPART_FORM = 'multipart_form/form-data'
    PLAIN_TEXT = 'text/plain'
    HTML = 'text/html'
    PDF = 'application/pdf'
    PNG = 'image/png'


@unique
class SecurityType(Enum):
    API_KEY = 'apiKey'
    HTTP = 'http'
    OAUTH2 = 'oauth2'
    OPEN_ID_CONNECT = 'openIdConnect'


@unique
class AuthenticationScheme(Enum):
    BASIC = 'basic'
    BEARER = 'bearer'
    DIGEST = 'digest'
    HOBA = 'hoba'
    MUTUAL = 'mutual'
    NEGOTIATE = 'negotiate'
    OAUTH = 'oauth'
    SCRAM_SHA1 = 'scram-sha-1'
    SCRAM_SHA256 = 'scram-sha-256'
    VAPID = 'vapid'


@unique
class OAuthFlowType(Enum):
    IMPLICIT = 'implicit'
    PASSWORD = 'password'
    CLIENT_CREDENTIALS = 'clientCredentials'
    AUTHORIZATION_CODE = 'authorizationCode'
