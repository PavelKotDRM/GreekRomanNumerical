"""Тесты для класса GreekConvert"""
import pytest
from GreekRomanUtils.GreekRoman import GreekConvert


class TestGreekConvert:
    """Тесты для класса GreekConvert"""

    def test_convert_basic_numbers(self):
        """Тест конвертации основных чисел от 1 до 9"""
        converter = GreekConvert()
        assert converter.convert(1) == "α"
        assert converter.convert(2) == "β"
        assert converter.convert(3) == "γ"
        assert converter.convert(4) == "δ"
        assert converter.convert(5) == "ε"
        assert converter.convert(6) == "ϝ"
        assert converter.convert(7) == "ζ"
        assert converter.convert(8) == "η"
        assert converter.convert(9) == "θ"

    def test_convert_tens(self):
        """Тест конвертации десятков"""
        converter = GreekConvert()
        assert converter.convert(10) == "ι"
        assert converter.convert(20) == "κ"
        assert converter.convert(30) == "λ"
        assert converter.convert(50) == "ν"
        assert converter.convert(90) == "ϙ"

    def test_convert_hundreds(self):
        """Тест конвертации сотен"""
        converter = GreekConvert()
        assert converter.convert(100) == "ρ"
        assert converter.convert(200) == "σ"
        assert converter.convert(500) == "φ"
        assert converter.convert(900) == "ϡ"

    def test_convert_composite_numbers(self):
        """Тест конвертации составных чисел"""
        converter = GreekConvert()
        assert converter.convert(11) == "ια"
        assert converter.convert(15) == "ιε"
        assert converter.convert(99) == "ϙθ"
        assert converter.convert(123) == "ρκγ"
        assert converter.convert(456) == "υνϝ"
        assert converter.convert(999) == "ϡϙθ"

    def test_convert_thousands(self):
        """Тест конвертации тысяч"""
        converter = GreekConvert()
        result = converter.convert(1000)
        assert "_" in result
        assert result == "α_"

    def test_convert_capital_letters(self):
        """Тест конвертации с заглавными буквами"""
        converter = GreekConvert(capital=True)
        assert converter.convert(1) == "Α"
        assert converter.convert(2) == "Β"
        assert converter.convert(10) == "Ι"
        assert converter.convert(100) == "Ρ"

    def test_change_capital(self):
        """Тест смены регистра"""
        converter = GreekConvert()
        assert converter.convert(5) == "ε"
        converter.change_capital(True)
        assert converter.convert(5) == "Ε"

    def test_convert_to_arabic_basic(self):
        """Тест обратной конвертации основных чисел"""
        converter = GreekConvert()
        assert converter.convert_to_arabic("α") == 1
        assert converter.convert_to_arabic("β") == 2
        assert converter.convert_to_arabic("ι") == 10
        assert converter.convert_to_arabic("ρ") == 100

    def test_convert_to_arabic_composite(self):
        """Тест обратной конвертации составных чисел"""
        converter = GreekConvert()
        assert converter.convert_to_arabic("ια") == 11
        assert converter.convert_to_arabic("ρκγ") == 123
        assert converter.convert_to_arabic("ϡϙθ") == 999

    def test_convert_to_arabic_capital(self):
        """Тест обратной конвертации заглавных букв"""
        converter = GreekConvert(capital=True)
        assert converter.convert_to_arabic("Α") == 1
        assert converter.convert_to_arabic("Ρ") == 100

    def test_convert_to_arabic_thousands(self):
        """Тест обратной конвертации тысяч"""
        converter = GreekConvert()
        assert converter.convert_to_arabic("α_") == 1000

    def test_convert_position(self):
        """Тест позиционной конвертации"""
        converter = GreekConvert()
        result = converter.convert_position(1000)
        assert "~" in result or len(result) > 1

    def test_convert_position_to_arabic(self):
        """Тест обратной позиционной конвертации"""
        converter = GreekConvert()
        numeral = converter.convert_position(1234)
        result = converter.covert_to_position_arabic(numeral)
        assert result == 1234

    def test_unicode_to_name(self):
        """Тест конвертации Unicode в названия"""
        converter = GreekConvert()
        assert "alpha" in converter.unicode_to_name("α")
        assert "beta" in converter.unicode_to_name("β")
        assert "gamma" in converter.unicode_to_name("γ")

    def test_unicode_to_name_capital(self):
        """Тест конвертации Unicode заглавных букв в названия"""
        converter = GreekConvert(capital=True)
        assert "Alpha" in converter.unicode_to_name("Α")

    def test_name_to_unicode(self):
        """Тест конвертации названий в Unicode"""
        converter = GreekConvert()
        assert converter.name_to_unicode("alpha") == "α"
        assert converter.name_to_unicode("beta") == "β"
        assert converter.name_to_unicode("gamma") == "γ"

    def test_name_to_unicode_capital(self):
        """Тест конвертации названий заглавных букв в Unicode"""
        converter = GreekConvert()
        assert converter.name_to_unicode("Alpha") == "Α"

    def test_create_greek_number(self):
        """Тест создания греческого числа"""
        converter = GreekConvert()
        greek_num = converter.create_greek_number("ρκγ")
        assert greek_num.get_number() == 123

    def test_create_greek_number_positional(self):
        """Тест создания позиционного греческого числа"""
        converter = GreekConvert()
        greek_num = converter.create_greek_number("α~σλδ", positional=True)
        assert greek_num.get_number() == 1234

    def test_convert_to_arabic_invalid_symbol(self):
        """Тест обработки некорректных символов"""
        converter = GreekConvert()
        with pytest.raises(ValueError):
            converter.convert_to_arabic("x")

    def test_unicode_to_name_invalid_symbol(self):
        """Тест обработки некорректных символов в unicode_to_name"""
        converter = GreekConvert()
        with pytest.raises(ValueError):
            converter.unicode_to_name("x")

    def test_name_to_unicode_invalid_name(self):
        """Тест обработки некорректных названий"""
        converter = GreekConvert()
        with pytest.raises(ValueError):
            converter.name_to_unicode("invalid")
