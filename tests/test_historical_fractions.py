import pytest

from GreekRomanUtils import historical_fractions
from GreekRomanUtils._backend import get_backend_name

rust_impl = pytest.importorskip("GreekRomanUtils._rust_impl")


@pytest.mark.parametrize(
    "number,expected",
    [
        (0.5, ".(S)"),
        (1.0 / 12.0, ".(\U00010191)"),
        (1.0 / 24.0, ".(\U00010192)"),
        (0.125, ".(\U00010191\U00010192)"),
        (3.75, f"III.(S{chr(0x10191) * 3})"),
        (-0.5, "-.(S)"),
    ],
)
def test_roman_historical_fractions_round_trip(number, expected):
    numeral = rust_impl.historical_arabic_to_roman(number)

    assert numeral == expected
    assert rust_impl.historical_roman_to_arabic(numeral) == number


def test_greek_historical_fractions_round_trip():
    numeral = rust_impl.historical_arabic_to_greek(3.14, positional=False, capital=False)

    assert numeral == "γ.(α/η+α/ξζ+α/ι_γ_υ)"
    assert rust_impl.historical_greek_to_arabic(
        numeral,
        positional=False,
        capital=False,
    ) == 3.14

    numeral = rust_impl.historical_arabic_to_greek(1.5, positional=True, capital=True)
    assert numeral == "Α.(Α/Β)"
    assert rust_impl.historical_greek_to_arabic(
        numeral,
        positional=True,
        capital=True,
    ) == 1.5


def test_historical_fraction_math_renderers():
    assert rust_impl.historical_arabic_to_roman_latex(3.5) == r"\text{III}+\frac{1}{2}"
    assert "<mfrac><mn>1</mn><mn>2</mn></mfrac>" in rust_impl.historical_arabic_to_roman_mathml(
        0.5
    )
    assert rust_impl.historical_arabic_to_greek_latex(1.5, positional=False, capital=False) == (
        r"\text{α}+\frac{\text{α}}{\text{β}}"
    )
    assert "<mfrac><mtext>Α</mtext><mtext>Β</mtext></mfrac>" in (
        rust_impl.historical_arabic_to_greek_mathml(1.5, positional=True, capital=True)
    )


def test_unrepresentable_roman_fraction_is_mapped_to_value_error():
    with pytest.raises(ValueError, match="not representable"):
        rust_impl.historical_arabic_to_roman(3.14)


def test_public_historical_fraction_api_uses_the_selected_rust_backend():
    if get_backend_name() != "rust":
        with pytest.raises(RuntimeError, match="require the Rust backend"):
            historical_fractions.arabic_to_roman(0.5)
        return

    assert historical_fractions.arabic_to_roman(0.5) == ".(S)"
    assert historical_fractions.roman_to_arabic("III.(S)") == 3.5
    assert historical_fractions.arabic_to_greek(1.5) == "α.(α/β)"
