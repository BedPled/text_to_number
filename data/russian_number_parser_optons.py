from dataclasses import dataclass


@dataclass
class RussianNumberParserOptions:
    # настройки по умолчанию
    # предельное значение ошибки в токене, чтобы его можно было использовать для распознавания
    MaxTokenError: float = 0.67
    # величина, на которую ухудшается результат после деления подстроки на более мелкие части
    SplitErrorValue: float = 0.1
