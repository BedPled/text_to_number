from dataclasses import dataclass


@dataclass
class RussianNumberParserResult:
    Value: int      # значение
    Error: float    # ошибка распознавания

