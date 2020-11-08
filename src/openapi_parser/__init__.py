__version__ = '0.0.1'
__title__ = 'openapi-parser'
__author__ = 'Artyom Manchenkov'
__email__ = 'artyom@manchenkoff.me'
__description__ = 'OpenAPI v3 parser'

from .parser import parse

__all__ = [
    "parse"
]
