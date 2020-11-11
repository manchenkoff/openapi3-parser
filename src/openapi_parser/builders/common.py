from collections import namedtuple
from typing import Any, Dict, Optional

from ..errors import ParserError


# TODO: rename type -> cast, PropertyInfoType -> ???
PropertyInfoType = namedtuple('PropertyInfoType', ['type', 'name'])


def extract_attrs_by_map(data: dict, attrs_map: Dict[str, PropertyInfoType]) -> Dict[str, Any]:
    def cast_value(name: str, value: Any, value_type: Optional[type]) -> Any:
        if not value_type:
            return value

        try:
            return value_type(value)
        except ValueError:
            raise ParserError(f"Invalid '{name}' property value for type: {value_type}")

    custom_attrs = {
        attr_name: cast_value(attr_info.name, data[attr_info.name], attr_info.type)
        for attr_name, attr_info in attrs_map.items()
        if data.get(attr_info.name) is not None
    }

    return custom_attrs
