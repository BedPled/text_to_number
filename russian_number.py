import re
from data.numeral import Numeral
from data.russian_number_parser_optons import RussianNumberParserOptions
from data.russian_number_parser_result import RussianNumberParserResult
from data.numeric_token import NumericToken
from numeral_levenshtein import NumeralLevenshtein


class RussianNumber:
    NumeralLevenshtein.init()

    _rgSplitter = r'\s+'            # регулярка для деления строки на токены
    _MAX_TOKEN_LENGTH = 12          # максимальная длина токена (слова)
    _MAX_ERROR_LIMIT = 0.3          # максимально допустимая средняя ошибка
    _MAX_TOKEN_ERROR_LIMIT = 0.3    # максимально допустимая ошибка токена

    #  словарь токенов
    _TOKENS = {
                "ноль":              Numeral(0, 1, False),
                "один":              Numeral(1, 1, False),
                "одна":              Numeral(1, 1, False),
                "два":               Numeral(2, 1, False),
                "две":               Numeral(2, 1, False),
                "три":               Numeral(3, 1, False),
                "четыре":            Numeral(4, 1, False),
                "пять":              Numeral(5, 1, False),
                "шесть":             Numeral(6, 1, False),
                "семь":              Numeral(7, 1, False),
                "восемь":            Numeral(8, 1, False),
                "девять":            Numeral(9, 1, False),
                "десять":            Numeral(10, 1, False),
                "одиннадцать":       Numeral(11, 1, False),
                "двенадцать":        Numeral(12, 1, False),
                "тринадцать":        Numeral(13, 1, False),
                "четырнадцать":      Numeral(14, 1, False),
                "пятнадцать":        Numeral(15, 1, False),
                "шестнадцать":       Numeral(16, 1, False),
                "семнадцать":        Numeral(17, 1, False),
                "восемнадцать":      Numeral(18, 1, False),
                "девятнадцать":      Numeral(19, 1, False),

                "двадцать":          Numeral(20, 2, False),
                "тридцать":          Numeral(30, 2, False),
                "сорок":             Numeral(40, 2, False),
                "пятьдесят":         Numeral(50, 2, False),
                "шестьдесят":        Numeral(60, 2, False),
                "семьдесят":         Numeral(70, 2, False),
                "восемьдесят":       Numeral(80, 2, False),
                "девяносто":         Numeral(90, 2, False),

                "сто":               Numeral(100, 3, False),
                "двести":            Numeral(200, 3, False),
                "триста":            Numeral(300, 3, False),
                "четыреста":         Numeral(400, 3, False),
                "пятьсот":           Numeral(500, 3, False),
                "шестьсот":          Numeral(600, 3, False),
                "семьсот":           Numeral(700, 3, False),
                "восемьсот":         Numeral(800, 3, False),
                "девятьсот":         Numeral(900, 3, False),

                "тысяч":             Numeral(1000, 4, True),
                "тысяча":            Numeral(1000, 4, True),
                "тысячи":            Numeral(1000, 4, True),
               }

    @classmethod
    def __parse_tokens(cls, in_str, options, lev_array, level):  # распознать токены
        try:
            if cls._TOKENS[in_str]:
                return [NumericToken(cls._TOKENS[in_str])]
        except KeyError:
            length = len(in_str)
            if length < 2:  # слишком короткая строка
                return []
            else:
                # строка не найдена => просчитываем варианты
                complex_parsing = length >= 6 and level <= 2
                variants = [] if complex_parsing else None

                # односложная фраза
                if length <= cls._MAX_TOKEN_LENGTH:
                    # пытаемся распознать с помощью расстояния Левенштейна
                    minimal_error = float('inf')  # PositiveInfinity

                    for item in cls._TOKENS:
                        error = NumeralLevenshtein.compare_strings(in_str, item, lev_array)
                        if error < minimal_error:
                            numeral = cls._TOKENS[item]
                            minimal_error = error

                    if minimal_error <= options.MaxTokenError:
                        if complex_parsing:
                            # могут быть другие варианты
                            variants.append([NumericToken(numeral, minimal_error)])
                        else:
                            return [NumericToken(numeral, minimal_error)]
                    elif not complex_parsing:
                        if level == 0:
                            # на первом уровне игнорируем плохие токены
                            return []
                        else:
                            # в рекурсии возвращаем плохие токены, чтобы они влияли на принятие решения
                            return [NumericToken(numeral, minimal_error)]

                # составная фраза

                # строки длиной меньше шести смысла делить нет
                if complex_parsing:
                    i = 3
                    while i <= length - 3:
                        left = cls.__parse_tokens(in_str[0:i], options, lev_array, level + 1)
                        right = cls.__parse_tokens(in_str[i:], options, lev_array, level + 1)

                        union = left + right
                        if len(union) > 0:
                            er = 0
                            for u in union:
                                er += u.error
                            # if sum(union.Error) != 0:
                            if er != 0:
                                # ухудшаем общий результат на некую величину
                                for x in union:
                                    x.error += options.SplitErrorValue / len(union)

                            # объединяем результат
                            variants.append(union)

                        i += 1

                # выбираем лучший вариант
                if not variants:
                    return []
                else:
                    best = None

                    minimal_error = float('inf')  # PositiveInfinity
                    for item in variants:

                        # считаем суммарную ошибку
                        error = 0
                        for it in item:
                            error += it.error
                        if error < minimal_error:
                            best = item
                            minimal_error = error

                    return best if best is not None else []

    @classmethod
    def text_to_numeral(cls, text, options=None):  # перевод строковой формы числа в числовое
        if text is None:
            print("text == None")
            return RussianNumberParserResult(-1, 1)

        text = text.translate({ord('_'): None})  # удаление символа '_'
        text = text.strip()
        text = text.lower()

        if len(text) == 0:
            print("text == 0")
            return RussianNumberParserResult(-1, 1)

        if options is None:
            options = RussianNumberParserOptions()

        # массив для расстояния Левенштейна
        lev_array = [0] * 2
        for i in range(2):
            lev_array[i] = [0] * (cls._MAX_TOKEN_LENGTH + 1)

        # разбиваем текст на токены
        string_tokens = re.split(cls._rgSplitter, text)
        tokens = list()

        # вытаскиваем значения токенов из листов
        for item in string_tokens:
            tk = cls.__parse_tokens(item, options, lev_array, 0)
            if len(tk) > 0:
                for tok in tk:
                    tokens.append(tok)

        tokens_for_del = list()

        for item in tokens:
            if item.error > cls._MAX_TOKEN_ERROR_LIMIT:
                tokens_for_del.append(item)

        for item in tokens_for_del:
            tokens.remove(item)

        # вспомогательные переменные
        global_level = None
        local_level = None
        global_value = None
        local_value = None
        was_critical_error = False

        # цикл по токенам
        n = len(tokens)
        for i in range(0, n):
            token = tokens[i]
            if token.error > options.MaxTokenError:
                continue

            value = token.value.value
            level = token.value.level
            multiplier = token.value.is_multiplier

            if multiplier:
                # множитель
                if global_level is None or global_level > level:

                    if global_value is not None:
                        global_value = global_value + (local_value if local_value is not None else 1) * value
                    else:
                        global_value = (local_value if local_value is not None else 1) * value

                    global_level = level
                    local_value = None
                    local_level = None
                    token.is_significant = True
                else:
                    # ошибка несоответствия уровней
                    token.error = 1
                    token.is_significant = True
                    was_critical_error = True
            else:
                # простое числительное
                if local_level is None or local_level > level:
                    local_value = (local_value if local_value is not None else 0) + value
                    local_level = level
                    token.is_significant = True
                else:
                    # ошибка несоответствия уровней
                    token.error = 1
                    token.is_significant = True
                    was_critical_error = True

        count = 0
        total_error = 0

        # подсчёт использованных для распознавания токенов
        for x in tokens:
            if x.is_significant:
                count += 1
                if x is None:
                    total_error += 1
                else:
                    total_error += x.error

        if count > 0:
            total_error = total_error / count
        else:
            was_critical_error = True
            total_error = 1

        if was_critical_error:
            # имело место критическая ошибка
            if total_error >= 0.5:
                total_error = 1
            else:
                total_error *= 2

        if global_value is None:
            global_value = 0
        if local_value is None:
            local_value = 0

        return RussianNumberParserResult(global_value + local_value, total_error)

    @classmethod
    def text_to_number(cls, text):  # обёртка для text_to_numeral возвращающая целое число
        num = cls.text_to_numeral(text)
        if num.Error > cls._MAX_ERROR_LIMIT:
            return -1

        return num.Value
