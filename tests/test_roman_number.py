"""Тесты для класса RomanNumber"""
import pytest
from GreekRomanUtils.DataType.GreekRomanType import RomanNumber


class TestRomanNumber:
    """Тесты для класса RomanNumber"""

    def test_init_basic(self):
        """Тест базовой инициализации"""
        roman = RomanNumber(5)
        assert roman.get_number() == 5
        assert str(roman) == "V"

    def test_init_no_number(self):
        """Тест инициализации без числа"""
        with pytest.raises(ValueError):
            RomanNumber(None)

    def test_str_representation(self):
        """Тест строкового представления"""
        roman = RomanNumber(123)
        assert str(roman) == "CXXIII"

    def test_repr_representation(self):
        """Тест repr представления"""
        roman = RomanNumber(123)
        assert repr(roman) == "CXXIII"

    def test_get_number(self):
        """Тест получения числа"""
        roman = RomanNumber(456)
        assert roman.get_number() == 456

    def test_get_value(self):
        """Тест получения значения"""
        roman = RomanNumber(123)
        assert roman.get_value() == "CXXIII"

    def test_len(self):
        """Тест длины"""
        roman = RomanNumber(123)
        assert len(roman) > 0

    def test_iter(self):
        """Тест итерации"""
        roman = RomanNumber(123)
        parts = list(roman)
        assert len(parts) > 0

    def test_getitem(self):
        """Тест получения элемента по индексу"""
        roman = RomanNumber(123)
        first_part = roman[0]
        assert first_part is not None

    def test_convert_single_digits(self):
        """Тест конвертации единичных цифр"""
        assert str(RomanNumber(1)) == "I"
        assert str(RomanNumber(2)) == "II"
        assert str(RomanNumber(3)) == "III"
        assert str(RomanNumber(4)) == "IV"
        assert str(RomanNumber(5)) == "V"
        assert str(RomanNumber(6)) == "VI"
        assert str(RomanNumber(7)) == "VII"
        assert str(RomanNumber(8)) == "VIII"
        assert str(RomanNumber(9)) == "IX"

    def test_convert_tens(self):
        """Тест конвертации десятков"""
        assert str(RomanNumber(10)) == "X"
        assert str(RomanNumber(20)) == "XX"
        assert str(RomanNumber(30)) == "XXX"
        assert str(RomanNumber(40)) == "XL"
        assert str(RomanNumber(50)) == "L"
        assert str(RomanNumber(60)) == "LX"
        assert str(RomanNumber(70)) == "LXX"
        assert str(RomanNumber(80)) == "LXXX"
        assert str(RomanNumber(90)) == "XC"

    def test_convert_hundreds(self):
        """Тест конвертации сотен"""
        assert str(RomanNumber(100)) == "C"
        assert str(RomanNumber(200)) == "CC"
        assert str(RomanNumber(300)) == "CCC"
        assert str(RomanNumber(400)) == "CD"
        assert str(RomanNumber(500)) == "D"
        assert str(RomanNumber(600)) == "DC"
        assert str(RomanNumber(700)) == "DCC"
        assert str(RomanNumber(800)) == "DCCC"
        assert str(RomanNumber(900)) == "CM"

    def test_convert_thousands(self):
        """Тест конвертации тысяч"""
        assert str(RomanNumber(1000)) == "M"
        assert str(RomanNumber(2000)) == "MM"
        assert str(RomanNumber(3000)) == "MMM"

    def test_convert_composite_numbers(self):
        """Тест конвертации составных чисел"""
        assert str(RomanNumber(11)) == "XI"
        assert str(RomanNumber(15)) == "XV"
        assert str(RomanNumber(27)) == "XXVII"
        assert str(RomanNumber(44)) == "XLIV"
        assert str(RomanNumber(99)) == "XCIX"
        assert str(RomanNumber(123)) == "CXXIII"
        assert str(RomanNumber(444)) == "CDXLIV"
        assert str(RomanNumber(888)) == "DCCCLXXXVIII"

    def test_convert_year_numbers(self):
        """Тест конвертации годов"""
        assert str(RomanNumber(1984)) == "MCMLXXXIV"
        assert str(RomanNumber(2024)) == "MMXXIV"
        assert str(RomanNumber(1999)) == "MCMXCIX"

    def test_convert_large_numbers(self):
        """Тест конвертации больших чисел"""
        roman = RomanNumber(5000)
        result = str(roman)
        assert "~" in result or "M" in result

    def test_convert_very_large_numbers(self):
        """Тест конвертации очень больших чисел"""
        roman = RomanNumber(100000)
        result = str(roman)
        assert "~" in result

    def test_invalid_type(self):
        """Тест некорректного типа"""
        with pytest.raises(TypeError):
            RomanNumber("123")

    def test_iter_none_value(self):
        """Тест итерации при None значении"""
        roman = RomanNumber(5)
        roman._value = None
        with pytest.raises(TypeError):
            list(roman)

    def test_getitem_none_value(self):
        """Тест получения элемента при None значении"""
        roman = RomanNumber(5)
        roman._value = None
        with pytest.raises(TypeError):
            _ = roman[0]

    def test_len_none_value(self):
        """Тест длины при None значении"""
        roman = RomanNumber(5)
        roman._value = None
        with pytest.raises(TypeError):
            len(roman)

    def test_get_value_list(self):
        """Тест get_value когда значение - список"""
        roman = RomanNumber(123)
        value = roman.get_value()
        assert isinstance(value, str)
        assert value == "CXXIII"

    def test_str_with_none_value(self):
        """Тест строкового представления при None значении"""
        roman = RomanNumber(5)
        roman._value = None
        assert str(roman) == "None"

    def test_repr_with_none_value(self):
        """Тест repr при None значении"""
        roman = RomanNumber(5)
        roman._value = None
        assert repr(roman) == "None"

    def test_conversion_consistency(self):
        """Тест согласованности конвертации"""
        for num in [1, 5, 10, 50, 100, 500, 1000]:
            roman = RomanNumber(num)
            assert roman.get_number() == num
            assert len(str(roman)) > 0

    def test_special_combinations(self):
        """Тест специальных комбинаций"""
        # Тест субтрактивной нотации
        assert str(RomanNumber(4)) == "IV"
        assert str(RomanNumber(9)) == "IX"
        assert str(RomanNumber(40)) == "XL"
        assert str(RomanNumber(90)) == "XC"
        assert str(RomanNumber(400)) == "CD"
        assert str(RomanNumber(900)) == "CM"

    def test_sequential_numbers(self):
        """Тест последовательных чисел"""
        for i in range(1, 100):
            roman = RomanNumber(i)
            assert roman.get_number() == i
            assert len(str(roman)) > 0

    def test_value_structure(self):
        """Тест структуры значения"""
        roman = RomanNumber(123)
        # Значение должно быть списком
        assert hasattr(roman, '_value')
        assert roman._value is not None

    def test_large_number_with_macron(self):
        """Тест больших чисел с макроном"""
        roman = RomanNumber(10000)
        result = str(roman)
        assert "~" in result
        assert "X" in result
