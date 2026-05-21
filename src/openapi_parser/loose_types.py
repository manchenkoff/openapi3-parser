"""Loose type aliases for non-strict enum matching."""

from dataclasses import dataclass


@dataclass
class LooseEnum:
    """Enum that accepts any string value."""

    value: str


LooseContentType = LooseEnum
LooseIntegerFormat = LooseEnum
LooseNumberFormat = LooseEnum
LooseStringFormat = LooseEnum
