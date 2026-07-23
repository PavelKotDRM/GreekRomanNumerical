import pytest

from GreekRomanUtils import _python_impl

rust_impl = pytest.importorskip("GreekRomanUtils._rust_impl")


@pytest.mark.parametrize("number", [0, 1, 4, 9, 44, 99, 944, 1984, 5000, 123456])
def test_roman_arabic_to_numeral_equivalence(number):
    assert rust_impl.arabic_to_roman(number) == _python_impl.arabic_to_roman(number)


@pytest.mark.parametrize("numeral", ["", "I", "IV", "MCMXCIX", "~C~X~XMMMCDLVI"])
def test_roman_numeral_to_arabic_equivalence(numeral):
    assert rust_impl.roman_to_arabic(numeral) == _python_impl.roman_to_arabic(numeral)


@pytest.mark.parametrize(
    "number,positional,capital",
    [
        (0, False, False),
        (1, False, False),
        (123, False, False),
        (1234, True, False),
        (5000, False, False),
        (123456, True, True),
    ],
)
def test_greek_arabic_to_numeral_equivalence(number, positional, capital):
    assert rust_impl.arabic_to_greek(number, positional, capital) == _python_impl.arabic_to_greek(
        number, positional, capital
    )


@pytest.mark.parametrize(
    "numeral,positional,capital",
    [
        ("", False, False),
        ("α", False, False),
        ("ρκγ", False, False),
        ("α_", False, False),
        ("α~σλδ", True, False),
        ("Α~ΣΛΔ", True, True),
    ],
)
def test_greek_numeral_to_arabic_equivalence(numeral, positional, capital):
    assert rust_impl.greek_to_arabic(numeral, positional, capital) == _python_impl.greek_to_arabic(
        numeral, positional, capital
    )


@pytest.mark.parametrize(
    "roman,greek",
    [
        ("ABC", "xyz"),
        ("@", "foo"),
    ],
)
def test_invalid_input_error_equivalence(roman, greek):
    with pytest.raises(ValueError):
        rust_impl.roman_to_arabic(roman)
    with pytest.raises(ValueError):
        _python_impl.roman_to_arabic(roman)

    with pytest.raises(ValueError):
        rust_impl.greek_to_arabic(greek, False, False)
    with pytest.raises(ValueError):
        _python_impl.greek_to_arabic(greek, False, False)
