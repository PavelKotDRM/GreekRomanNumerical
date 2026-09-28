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


class TestNumberEdgeCases:
    @pytest.mark.parametrize("number_type", [GreekNumber, RomanNumber])
    @pytest.mark.parametrize(
        ("dividend", "divisor", "expected"),
        [(7, 3, 2), (-7, 3, -2), (7, -3, -2), (-7, -3, 2)],
    )
    def test_division_truncates_toward_zero(self, number_type, dividend, divisor, expected):
        result = number_type(dividend) / number_type(divisor)

        assert result.get_number() == expected

    @pytest.mark.parametrize("number_type", [GreekNumber, RomanNumber])
    def test_division_by_zero_raises(self, number_type):
        with pytest.raises(ZeroDivisionError):
            number_type(7) / 0

    @pytest.mark.parametrize(
        ("number_type", "numeral"),
        [(GreekNumber, "ε"), (RomanNumber, "V")],
    )
    def test_equality_with_numeral_string(self, number_type, numeral):
        assert number_type(5) == numeral


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

    def test_division_preserves_large_integer_precision(self):
        number = 10**400

        assert (GreekNumber(number) / 3).get_number() == number // 3
        assert (GreekNumber(-number) / 3).get_number() == -(number // 3)

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

    def test_inplace_operations_refresh_string_value(self):
        greek = GreekNumber(number=10)
        greek += 5
        assert (greek.get_number(), str(greek)) == (15, "ιε")

        roman = RomanNumber(10)
        roman += 5
        assert (roman.get_number(), str(roman)) == (15, "XV")

    @pytest.mark.parametrize(
        ("number_type", "expected_numeral"),
        [(GreekNumber, "α.25"), (RomanNumber, "I.25")],
    )
    def test_float_values_preserve_fraction_and_numeral(self, number_type, expected_numeral):
        number = number_type(1.25)

        assert number.get_number() == 1.25
        assert str(number) == expected_numeral

    @pytest.mark.parametrize("number_type", [GreekNumber, RomanNumber])
    def test_float_operands_preserve_fraction(self, number_type):
        number = number_type(1.5)

        assert (number + 0.25).get_number() == 1.75
        assert (number * 2.0).get_number() == 3.0
        assert (number / 2.0).get_number() == 0.75

    def test_integer_division_keeps_truncating_behavior(self):
        assert (GreekNumber(10) / 3).get_number() == 3
