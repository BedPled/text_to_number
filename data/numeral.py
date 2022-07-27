from dataclasses import dataclass


@dataclass
class Numeral:
    value: int = 0
    level: int = 0
    is_multiplier: bool = False
