
class NumeralLevenshtein:
    _insert = {}  # таблица стоимости вставки
    _delete = {}  # таблица стоимости удаления
    _update = {}  # таблица стоимости замены
    _insert_non_table_char = 0  # стоимость вставки не табличного символа
    _delete_non_table_char = 0  # стоимость удаления не табличного символа
    _update_non_table_char = 0  # стоимость замены не табличного символа

    # определение степени похожести строки (расстояние Левенштейна)
    @classmethod
    def compare_strings(cls, s1, s2, relative=True):
        s1 = s1.lower()
        s2 = s2.lower()

        m = len(s1)
        n = len(s2)

        # вспомогательные переменные
        a = 1
        b = 0

        # двумерный массив, в котором вычисляем разность
        lev_array = [0] * 2
        for i in range(2):
            lev_array[i] = [0] * (n + 1)

        for i in range(m + 1):
            for j in range(n + 1):
                if i != 0 or j != 0:
                    if i == 0:
                        # считаем стоимость вставки
                        try:
                            cost_insert = cls._insert[s2[j - 1]]
                        except KeyError:
                            cost_insert = cls._insert_non_table_char

                        lev_array[1][j] = lev_array[1][j - 1] + cost_insert

                    elif j == 0:
                        # считаем стоимость удаления
                        try:
                            cost_delete = cls._delete[s1[i - 1]]
                        except KeyError:
                            cost_delete = cls._delete_non_table_char

                        lev_array[a][0] = lev_array[b][0] + cost_delete

                    else:
                        c1 = s1[i - 1]
                        c2 = s2[j - 1]
                        if c1 != c2:
                            # считаем стоимость удаления
                            try:
                                cost_delete = cls._delete[c1]
                            except KeyError:
                                cost_delete = cls._delete_non_table_char

                            # считаем стоимость вставки
                            try:
                                cost_insert = cls._insert[c2]
                            except KeyError:
                                cost_insert = cls._insert_non_table_char

                            # считаем стоимость замены
                            try:
                                cost_update = cls._update[(c1, c2)]
                            except KeyError:
                                cost_update = cls._update_non_table_char

                            lev_array[a][j] = min(min(lev_array[b][j] + cost_delete,
                                                      lev_array[a][j - 1] + cost_insert),
                                                  lev_array[b][j - 1] + cost_update)
                        else:
                            lev_array[a][j] = lev_array[b][j - 1]
            a, b = b, a

        if relative and n == 0:
            return float('inf')

        return float(lev_array[b][n] / n) if relative else float(lev_array[b][n])

    @classmethod
    def _parse(cls, text, default=1):
        if len(text) == 0:
            return float(default)
        else:
            return float(text)

    # статический конструктор
    @classmethod
    def init(cls):
        # загружаем данные о символах
        data = list()
        chars = list()
        name = 'data/numeral_levenshtein_data.txt'  # путь к таблице весов символов

        file = open(name, "r", encoding="utf8")
        lines = file.readlines()

        row = 0
        for line in lines:
            data.append(line.strip(" \r\n").split("\t"))
            if row != 0:
                data[row].append('')
            row += 1
            file.close()
        file.close()

        # формируем таблицы
        n = len(data[0]) - 1
        row = 0
        min_cost = float('inf')  # PositiveInfinity
        max_cost = 0

        for var in data[row][1:]:
            chars.append(var)

        # INSERT
        row += 1
        for index, value in zip(chars, data[row][1:]):
            cls._insert[index] = cls._parse(value)
            if cls._parse(value) < min_cost:
                min_cost = cls._parse(value)
            if cls._parse(value) > max_cost:
                max_cost = cls._parse(value)

        # DELETE
        row += 1
        for index, value in zip(chars, data[row][1:]):
            cls._delete[index] = cls._parse(value)
            if cls._parse(value) < min_cost:
                min_cost = cls._parse(value)
            if cls._parse(value) > max_cost:
                max_cost = cls._parse(value)

        # UPDATE
        for i in range(n):
            row += 1
            for index, value in zip(chars, data[row][1:]):
                if chars[i] != index:
                    cls._update[(chars[i], index)] = cls._parse(value)
                    if cls._parse(value) < min_cost:
                        min_cost = cls._parse(value)
                    if cls._parse(value) > max_cost:
                        max_cost = cls._parse(value)

        # прочие показатели
        cls._insert_non_table_char = max_cost
        cls._delete_non_table_char = min_cost
        cls._update_non_table_char = min_cost
