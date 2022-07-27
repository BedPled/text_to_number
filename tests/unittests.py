import unittest
from russian_number import RussianNumber
from numeral_levenshtein import NumeralLevenshtein


class TestStringMethods(unittest.TestCase):

    def test_simple_1(self):
        self.assertEqual(RussianNumber.text_to_number("сто двадцать семь"), 127)
        self.assertEqual(RussianNumber.text_to_number("тридцать три тысячи"), 33000)
        self.assertEqual(RussianNumber.text_to_number("сто двадцать три тысячи двести тридцать шесть"), 123236)

    def test_simple_2(self):
        self.assertEqual(RussianNumber.text_to_number("сто дватцать три тысячи двести тритцать шесть"), 123236)
        self.assertEqual(RussianNumber.text_to_number("нуль"), 0)
        self.assertEqual(RussianNumber.text_to_number("адин"), 1)
        self.assertEqual(RussianNumber.text_to_number("0дин"), 1)
        self.assertEqual(RussianNumber.text_to_number("двинацать"), 12)
        self.assertEqual(RussianNumber.text_to_number("двапать"), 20)
        self.assertEqual(RussianNumber.text_to_number("Двадиать"), 20)

    def test_hard(self):
        self.assertEqual(RussianNumber.text_to_number("двапать одина"), 21)
        self.assertEqual(RussianNumber.text_to_number("Тридпать четыре"), 34)
        self.assertEqual(RussianNumber.text_to_number("сто двадцать три"), 123)
        self.assertEqual(RussianNumber.text_to_number("Одина тысяча двести"), 1200)
        # self.assertEqual(RussianNumber.text_to_number("Два миллиарда сто сорок семь миллионов четыреста восемьдесят три тысячи шестьсот сорок семь"), 2147483647)

    def test_merger(self):
        self.assertEqual(RussianNumber.text_to_number("двадцатьоди"), 21)
        self.assertEqual(RussianNumber.text_to_number("двапатьодин"), 21)
        self.assertEqual(RussianNumber.text_to_number("стопть"), 105)
        self.assertEqual(RussianNumber.text_to_number("дветысячи"), 2000)
        self.assertEqual(RussianNumber.text_to_number("дветысячистопять"), 2105)

    def test_hard_stupid(self):
        self.assertEqual(RussianNumber.text_to_number("симнацать"), 17)
        self.assertEqual(RussianNumber.text_to_number("сто двацать пить"), 125)
        self.assertEqual(RussianNumber.text_to_number("тритысчи стоопятьдесят"), 3150)
        # self.assertEqual(RussianNumber.text_to_number("дивяноост семь"), 97)
        # self.assertEqual(RussianNumber.text_to_number("двести пяцят шесть"), 256)
        # self.assertEqual(RussianNumber.text_to_number("тыща сто адын"), 1101)
        # self.assertEqual(RussianNumber.text_to_number("две тыщи пяццот"), 2500)

    # def test_ ... (self):
        # self.assertEqual(RussianNumber.text_to_number(""), ...)


if __name__ == '__main__':
    unittest.main()
