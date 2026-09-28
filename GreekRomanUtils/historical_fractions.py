"""Optional historical-fraction conversions backed by the Rust core."""

from ._backend import get_backend


def _rust_backend():
    if get_backend().name != "rust":
        raise RuntimeError(
            "Historical fractions require the Rust backend; install the native extension "
            "and make sure GREEKROMAN_FORCE_PYTHON is not enabled."
        )
    from . import _rust_impl

    return _rust_impl


def arabic_to_roman(number: float) -> str:
    """Convert an integer or float using Roman historical-fraction notation."""
    return _rust_backend().historical_arabic_to_roman(number)


def roman_to_arabic(numeral: str) -> int | float:
    """Parse a Roman historical-fraction numeral to an integer or float."""
    return _rust_backend().historical_roman_to_arabic(numeral)


def arabic_to_greek(
    number: float,
    positional: bool = False,
    capital: bool = False,
) -> str:
    """Convert an integer or float using Greek unit-fraction notation."""
    return _rust_backend().historical_arabic_to_greek(number, positional, capital)


def greek_to_arabic(
    numeral: str,
    positional: bool = False,
    capital: bool = False,
) -> int | float:
    """Parse a Greek historical-fraction numeral to an integer or float."""
    return _rust_backend().historical_greek_to_arabic(numeral, positional, capital)


def arabic_to_roman_latex(number: float) -> str:
    """Render a Roman historical-fraction conversion as a LaTeX math fragment."""
    return _rust_backend().historical_arabic_to_roman_latex(number)


def arabic_to_roman_mathml(number: float) -> str:
    """Render a Roman historical-fraction conversion as inline MathML."""
    return _rust_backend().historical_arabic_to_roman_mathml(number)


def arabic_to_greek_latex(
    number: float,
    positional: bool = False,
    capital: bool = False,
) -> str:
    """Render a Greek historical-fraction conversion as a LaTeX math fragment."""
    return _rust_backend().historical_arabic_to_greek_latex(number, positional, capital)


def arabic_to_greek_mathml(
    number: float,
    positional: bool = False,
    capital: bool = False,
) -> str:
    """Render a Greek historical-fraction conversion as inline MathML."""
    return _rust_backend().historical_arabic_to_greek_mathml(number, positional, capital)
