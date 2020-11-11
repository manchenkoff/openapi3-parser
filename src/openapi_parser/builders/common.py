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
