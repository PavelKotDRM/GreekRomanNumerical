from . import _native

name = "rust"


def arabic_to_roman(number: int) -> str:
    return _native.arabic_to_roman(number)


def roman_to_arabic(numeral: str) -> int:
    return _native.roman_to_arabic(numeral)


def arabic_to_greek(number: int, positional: bool, capital: bool) -> str:
    return _native.arabic_to_greek(number, positional, capital)


def greek_to_arabic(numeral: str, positional: bool, capital: bool) -> int:
    return _native.greek_to_arabic(numeral, positional, capital)
