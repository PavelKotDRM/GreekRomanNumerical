"""Тесты для арифметических операций над числами"""
import pytest
from GreekRomanUtils.DataType.GreekRomanType import GreekNumber, RomanNumber


class TestGreekNumberArithmetic:
    """Тесты арифметических операций для GreekNumber"""

    def test_addition_with_greek_number(self):
        """Тест сложения двух греческих чисел"""
        num1 = GreekNumber(number=10)
        num2 = GreekNumber(number=5)
        result = num1 + num2
        assert result.get_number() == 15

    def test_addition_with_int(self):
        """Тест сложения греческого числа с int"""
        num = GreekNumber(number=10)
        result = num + 5
        assert result.get_number() == 15

    def test_subtraction_with_greek_number(self):
        """Тест вычитания двух греческих чисел"""
        num1 = GreekNumber(number=10)
        num2 = GreekNumber(number=5)
        result = num1 - num2
        assert result.get_number() == 5

    def test_subtraction_with_int(self):
        """Тест вычитания int из греческого числа"""
        num = GreekNumber(number=10)
        result = num - 5
        assert result.get_number() == 5

    def test_multiplication_with_greek_number(self):
        """Тест умножения двух греческих чисел"""
        num1 = GreekNumber(number=10)
        num2 = GreekNumber(number=5)
        result = num1 * num2
        assert result.get_number() == 50

    def test_multiplication_with_int(self):
        """Тест умножения греческого числа на int"""
        num = GreekNumber(number=10)
        result = num * 5
        assert result.get_number() == 50

    def test_division_with_greek_number(self):
        """Тест деления двух греческих чисел"""
        num1 = GreekNumber(number=10)
        num2 = GreekNumber(number=5)
        result = num1 / num2
        assert result.get_number() == 2

    def test_division_with_int(self):
        """Тест деления греческого числа на int"""
        num = GreekNumber(number=10)
        result = num / 5
        assert result.get_number() == 2

    def test_floor_division_with_greek_number(self):
        """Тест целочисленного деления двух греческих чисел"""
        num1 = GreekNumber(number=11)
        num2 = GreekNumber(number=5)
        result = num1 // num2
        assert result.get_number() == 2

    def test_floor_division_with_int(self):
        """Тест целочисленного деления греческого числа на int"""
        num = GreekNumber(number=11)
        result = num // 5
        assert result.get_number() == 2

    def test_modulo_with_greek_number(self):
        """Тест остатка от деления двух греческих чисел"""
        num1 = GreekNumber(number=11)
        num2 = GreekNumber(number=5)
        result = num1 % num2
        assert result.get_number() == 1

    def test_modulo_with_int(self):
        """Тест остатка от деления греческого числа на int"""
        num = GreekNumber(number=11)
        result = num % 5
        assert result.get_number() == 1

    def test_power_with_greek_number(self):
        """Тест возведения в степень двух греческих чисел"""
        num1 = GreekNumber(number=2)
        num2 = GreekNumber(number=3)
        result = num1 ** num2
        assert result.get_number() == 8

    def test_power_with_int(self):
        """Тест возведения греческого числа в степень int"""
        num = GreekNumber(number=2)
        result = num ** 3
        assert result.get_number() == 8

    def test_equality_with_greek_number(self):
        """Тест равенства двух греческих чисел"""
        num1 = GreekNumber(number=10)
        num2 = GreekNumber(number=10)
        assert num1 == num2

    def test_equality_with_int(self):
        """Тест равенства греческого числа и int"""
        num = GreekNumber(number=10)
        assert num == 10

    def test_inequality_with_greek_number(self):
        """Тест неравенства двух греческих чисел"""
        num1 = GreekNumber(number=10)
        num2 = GreekNumber(number=5)
        assert num1 != num2

    def test_inequality_with_int(self):
        """Тест неравенства греческого числа и int"""
        num = GreekNumber(number=10)
        assert num != 5

    def test_less_than_with_greek_number(self):
        """Тест меньше для двух греческих чисел"""
        num1 = GreekNumber(number=5)
        num2 = GreekNumber(number=10)
        assert num1 < num2

    def test_less_than_with_int(self):
        """Тест меньше для греческого числа и int"""
        num = GreekNumber(number=5)
        assert num < 10

    def test_less_equal_with_greek_number(self):
        """Тест меньше или равно для двух греческих чисел"""
        num1 = GreekNumber(number=5)
        num2 = GreekNumber(number=10)
        assert num1 <= num2
        num3 = GreekNumber(number=10)
        assert num2 <= num3

    def test_less_equal_with_int(self):
        """Тест меньше или равно для греческого числа и int"""
        num = GreekNumber(number=5)
        assert num <= 10
        assert num <= 5

    def test_greater_than_with_greek_number(self):
        """Тест больше для двух греческих чисел"""
        num1 = GreekNumber(number=10)
        num2 = GreekNumber(number=5)
        assert num1 > num2

    def test_greater_than_with_int(self):
        """Тест больше для греческого числа и int"""
        num = GreekNumber(number=10)
        assert num > 5

    def test_greater_equal_with_greek_number(self):
        """Тест больше или равно для двух греческих чисел"""
        num1 = GreekNumber(number=10)
        num2 = GreekNumber(number=5)
        assert num1 >= num2
        num3 = GreekNumber(number=10)
        assert num1 >= num3

    def test_greater_equal_with_int(self):
        """Тест больше или равно для греческого числа и int"""
        num = GreekNumber(number=10)
        assert num >= 5
        assert num >= 10

    def test_iadd_with_greek_number(self):
        """Тест оператора += с греческим числом"""
        num1 = GreekNumber(number=10)
        num2 = GreekNumber(number=5)
        num1 += num2
        assert num1.get_number() == 15

    def test_iadd_with_int(self):
        """Тест оператора += с int"""
        num = GreekNumber(number=10)
        num += 5
        assert num.get_number() == 15

    def test_isub_with_greek_number(self):
        """Тест оператора -= с греческим числом"""
        num1 = GreekNumber(number=10)
        num2 = GreekNumber(number=5)
        num1 -= num2
        assert num1.get_number() == 5

    def test_isub_with_int(self):
        """Тест оператора -= с int"""
        num = GreekNumber(number=10)
        num -= 5
        assert num.get_number() == 5

    def test_imul_with_greek_number(self):
        """Тест оператора *= с греческим числом"""
        num1 = GreekNumber(number=10)
        num2 = GreekNumber(number=5)
        num1 *= num2
        assert num1.get_number() == 50

    def test_imul_with_int(self):
        """Тест оператора *= с int"""
        num = GreekNumber(number=10)
        num *= 5
        assert num.get_number() == 50

    def test_itruediv_with_greek_number(self):
        """Тест оператора /= с греческим числом"""
        num1 = GreekNumber(number=10)
        num2 = GreekNumber(number=5)
        num1 /= num2
        assert num1.get_number() == 2

    def test_itruediv_with_int(self):
        """Тест оператора /= с int"""
        num = GreekNumber(number=10)
        num /= 5
        assert num.get_number() == 2

    def test_ifloordiv_with_greek_number(self):
        """Тест оператора //= с греческим числом"""
        num1 = GreekNumber(number=11)
        num2 = GreekNumber(number=5)
        num1 //= num2
        assert num1.get_number() == 2

    def test_ifloordiv_with_int(self):
        """Тест оператора //= с int"""
        num = GreekNumber(number=11)
        num //= 5
        assert num.get_number() == 2

    def test_imod_with_greek_number(self):
        """Тест оператора %= с греческим числом"""
        num1 = GreekNumber(number=11)
        num2 = GreekNumber(number=5)
        num1 %= num2
        assert num1.get_number() == 1

    def test_imod_with_int(self):
        """Тест оператора %= с int"""
        num = GreekNumber(number=11)
        num %= 5
        assert num.get_number() == 1

    def test_ipow_with_greek_number(self):
        """Тест оператора **= с греческим числом"""
        num1 = GreekNumber(number=2)
        num2 = GreekNumber(number=3)
        num1 **= num2
        assert num1.get_number() == 8

    def test_ipow_with_int(self):
        """Тест оператора **= с int"""
        num = GreekNumber(number=2)
        num **= 3
        assert num.get_number() == 8

    def test_negation(self):
        """Тест унарного минуса"""
        num = GreekNumber(number=10)
        result = -num
        assert result.get_number() == -10

    def test_positive(self):
        """Тест унарного плюса"""
        num = GreekNumber(number=10)
        result = +num
        assert result.get_number() == 10

    def test_negation_none_value(self):
        """Тест унарного минуса для None"""
        num = GreekNumber(number=10)
        num._number = None
        with pytest.raises(TypeError):
            -num

    def test_positive_none_value(self):
        """Тест унарного плюса для None"""
        num = GreekNumber(number=10)
        num._number = None
        with pytest.raises(TypeError):
            +num

    def test_unsupported_operand_type(self):
        """Тест неподдерживаемого типа операнда"""
        num = GreekNumber(number=10)
        with pytest.raises(TypeError):
            num + "5"


class TestRomanNumberArithmetic:
    """Тесты арифметических операций для RomanNumber"""

    def test_addition_with_roman_number(self):
        """Тест сложения двух римских чисел"""
        num1 = RomanNumber(10)
        num2 = RomanNumber(5)
        result = num1 + num2
        assert result.get_number() == 15

    def test_addition_with_int(self):
        """Тест сложения римского числа с int"""
        num = RomanNumber(10)
        result = num + 5
        assert result.get_number() == 15

    def test_subtraction_with_roman_number(self):
        """Тест вычитания двух римских чисел"""
        num1 = RomanNumber(10)
        num2 = RomanNumber(5)
        result = num1 - num2
        assert result.get_number() == 5

    def test_multiplication_with_roman_number(self):
        """Тест умножения двух римских чисел"""
        num1 = RomanNumber(10)
        num2 = RomanNumber(5)
        result = num1 * num2
        assert result.get_number() == 50

    def test_division_with_roman_number(self):
        """Тест деления двух римских чисел"""
        num1 = RomanNumber(10)
        num2 = RomanNumber(5)
        result = num1 / num2
        assert result.get_number() == 2

    def test_equality_with_roman_number(self):
        """Тест равенства двух римских чисел"""
        num1 = RomanNumber(10)
        num2 = RomanNumber(10)
        assert num1 == num2

    def test_equality_with_int(self):
        """Тест равенства римского числа и int"""
        num = RomanNumber(10)
        assert num == 10

    def test_less_than_with_roman_number(self):
        """Тест меньше для двух римских чисел"""
        num1 = RomanNumber(5)
        num2 = RomanNumber(10)
        assert num1 < num2

    def test_greater_than_with_roman_number(self):
        """Тест больше для двух римских чисел"""
        num1 = RomanNumber(10)
        num2 = RomanNumber(5)
        assert num1 > num2

    def test_iadd_with_int(self):
        """Тест оператора += с int для римского числа"""
        num = RomanNumber(10)
        num += 5
        assert num.get_number() == 15

    def test_negation_roman(self):
        """Тест унарного минуса для римского числа"""
        num = RomanNumber(10)
        result = -num
        assert result.get_number() == -10


class TestMixedArithmetic:
    """Тесты смешанных арифметических операций"""

    def test_greek_and_roman_addition(self):
        """Тест сложения греческого и римского чисел"""
        greek = GreekNumber(number=10)
        roman = RomanNumber(5)
        # Они оба наследуются от BaseNumberVirtual
        result = greek + roman
        assert result.get_number() == 15

    def test_complex_expression(self):
        """Тест сложного выражения"""
        num1 = GreekNumber(number=10)
        num2 = GreekNumber(number=5)
        num3 = GreekNumber(number=2)
        result = (num1 + num2) * num3
        assert result.get_number() == 30

    def test_chained_operations(self):
        """Тест цепочки операций"""
        num = GreekNumber(number=10)
        num += 5
        num *= 2
        num -= 10
        assert num.get_number() == 20

    def test_comparison_chain(self):
        """Тест цепочки сравнений"""
        num1 = GreekNumber(number=5)
        num2 = GreekNumber(number=10)
        num3 = GreekNumber(number=15)
        assert num1 < num2 < num3

    def test_division_with_float_result(self):
        """Тест деления с дробным результатом"""
        num1 = GreekNumber(number=10)
        num2 = GreekNumber(number=3)
        result = num1 / num2
        # Результат должен быть преобразован в int
        assert isinstance(result.get_number(), int)

    def test_positional_preservation_in_operations(self):
        """Тест сохранения позиционности в операциях"""
        num1 = GreekNumber(number=1000, positional=True)
        num2 = GreekNumber(number=1000, positional=True)
        result = num1 + num2
        # Проверяем, что результат также позиционный
        assert result.get_positional() == True

    def test_capital_preservation_in_operations(self):
        """Тест сохранения регистра в операциях"""
        num1 = GreekNumber(number=10, capital=True)
        num2 = GreekNumber(number=5, capital=True)
        result = num1 + num2
        # Проверяем, что результат также с заглавными буквами
        assert result.get_capital() == True
