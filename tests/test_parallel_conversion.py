import pytest

from GreekRomanUtils import _python_impl
from GreekRomanUtils.GreekRoman import GreekConvert, RomanConvert


def test_python_backend_parallel_api_converts_iterables():
    assert _python_impl.arabic_to_roman_many(number for number in [4, 2024, 1.25]) == [
        "IV",
        "MMXXIV",
        "I.(II:V)",
    ]
    assert _python_impl.arabic_to_greek_many([4, 1234], positional=False, capital=False) == [
        "δ",
        "α_σλδ",
    ]


def test_converter_batch_methods():
    roman = RomanConvert()
    greek = GreekConvert(positional=True, capital=True)

    assert roman.convert_many([4, 2024]) == ["IV", "MMXXIV"]
    assert greek.convert_many(iter([4, 1234])) == ["Δ", "Α~ΣΛΔ"]


def test_rust_backend_parallel_api_matches_single_conversions():
    rust_impl = pytest.importorskip("GreekRomanUtils._rust_impl")

    numbers = [4, 2024, 1.25]
    assert rust_impl.arabic_to_roman_many(numbers) == [
        rust_impl.arabic_to_roman(number) for number in numbers
    ]
    assert rust_impl.arabic_to_greek_many(numbers, positional=True, capital=True) == [
        rust_impl.arabic_to_greek(number, positional=True, capital=True)
        for number in numbers
    ]


def test_batch_conversion_errors_are_not_silently_discarded():
    with pytest.raises(ValueError):
        RomanConvert().convert_many([4, float("inf")])
