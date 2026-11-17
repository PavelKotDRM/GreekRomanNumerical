from collections.abc import Callable, Iterable

from ._numeric import format_float_numeral, parse_decimal_numeral
from ._progress import ProgressBar
from .DataStorage.Alphabet import RomanNumberAlphabet
from .DataType.GreekRomanType import GreekNumber, RomanNumber

name = "python"


def create_progress_bar(total: int, message: str | None = None) -> ProgressBar:
    return ProgressBar(total, message)


def _convert_many(
    numbers: Iterable[int | float],
    convert: Callable[[int | float], str],
    progress: bool,
    message: str | None,
) -> list[str]:
    if not progress:
        return [convert(number) for number in numbers]

    numbers = list(numbers)
    bar = ProgressBar(len(numbers), message)
    try:
        results = []
        for number in numbers:
            results.append(convert(number))
            bar.inc()
        return results
    finally:
        bar.finish()


def arabic_to_roman(number: float) -> str:
    if isinstance(number, float):
        return format_float_numeral(
            number,
            lambda whole: RomanNumber(whole).get_value(),
            zero_token="_",
        )
    return RomanNumber(number).get_value()

def arabic_to_roman_many(
    numbers: Iterable[int | float],
    progress: bool = False,
    message: str | None = None,
) -> list[str]:
    return _convert_many(numbers, arabic_to_roman, progress, message)


def _roman_to_arabic_integer(numeral: str) -> int:
    number = 0
    index = 0
    while index < len(numeral):
        token2 = numeral[index:index + 2]
        if token2 in RomanNumberAlphabet.ROMAN_NUMERAL_DICT:
            number += RomanNumberAlphabet.ROMAN_NUMERAL_DICT[token2]
            index += 2
            continue
        token1 = numeral[index]
        if token1 in RomanNumberAlphabet.ROMAN_NUMERAL_DICT:
            number += RomanNumberAlphabet.ROMAN_NUMERAL_DICT[token1]
            index += 1
            continue
        raise ValueError(f"Invalid name: {numeral}")
    return number


def roman_to_arabic(numeral: str) -> int | float:
    return parse_decimal_numeral(numeral, _roman_to_arabic_integer, zero_token="_")


def arabic_to_greek(number: float, positional: bool, capital: bool) -> str:
    if isinstance(number, float):
        return format_float_numeral(
            number,
            lambda whole: arabic_to_greek(whole, positional=positional, capital=capital),
            zero_token="~" if positional else "_",
        )
    return str(GreekNumber(number=number, positional=positional, capital=capital))

def arabic_to_greek_many(
    numbers: Iterable[int | float],
    positional: bool,
    capital: bool,
    progress: bool = False,
    message: str | None = None,
) -> list[str]:
    return _convert_many(
        numbers,
        lambda number: arabic_to_greek(number, positional=positional, capital=capital),
        progress,
        message,
    )


def _greek_to_arabic_integer(numeral: str, positional: bool, capital: bool) -> int:
    result = GreekNumber(value=numeral, positional=positional, capital=capital).get_number()
    if result is None:
        raise ValueError("Failed to convert Greek numeral to Arabic")
    if not isinstance(result, int):
        raise TypeError("Expected an integer Greek numeral")
    return result


def greek_to_arabic(numeral: str, positional: bool, capital: bool) -> int | float:
    return parse_decimal_numeral(
        numeral,
        lambda integer: _greek_to_arabic_integer(
            integer,
            positional=positional,
            capital=capital,
        ),
        zero_token="~" if positional else "_",
    )
