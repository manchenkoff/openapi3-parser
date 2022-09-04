from dataclasses import dataclass


@dataclass
class LooseEnum:
    value: str


LooseContentType = LooseEnum
LooseIntegerFormat = LooseEnum
LooseNumberFormat = LooseEnum
LooseStringFormat = LooseEnum
