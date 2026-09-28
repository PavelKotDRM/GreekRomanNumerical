import pytest

from GreekRomanUtils import _python_impl
from GreekRomanUtils.GreekRoman import GreekConvert, RomanConvert

rust_impl = pytest.importorskip("GreekRomanUtils._rust_impl")


@pytest.mark.parametrize("number", [0, 1, 4, 9, 44, 99, 944, 1984, 5000, 123456])
def test_roman_arabic_to_numeral_equivalence(number):
    assert rust_impl.arabic_to_roman(number) == _python_impl.arabic_to_roman(number)


@pytest.mark.parametrize("number", [-1, -1234, -123456])
@pytest.mark.parametrize("positional", [False, True])
@pytest.mark.parametrize("capital", [False, True])
def test_negative_integer_conversion_round_trips(number, positional, capital):
    for backend in (_python_impl, rust_impl):
        roman = backend.arabic_to_roman(number)
        greek = backend.arabic_to_greek(number, positional, capital)

        assert roman.startswith("-")
        assert greek.startswith("-")
        assert backend.roman_to_arabic(roman) == number
        assert backend.greek_to_arabic(greek, positional, capital) == number


@pytest.mark.parametrize("numeral", ["", "I", "IV", "MCMXCIX", "~C~X~XMMMCDLVI"])
def test_roman_numeral_to_arabic_equivalence(numeral):
    assert rust_impl.roman_to_arabic(numeral) == _python_impl.roman_to_arabic(numeral)


@pytest.mark.parametrize("backend", [_python_impl, rust_impl], ids=["python", "rust"])
@pytest.mark.parametrize("numeral", ["I.(0:V)", "I.(_:V)"])
def test_roman_fractional_zero_markers_are_accepted(backend, numeral):
    assert backend.roman_to_arabic(numeral) == 1.05


@pytest.mark.parametrize(
    "number",
    [0.5, 1.05, 1.25, -1.25, 2.0, 1e-7, -1e-7, 0.30000000000000004],
)
def test_roman_float_conversion_equivalence(number):
    numeral = _python_impl.arabic_to_roman(number)

    assert rust_impl.arabic_to_roman(number) == numeral
    assert _python_impl.roman_to_arabic(numeral) == number
    assert rust_impl.roman_to_arabic(numeral) == number


@pytest.mark.parametrize("number", [0.0, -0.0])
@pytest.mark.parametrize("positional", [False, True])
@pytest.mark.parametrize("capital", [False, True])
def test_float_zero_uses_empty_integer_numeral(number, positional, capital):
    for backend in (_python_impl, rust_impl):
        assert backend.arabic_to_roman(number) == ""
        assert backend.arabic_to_greek(number, positional=positional, capital=capital) == ""
        assert backend.roman_to_arabic("") == 0
        assert backend.greek_to_arabic("", positional=positional, capital=capital) == 0

    assert str(RomanConvert().convert(number)) == ""
    assert str(GreekConvert(positional=positional, capital=capital).convert(number)) == ""


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


@pytest.mark.parametrize("backend", [_python_impl, rust_impl], ids=["python", "rust"])
@pytest.mark.parametrize(
    "numeral,positional,capital",
    [
        ("α.(0:ε)", False, False),
        ("α.(_:ε)", False, False),
        ("α.(0:ε)", True, False),
        ("α.(~:ε)", True, False),
    ],
)
def test_greek_fractional_zero_markers_are_accepted(backend, numeral, positional, capital):
    assert backend.greek_to_arabic(numeral, positional, capital) == 1.05


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
    assert str(roman_number) == "I.(_:V)"
    assert roman_number.get_number() == 1.05
    assert roman_converter.convert_to_arabic("I.(_:V)") == 1.05
    assert roman_converter.convert_to_arabic("I.(0:V)") == 1.05

    greek_converter = GreekConvert(positional=True, capital=True)
    greek_number = greek_converter.convert(1.05)
    assert str(greek_number) == "Α.(~:Ε)"
    assert isinstance(GreekConvert().convert(2.0).get_number(), float)
    assert greek_converter.convert_to_arabic("Α.(~:Ε)") == 1.05

    classic_converter = GreekConvert()
    assert str(classic_converter.convert(1.05)) == "α.(_:ε)"
    assert classic_converter.convert_to_arabic("α.(_:ε)") == 1.05
    assert classic_converter.convert_to_arabic("α.(0:ε)") == 1.05


def test_public_converters_roundtrip_negative_integer():
    number = -1234
    roman_converter = RomanConvert()
    roman_numeral = str(roman_converter.convert(number))

    assert roman_numeral == "-MCCXXXIV"
    assert roman_converter.convert_to_arabic(roman_numeral) == number

    for positional in (False, True):
        for capital in (False, True):
            greek_converter = GreekConvert(positional=positional, capital=capital)
            greek_numeral = str(greek_converter.convert(number))

            assert greek_numeral.startswith("-")
            assert greek_converter.convert_to_arabic(greek_numeral) == number


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
