"""OpenAPI specification enum types."""

from enum import Enum, unique


@unique
class DataType(Enum):
    """OpenAPI data types."""

    NULL = "null"
    INTEGER = "integer"
    NUMBER = "number"
    STRING = "string"
    BOOLEAN = "boolean"
    ARRAY = "array"
    OBJECT = "object"
    ONE_OF = "oneOf"
    ANY_OF = "anyOf"


@unique
class IntegerFormat(Enum):
    """Integer format variants."""

    INT32 = "int32"
    INT64 = "int64"


@unique
class NumberFormat(Enum):
    """Number format variants."""

    FLOAT = "float"
    DOUBLE = "double"


@unique
class StringFormat(Enum):
    """String format variants."""

    BYTE = "byte"
    BINARY = "binary"
    DATE = "date"
    DATETIME = "date-time"
    PASSWORD = "password"
    UUID = "uuid"
    UUID4 = "uuid4"
    EMAIL = "email"
    URI = "uri"
    HOSTNAME = "hostname"
    IPV4 = "ipv4"
    IPV6 = "ipv6"
    URL = "url"
    TIME = "time"


@unique
class OperationMethod(Enum):
    """HTTP operation methods."""

    GET = "get"
    PUT = "put"
    POST = "post"
    DELETE = "delete"
    OPTIONS = "options"
    HEAD = "head"
    PATCH = "patch"
    TRACE = "trace"


@unique
class BaseLocation(Enum):
    """Base security location types."""

    HEADER = "header"
    QUERY = "query"
    COOKIE = "cookie"


@unique
class ParameterLocation(Enum):
    """Parameter location variants."""

    HEADER = "header"
    QUERY = "query"
    COOKIE = "cookie"
    PATH = "path"


@unique
class PathParameterStyle(Enum):
    """Path parameter serialization styles."""

    SIMPLE = "simple"
    LABEL = "label"
    MATRIX = "matrix"


@unique
class QueryParameterStyle(Enum):
    """Query parameter serialization styles."""

    FORM = "form"
    SPACE_DELIMITED = "spaceDelimited"
    PIPE_DELIMITED = "pipeDelimited"
    DEEP_OBJECT = "deepObject"


@unique
class HeaderParameterStyle(Enum):
    """Header parameter serialization styles."""

    SIMPLE = "simple"


@unique
class CookieParameterStyle(Enum):
    """Cookie parameter serialization styles."""

    FORM = "form"


@unique
class ContentType(Enum):
    """Media content type variants."""

    JSON = "application/json"
    JSON_TEXT = "text/json"
    JSON_ANY = "application/*+json"
    JSON_PROBLEM = "application/problem+json"
    XML = "application/xml"
    FORM = "application/x-www-form-urlencoded"
    MULTIPART_FORM = "multipart/form-data"
    PLAIN_TEXT = "text/plain"
    HTML = "text/html"
    PDF = "application/pdf"
    PNG = "image/png"
    JPEG = "image/jpeg"
    GIF = "image/gif"
    SVG = "image/svg+xml"
    AVIF = "image/avif"
    BMP = "image/bmp"
    WEBP = "image/webp"
    Image = "image/*"
    BINARY = "application/octet-stream"


@unique
class SecurityType(Enum):
    """Security scheme types."""

    API_KEY = "apiKey"
    HTTP = "http"
    OAUTH2 = "oauth2"
    OPEN_ID_CONNECT = "openIdConnect"


@unique
class AuthenticationScheme(Enum):
    """Authentication scheme variants."""

    BASIC = "basic"
    BEARER = "bearer"
    DIGEST = "digest"
    HOBA = "hoba"
    MUTUAL = "mutual"
    NEGOTIATE = "negotiate"
    OAUTH = "oauth"
    SCRAM_SHA1 = "scram-sha-1"
    SCRAM_SHA256 = "scram-sha-256"
    VAPID = "vapid"


@unique
class OAuthFlowType(Enum):
    """OAuth flow type variants."""

    IMPLICIT = "implicit"
    PASSWORD = "password"
    CLIENT_CREDENTIALS = "clientCredentials"
    AUTHORIZATION_CODE = "authorizationCode"
