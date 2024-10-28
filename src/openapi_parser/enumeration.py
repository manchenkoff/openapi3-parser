from enum import Enum, unique


@unique
class DataType(Enum):
    NULL = 'null'
    INTEGER = 'integer'
    NUMBER = 'number'
    STRING = 'string'
    BOOLEAN = 'boolean'
    ARRAY = 'array'
    OBJECT = 'object'
    ONE_OF = 'oneOf'
    ANY_OF = 'anyOf'


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
    UUID4 =  'uuid4'
    EMAIL = 'email'
    URI = 'uri'
    HOSTNAME = 'hostname'
    IPV4 = 'ipv4'
    IPV6 = 'ipv6'
    URL = 'url'


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
class PathParameterStyle(Enum):
    SIMPLE = 'simple'
    LABEL = 'label'
    MATRIX = 'matrix'


@unique
class QueryParameterStyle(Enum):
    FORM = 'form'
    SPACE_DELIMITED = 'spaceDelimited'
    PIPE_DELIMITED = 'pipeDelimited'
    DEEP_OBJECT = 'deepObject'


@unique
class HeaderParameterStyle(Enum):
    SIMPLE = 'simple'


@unique
class CookieParameterStyle(Enum):
    FORM = 'form'


@unique
class ContentType(Enum):
    JSON = 'application/json'
    JSON_TEXT = 'text/json'
    JSON_ANY = 'application/*+json'
    JSON_PROBLEM = 'application/problem+json'
    XML = 'application/xml'
    FORM = 'application/x-www-form-urlencoded'
    MULTIPART_FORM = 'multipart/form-data'
    PLAIN_TEXT = 'text/plain'
    HTML = 'text/html'
    PDF = 'application/pdf'
    PNG = 'image/png'
    JPEG = 'image/jpeg'
    GIF = 'image/gif'
    SVG = 'image/svg+xml'
    AVIF = 'image/avif'
    BMP = 'image/bmp'
    WEBP = 'image/webp'
    Image = 'image/*'
    BINARY = 'application/octet-stream'


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
