import pytest

from GreekRomanUtils import _python_impl
from GreekRomanUtils.GreekRoman import GreekConvert, RomanConvert

rust_impl = pytest.importorskip("GreekRomanUtils._rust_impl")


@pytest.mark.parametrize("number", [0, 1, 4, 9, 44, 99, 944, 1984, 5000, 123456])
def test_roman_arabic_to_numeral_equivalence(number):
    assert rust_impl.arabic_to_roman(number) == _python_impl.arabic_to_roman(number)


@pytest.mark.parametrize("numeral", ["", "I", "IV", "MCMXCIX", "~C~X~XMMMCDLVI"])
def test_roman_numeral_to_arabic_equivalence(numeral):
    assert rust_impl.roman_to_arabic(numeral) == _python_impl.roman_to_arabic(numeral)


@pytest.mark.parametrize(
    "number",
    [0.5, 1.05, 1.25, -1.25, 2.0, 1e-7, -1e-7, 0.30000000000000004],
)
def test_roman_float_conversion_equivalence(number):
    numeral = _python_impl.arabic_to_roman(number)

    assert rust_impl.arabic_to_roman(number) == numeral
    assert _python_impl.roman_to_arabic(numeral) == number
    assert rust_impl.roman_to_arabic(numeral) == number


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


@pytest.mark.parametrize("positional", [False, True])
@pytest.mark.parametrize("capital", [False, True])
def test_large_greek_number_equivalence(positional, capital):
    number = 2**63
    numeral = _python_impl.arabic_to_greek(number, positional, capital)

    assert rust_impl.arabic_to_greek(number, positional, capital) == numeral
    assert rust_impl.greek_to_arabic(numeral, positional, capital) == number


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
    "number",
    [0.5, 1.05, 1.25, -1.25, 2.0, 1e-7, -1e-7, 0.30000000000000004],
)
@pytest.mark.parametrize("positional", [False, True])
@pytest.mark.parametrize("capital", [False, True])
def test_greek_float_conversion_equivalence(number, positional, capital):
    numeral = _python_impl.arabic_to_greek(number, positional, capital)

    assert rust_impl.arabic_to_greek(number, positional, capital) == numeral
    assert _python_impl.greek_to_arabic(numeral, positional, capital) == number
    assert rust_impl.greek_to_arabic(numeral, positional, capital) == number


@pytest.mark.parametrize("backend", [_python_impl, rust_impl], ids=["python", "rust"])
@pytest.mark.parametrize("number", [float("inf"), float("-inf"), float("nan")])
def test_non_finite_float_values_are_rejected(backend, number):
    with pytest.raises(ValueError):
        backend.arabic_to_roman(number)
    with pytest.raises(ValueError):
        backend.arabic_to_greek(number, positional=False, capital=False)


def test_public_converters_roundtrip_float_values():
    roman_converter = RomanConvert()
    roman_number = roman_converter.convert(1.05)
    assert str(roman_number) == "I.(0:V)"
    assert roman_number.get_number() == 1.05
    assert roman_converter.convert_to_arabic("I.(0:V)") == 1.05

    greek_converter = GreekConvert(positional=True, capital=True)
    greek_number = greek_converter.convert(1.05)
    assert str(greek_number) == "Α.(0:Ε)"
    assert isinstance(GreekConvert().convert(2.0).get_number(), float)
    assert greek_converter.convert_to_arabic("Α.(0:Ε)") == 1.05


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
