from collections import namedtuple
from typing import Any, Callable, Dict, Optional

from ..errors import ParserError

PropertyMeta = namedtuple('PropertyMeta', ['cast', 'name'])


def extract_typed_props(data: dict, attrs_map: Dict[str, PropertyMeta]) -> Dict[str, Any]:
    def cast_value(name: str, value: Any, type_cast_func: Optional[Callable]) -> Any:
        try:
            return type_cast_func(value) \
                if type_cast_func is not None \
                else value
        except ValueError:
            raise ParserError(f"Invalid '{name}' property value for type: {type_cast_func}")

    custom_attrs = {
        attr_name: cast_value(attr_info.name, data[attr_info.name], attr_info.cast)
        for attr_name, attr_info in attrs_map.items()
        if data.get(attr_info.name) is not None
    }

    return custom_attrs


def merge_dicts(original: dict, other: dict) -> dict:
    source = original.copy()

    for key, value in other.items():
        source[key] = value \
            if key not in source \
            else (merge_dicts(source[key], value) if isinstance(value, dict) else value)

    return source


def extract_extension_attributes(schema: dict) -> dict:
    extension_key_format = 'x-'

    extensions_dict: dict = {
        key.replace(extension_key_format, '').replace('-', '_'): value
        for key, value in schema.items()
        if key.startswith(extension_key_format)
    }

    return extensions_dict
