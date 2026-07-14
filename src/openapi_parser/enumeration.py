"""OpenAPI specification enum types."""

from enum import Enum, unique


@unique
class DataType(str, Enum):
    """OpenAPI data types."""

    NULL = "null"
    INTEGER = "integer"
    NUMBER = "number"
    STRING = "string"
    BOOLEAN = "boolean"
    ARRAY = "array"
    OBJECT = "object"


@unique
class ApiKeyLocation(str, Enum):
    """API key location in the request."""

    HEADER = "header"
    QUERY = "query"
    COOKIE = "cookie"


@unique
class ParameterLocation(str, Enum):
    """Parameter location variants."""

    HEADER = "header"
    QUERY = "query"
    COOKIE = "cookie"
    PATH = "path"


@unique
class PathParameterStyle(str, Enum):
    """Path parameter serialization styles."""

    SIMPLE = "simple"
    LABEL = "label"
    MATRIX = "matrix"


@unique
class QueryParameterStyle(str, Enum):
    """Query parameter serialization styles."""

    FORM = "form"
    SPACE_DELIMITED = "spaceDelimited"
    PIPE_DELIMITED = "pipeDelimited"
    DEEP_OBJECT = "deepObject"


@unique
class HeaderParameterStyle(str, Enum):
    """Header parameter serialization styles."""

    SIMPLE = "simple"


@unique
class CookieParameterStyle(str, Enum):
    """Cookie parameter serialization styles."""

    FORM = "form"


@unique
class SecurityType(str, Enum):
    """Security scheme types."""

    API_KEY = "apiKey"
    HTTP = "http"
    OAUTH2 = "oauth2"
    OPEN_ID_CONNECT = "openIdConnect"


@unique
class OAuthFlowType(str, Enum):
    """OAuth flow type variants."""

    IMPLICIT = "implicit"
    PASSWORD = "password"
    CLIENT_CREDENTIALS = "clientCredentials"
    AUTHORIZATION_CODE = "authorizationCode"
