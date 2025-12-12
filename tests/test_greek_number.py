"""Тесты для класса GreekNumber"""
import pytest
from GreekRomanUtils.DataType.GreekRomanType import GreekNumber


class TestGreekNumber:
    """Тесты для класса GreekNumber"""

    def test_init_with_number(self):
        """Тест инициализации с числом"""
        greek = GreekNumber(number=5)
        assert greek.get_number() == 5
        assert str(greek) == "ε"

    def test_init_with_value(self):
        """Тест инициализации со значением"""
        greek = GreekNumber(value="ε")
        assert greek.get_number() == 5
        assert str(greek) == "ε"

    def test_init_no_parameters(self):
        """Тест инициализации без параметров"""
        with pytest.raises(ValueError):
            GreekNumber()

    def test_str_representation(self):
        """Тест строкового представления"""
        greek = GreekNumber(number=123)
        assert str(greek) == "ρκγ"

    def test_repr_representation(self):
        """Тест repr представления"""
        greek = GreekNumber(number=123)
        assert repr(greek) == "ρκγ"

    def test_len(self):
        """Тест длины"""
        greek = GreekNumber(number=123)
        assert len(greek) == 3

    def test_iter(self):
        """Тест итерации"""
        greek = GreekNumber(number=123)
        chars = list(greek)
        assert len(chars) == 3
        assert chars[0] == "ρ"

    def test_get_str(self):
        """Тест получения строки с названиями"""
        greek = GreekNumber(number=5)
        result = greek.get_str()
        assert "epsilon" in result

    def test_set_number(self):
        """Тест установки числа"""
        greek = GreekNumber(number=5)
        greek.set_number(10)
        assert greek.get_number() == 10
        assert str(greek) == "ι"

    def test_set_positional(self):
        """Тест установки позиционного режима"""
        greek = GreekNumber(number=1000)
        greek.set_positional(True)
        result = str(greek)
        assert "~" in result or len(result) > 1

    def test_set_capital(self):
        """Тест установки заглавных букв"""
        greek = GreekNumber(number=5)
        greek.set_capital(True)
        assert str(greek) == "Ε"

    def test_get_positional(self):
        """Тест получения флага позиционности"""
        greek = GreekNumber(number=5, positional=False)
        assert greek.get_positional() == False
        greek.set_positional(True)
        assert greek.get_positional() == True

    def test_get_capital(self):
        """Тест получения флага заглавных букв"""
        greek = GreekNumber(number=5, capital=False)
        assert greek.get_capital() == False
        greek.set_capital(True)
        assert greek.get_capital() == True

    def test_capital_initialization(self):
        """Тест инициализации с заглавными буквами"""
        greek = GreekNumber(number=5, capital=True)
        assert str(greek) == "Ε"

    def test_positional_initialization(self):
        """Тест инициализации с позиционным режимом"""
        greek = GreekNumber(number=1234, positional=True)
        result = str(greek)
        assert "~" in result

    def test_convert_basic_numbers(self):
        """Тест конвертации основных чисел"""
        for i in range(1, 10):
            greek = GreekNumber(number=i)
            assert greek.get_number() == i

    def test_convert_composite_numbers(self):
        """Тест конвертации составных чисел"""
        test_cases = [11, 15, 99, 123, 456, 789, 999]
        for num in test_cases:
            greek = GreekNumber(number=num)
            assert greek.get_number() == num

    def test_convert_thousands(self):
        """Тест конвертации тысяч"""
        greek = GreekNumber(number=1000)
        result = str(greek)
        assert "_" in result

    def test_convert_large_numbers(self):
        """Тест конвертации больших чисел"""
        greek = GreekNumber(number=5000)
        result = str(greek)
        assert "_" in result

    def test_roundtrip_conversion(self):
        """Тест туда-обратно конвертации"""
        for number in [1, 5, 10, 50, 100, 500, 999, 1234]:
            greek = GreekNumber(number=number)
            value_str = str(greek)
            greek2 = GreekNumber(value=value_str)
            assert greek2.get_number() == number

    def test_positional_roundtrip(self):
        """Тест позиционной туда-обратно конвертации"""
        for number in [1000, 5000, 10000, 123456]:
            greek = GreekNumber(number=number, positional=True)
            value_str = str(greek)
            greek2 = GreekNumber(value=value_str, positional=True)
            assert greek2.get_number() == number

    def test_invalid_value_type(self):
        """Тест некорректного типа значения"""
        with pytest.raises(TypeError):
            GreekNumber(number="123")

    def test_invalid_symbol_in_value(self):
        """Тест некорректного символа в значении"""
        with pytest.raises(ValueError):
            GreekNumber(value="xyz")

    def test_get_str_with_capital(self):
        """Тест get_str с заглавными буквами"""
        greek = GreekNumber(number=5, capital=True)
        result = greek.get_str()
        assert "Epsilon" in result

    def test_convert_arabic_to_greek(self):
        """Тест приватного метода конвертации"""
        greek = GreekNumber(number=123)
        assert str(greek) == "ρκγ"

    def test_convert_greek_to_arabic(self):
        """Тест приватного метода обратной конвертации"""
        greek = GreekNumber(value="ρκγ")
        assert greek.get_number() == 123

    def test_positional_conversion(self):
        """Тест позиционной конвертации"""
        greek = GreekNumber(number=1234, positional=True)
        result = str(greek)
        # Проверяем, что результат содержит разделитель или имеет правильную структуру
        assert len(result) > 0
        # Обратная конвертация
        greek2 = GreekNumber(value=result, positional=True)
        assert greek2.get_number() == 1234

    def test_multiple_thousands(self):
        """Тест конвертации с несколькими тысячами"""
        greek = GreekNumber(number=3000)
        result = str(greek)
        assert "_" in result

    def test_complex_number_with_thousands(self):
        """Тест сложного числа с тысячами"""
        greek = GreekNumber(number=2345)
        result = str(greek)
        assert "_" in result
        # Обратная конвертация
        greek2 = GreekNumber(value=result)
        assert greek2.get_number() == 2345

    def test_capital_conversion_consistency(self):
        """Тест согласованности конвертации заглавных букв"""
        for i in [1, 10, 100]:
            greek_lower = GreekNumber(number=i, capital=False)
            greek_upper = GreekNumber(number=i, capital=True)
            assert str(greek_lower).lower() == str(greek_upper).lower()

    def test_len_none_value(self):
        """Тест длины при None значении"""
        greek = GreekNumber(number=5)
        greek._value = None
        with pytest.raises(TypeError):
            len(greek)

    def test_iter_none_value(self):
        """Тест итерации при None значении"""
        greek = GreekNumber(number=5)
        greek._value = None
        with pytest.raises(TypeError):
            list(greek)

    def test_get_str_invalid_type(self):
        """Тест get_str с некорректным типом"""
        greek = GreekNumber(number=5)
        greek._value = 123
        with pytest.raises(TypeError):
            greek.get_str()

    def test_update_value_on_set_number(self):
        """Тест обновления значения при установке числа"""
        greek = GreekNumber(number=5)
        original_value = str(greek)
        greek.set_number(10)
        new_value = str(greek)
        assert original_value != new_value
        assert new_value == "ι"
