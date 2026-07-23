from .DataType.GreekRomanType import GreekNumber, RomanNumber
from .DataStorage.Alphabet import RomanNumberAlphabet

name = "python"


def arabic_to_roman(number: int) -> str:
    return RomanNumber(number).get_value()


def roman_to_arabic(numeral: str) -> int:
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


def arabic_to_greek(number: int, positional: bool, capital: bool) -> str:
    return str(GreekNumber(number=number, positional=positional, capital=capital))


def greek_to_arabic(numeral: str, positional: bool, capital: bool) -> int:
    if numeral == "":
        return 0
    result = GreekNumber(value=numeral, positional=positional, capital=capital).get_number()
    if result is None:
        raise ValueError("Failed to convert Greek numeral to Arabic")
    return result
