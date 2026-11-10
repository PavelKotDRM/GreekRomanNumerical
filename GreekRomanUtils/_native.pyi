from collections.abc import Iterable as _Iterable

def arabic_to_roman(number: float) -> str: ...


def arabic_to_roman_parallel(numbers: _Iterable[int | float]) -> list[str]: ...


def roman_to_arabic(numeral: str) -> int | float: ...


def arabic_to_greek(number: float, positional: bool, capital: bool) -> str: ...


def arabic_to_greek_parallel(
    numbers: _Iterable[int | float],
    positional: bool,
    capital: bool,
) -> list[str]: ...


def greek_to_arabic(numeral: str, positional: bool, capital: bool) -> int | float: ...


def historical_arabic_to_roman(number: float) -> str: ...


def historical_roman_to_arabic(numeral: str) -> int | float: ...


def historical_arabic_to_greek(number: float, positional: bool, capital: bool) -> str: ...


def historical_greek_to_arabic(
    numeral: str,
    positional: bool,
    capital: bool,
) -> int | float: ...


def historical_arabic_to_roman_latex(number: float) -> str: ...


def historical_arabic_to_roman_mathml(number: float) -> str: ...


def historical_arabic_to_greek_latex(
    number: float,
    positional: bool,
    capital: bool,
) -> str: ...


def historical_arabic_to_greek_mathml(
    number: float,
    positional: bool,
    capital: bool,
) -> str: ...
