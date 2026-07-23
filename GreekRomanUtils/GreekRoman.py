from .DataStorage.Alphabet import GreekAlphabet, RomanNumberAlphabet
from .DataType.GreekRomanType import GreekNumber, RomanNumber
from ._backend import get_backend


_GREEK_NAME_TO_UNICODE = {v: k for k, v in GreekAlphabet.GREEK_ALPHABET_DICT.items()}
_GREEK_NAME_TO_UNICODE_CAPITAL = {v: k for k, v in GreekAlphabet.GREEK_ALPHABET_DICT_CAPITAL.items()}

class GreekConvert():

    def change_capital(self, capital:bool):
        """Changing the case

        Args:
            capital (bool): Upper or lower register
        """
        self._capital = capital

    def change_positional(self, positional:bool):
        """Changing the positional mode

        Args:
            positional (bool): Positional or not
        """
        self._positional = positional

    def convert(self, number: int) -> GreekNumber:
        """Converting an Arabic number to a Greek one

        Args:
            number (int): The number to convert

        Returns:
            GreekNumber: The Greek number
        """
        numeral = self._backend.arabic_to_greek(
            number=number,
            positional=self._positional,
            capital=self._capital,
        )
        greek_num = GreekNumber(value=numeral, positional=self._positional,
                                capital=self._capital, debug=self._debug)
        return greek_num

    def convert_to_arabic(self, numeral: str) -> int:
        """Converting a Greek or Roman number to an Arabic one

        Args:
            numeral (str): The number to convert

        Returns:
            int: The converted number
        """
        result = self._backend.greek_to_arabic(
            numeral=numeral,
            positional=self._positional,
            capital=self._capital,
        )
        if result is None:
            raise ValueError("Failed to convert Greek numeral to Arabic")
        return result

    def __init__(self, capital:bool=False, debug:bool=False, positional:bool=False):
        """Initializing a class

        Args:
            capital (bool, optional): Upper or lower case. Defaults to False.
        """
        self._debug = debug
        self._capital = capital
        self._positional = positional
        self._backend = get_backend()

    def unicode_to_name(self, greek_numeral: str) -> str:
        """Convert Unicode Greek numeral to name

        Args:
            greek_numeral (str): Greek numeral in Unicode

        Raises:
            ValueError: If invalid symbol is encountered

        Returns:
            str: Name of the Greek numeral
        """
        parts: list[str] = []
        greek_alphabet = (
            GreekAlphabet.GREEK_ALPHABET_DICT_CAPITAL
            if self._capital
            else GreekAlphabet.GREEK_ALPHABET_DICT
        )
        for char in greek_numeral:
            if char in greek_alphabet:
                parts.append(greek_alphabet[char])
            else:
                raise ValueError(f"Invalid symbol: {char}")
        return " ".join(parts)

    def name_to_unicode(self, name: str) -> str:
        """Convert name of Greek numeral to its Unicode representation

        Args:
            name (str): Name of Greek numeral

        Raises:
            ValueError: If invalid name is encountered

        Returns:
            str: Unicode representation of Greek numeral
        """
        chars: list[str] = []
        for word in name.split():
            if word in _GREEK_NAME_TO_UNICODE:
                chars.append(_GREEK_NAME_TO_UNICODE[word])
            elif word in _GREEK_NAME_TO_UNICODE_CAPITAL:
                chars.append(_GREEK_NAME_TO_UNICODE_CAPITAL[word])
            else:
                raise ValueError(f"Invalid name: {word}")
        return "".join(chars)

class RomanConvert():

    def __init__(self):
        self._backend = get_backend()

    @staticmethod
    def _chunk_roman_value(numeral: str) -> list[str]:
        chunks: list[str] = []
        index = 0
        for token, _ in RomanNumberAlphabet.ROMAN_NUMERAL_LIST:
            count = 0
            while numeral[index:index + len(token)] == token and token:
                index += len(token)
                count += 1
            if count > 0:
                chunks.append(token * count)
        return chunks
    
    def convert(self, number: int) -> RomanNumber:
        """Convert Arabic number to Roman numeral

        Args:
            number (int): Number to convert
        Returns:
            RomanNumber: Roman numeral representation
        """
        roman_number = RomanNumber(number)
        numeral = self._backend.arabic_to_roman(number=number)
        roman_number._value = self._chunk_roman_value(numeral)
        return roman_number
    
    def convert_to_arabic(self, roman_numeral: str) -> int:
        """Convert Roman numeral to Arabic number

        Args:
            roman_numeral (str): Roman numeral to convert

        Returns:
            int: Arabic number representation
        """
        return self._backend.roman_to_arabic(numeral=roman_numeral)
    
    def _convert_arabic_to_roman(self, number: int) -> str:
        return self._backend.arabic_to_roman(number=number)

    def _convert_roman_to_arabic(self, roman: str) -> int:
        return self._backend.roman_to_arabic(numeral=roman)