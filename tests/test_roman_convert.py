"""Тесты для класса RomanConvert"""
import pytest
from GreekRomanUtils.GreekRoman import RomanConvert


class TestRomanConvert:
    """Тесты для класса RomanConvert"""

    def test_convert_basic_numbers(self):
        """Тест конвертации основных чисел"""
        converter = RomanConvert()
        assert converter.convert(1) == "I"
        assert converter.convert(2) == "II"
        assert converter.convert(3) == "III"
        assert converter.convert(4) == "IV"
        assert converter.convert(5) == "V"
        assert converter.convert(6) == "VI"
        assert converter.convert(7) == "VII"
        assert converter.convert(8) == "VIII"
        assert converter.convert(9) == "IX"

    def test_convert_tens(self):
        """Тест конвертации десятков"""
        converter = RomanConvert()
        assert converter.convert(10) == "X"
        assert converter.convert(20) == "XX"
        assert converter.convert(30) == "XXX"
        assert converter.convert(40) == "XL"
        assert converter.convert(50) == "L"
        assert converter.convert(60) == "LX"
        assert converter.convert(70) == "LXX"
        assert converter.convert(80) == "LXXX"
        assert converter.convert(90) == "XC"

    def test_convert_hundreds(self):
        """Тест конвертации сотен"""
        converter = RomanConvert()
        assert converter.convert(100) == "C"
        assert converter.convert(200) == "CC"
        assert converter.convert(300) == "CCC"
        assert converter.convert(400) == "CD"
        assert converter.convert(500) == "D"
        assert converter.convert(600) == "DC"
        assert converter.convert(700) == "DCC"
        assert converter.convert(800) == "DCCC"
        assert converter.convert(900) == "CM"

    def test_convert_thousands(self):
        """Тест конвертации тысяч"""
        converter = RomanConvert()
        assert converter.convert(1000) == "M"
        assert converter.convert(2000) == "MM"
        assert converter.convert(3000) == "MMM"

    def test_convert_composite_numbers(self):
        """Тест конвертации составных чисел"""
        converter = RomanConvert()
        assert converter.convert(11) == "XI"
        assert converter.convert(15) == "XV"
        assert converter.convert(27) == "XXVII"
        assert converter.convert(44) == "XLIV"
        assert converter.convert(99) == "XCIX"
        assert converter.convert(123) == "CXXIII"
        assert converter.convert(444) == "CDXLIV"
        assert converter.convert(888) == "DCCCLXXXVIII"
        assert converter.convert(1984) == "MCMLXXXIV"
        assert converter.convert(2024) == "MMXXIV"

    def test_convert_large_numbers(self):
        """Тест конвертации больших чисел"""
        converter = RomanConvert()
        assert converter.convert(5000) == "~V"
        assert converter.convert(10000) == "~X"
        assert converter.convert(50000) == "~L"
        assert converter.convert(100000) == "~C"
        assert converter.convert(500000) == "~D"
        assert converter.convert(1000000) == "~M"

    def test_convert_very_large_numbers(self):
        """Тест конвертации очень больших чисел"""
        converter = RomanConvert()
        result = converter.convert(123456)
        assert "~C" in result
        assert result == "~C~X~XMMMCDLVI"

    def test_convert_to_arabic_basic(self):
        """Тест обратной конвертации основных чисел"""
        converter = RomanConvert()
        assert converter.convert_to_arabic("I") == 1
        assert converter.convert_to_arabic("II") == 2
        assert converter.convert_to_arabic("III") == 3
        assert converter.convert_to_arabic("IV") == 4
        assert converter.convert_to_arabic("V") == 5
        assert converter.convert_to_arabic("IX") == 9

    def test_convert_to_arabic_tens(self):
        """Тест обратной конвертации десятков"""
        converter = RomanConvert()
        assert converter.convert_to_arabic("X") == 10
        assert converter.convert_to_arabic("XL") == 40
        assert converter.convert_to_arabic("L") == 50
        assert converter.convert_to_arabic("XC") == 90

    def test_convert_to_arabic_hundreds(self):
        """Тест обратной конвертации сотен"""
        converter = RomanConvert()
        assert converter.convert_to_arabic("C") == 100
        assert converter.convert_to_arabic("CD") == 400
        assert converter.convert_to_arabic("D") == 500
        assert converter.convert_to_arabic("CM") == 900

    def test_convert_to_arabic_thousands(self):
        """Тест обратной конвертации тысяч"""
        converter = RomanConvert()
        assert converter.convert_to_arabic("M") == 1000
        assert converter.convert_to_arabic("MM") == 2000

    def test_convert_to_arabic_composite(self):
        """Тест обратной конвертации составных чисел"""
        converter = RomanConvert()
        assert converter.convert_to_arabic("XI") == 11
        assert converter.convert_to_arabic("XV") == 15
        assert converter.convert_to_arabic("XXVII") == 27
        assert converter.convert_to_arabic("XLIV") == 44
        assert converter.convert_to_arabic("XCIX") == 99
        assert converter.convert_to_arabic("CXXIII") == 123
        assert converter.convert_to_arabic("MCMLXXXIV") == 1984

    def test_convert_to_arabic_large_numbers(self):
        """Тест обратной конвертации больших чисел"""
        converter = RomanConvert()
        assert converter.convert_to_arabic("~V") == 5000
        assert converter.convert_to_arabic("~X") == 10000
        assert converter.convert_to_arabic("~L") == 50000
        assert converter.convert_to_arabic("~C") == 100000

    def test_roundtrip_conversion(self):
        """Тест туда-обратно конвертации"""
        converter = RomanConvert()
        for number in [1, 5, 10, 50, 100, 500, 1000, 1234, 1999, 2024]:
            roman = converter.convert(number)
            back_to_arabic = converter.convert_to_arabic(roman)
            assert back_to_arabic == number

    def test_create_roman_number(self):
        """Тест создания римского числа"""
        converter = RomanConvert()
        roman_num = converter.create_roman_number(123)
        assert roman_num.get_number() == 123
        assert str(roman_num) == "CXXIII"

    def test_convert_invalid_type(self):
        """Тест обработки некорректного типа"""
        converter = RomanConvert()
        with pytest.raises(TypeError):
            converter.convert("123")

    def test_convert_to_arabic_invalid_symbol(self):
        """Тест обработки некорректных символов"""
        converter = RomanConvert()
        with pytest.raises(ValueError):
            converter.convert_to_arabic("ABC")

    def test_convert_zero(self):
        """Тест конвертации нуля (римляне не имели нуля)"""
        converter = RomanConvert()
        result = converter.convert(0)
        assert result == ""

    def test_convert_to_arabic_empty_string(self):
        """Тест обратной конвертации пустой строки"""
        converter = RomanConvert()
        assert converter.convert_to_arabic("") == 0
