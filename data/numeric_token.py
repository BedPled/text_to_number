from dataclasses import dataclass
from data.numeral import Numeral


@dataclass
class NumericToken:
    value: Numeral  # значение (Numeral)
    error: float = 0  # ошибка распознавания
    is_significant: bool = False  # указывает, что токен был использован для распознавания

