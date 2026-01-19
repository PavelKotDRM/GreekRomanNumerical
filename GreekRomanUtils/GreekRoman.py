from .DataStorage.Alphabet import GreekAlphabet, RomanNumberAlphabet
from .DataType.GreekRomanType import GreekNumber, RomanNumber

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
        greek_num = GreekNumber(number=number, positional=self._positional, 
                                capital=self._capital, debug=self._debug)
        return greek_num

    def convert_to_arabic(self, numeral: str) -> int:
        """Converting a Greek or Roman number to an Arabic one

        Args:
            numeral (str): The number to convert

        Returns:
            int: The converted number
        """
        result = GreekNumber(value=numeral, positional=self._positional, 
                           capital=self._capital, debug=self._debug).get_number()
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

    def unicode_to_name(self, greek_numeral: str) -> str:
        """Convert Unicode Greek numeral to name

        Args:
            greek_numeral (str): Greek numeral in Unicode

        Raises:
            ValueError: If invalid symbol is encountered

        Returns:
            str: Name of the Greek numeral
        """
        result = ""
        greek_alphabet = (
            GreekAlphabet.GREEK_ALPHABET_DICT_CAPITAL
            if self._capital
            else GreekAlphabet.GREEK_ALPHABET_DICT
        )
        for char in greek_numeral:
            if char in greek_alphabet:
                result += greek_alphabet[char] + " "
            else:
                raise ValueError(f"Invalid symbol: {char}")
        return result.strip()

    def name_to_unicode(self, name: str) -> str:
        """Convert name of Greek numeral to its Unicode representation

        Args:
            name (str): Name of Greek numeral

        Raises:
            ValueError: If invalid name is encountered

        Returns:
            str: Unicode representation of Greek numeral
        """
        greek_alphabet_dict = GreekAlphabet.GREEK_ALPHABET_DICT
        greek_alphabet_dict_capital = GreekAlphabet.GREEK_ALPHABET_DICT_CAPITAL
        reverse_dict = {v: k for k, v in greek_alphabet_dict.items()}
        reverse_dict_capital = {v: k for k, v in greek_alphabet_dict_capital.items()}
        result = ""
        for word in name.split():
            if word in reverse_dict:
                result += reverse_dict[word]
            elif word in reverse_dict_capital:
                result += reverse_dict_capital[word]
            else:
                raise ValueError(f"Invalid name: {word}")
        return result

class RomanConvert():
    
    def convert(self, number: int) -> RomanNumber:
        """Convert Arabic number to Roman numeral

        Args:
            number (int): Number to convert
        Returns:
            RomanNumber: Roman numeral representation
        """
        return RomanNumber(number)
    
    def convert_to_arabic(self, roman_numeral: str) -> int:
        """Convert Roman numeral to Arabic number

        Args:
            roman_numeral (str): Roman numeral to convert

        Returns:
            int: Arabic number representation
        """
        return self._convert_roman_to_arabic(roman_numeral)
    
    def _convert_arabic_to_roman(self, number: int) -> str:
        if not (isinstance(number, int)):
            raise TypeError("Число должно быть целым числом и иметь тип int")
        display_numerals = []
        input_num = number
        for numeral, value in RomanNumberAlphabet.ROMAN_NUMERAL_LIST:
            if input_num // value > 0:
                count = input_num // value
                input_num -= count * value
                display_numerals.append(numeral * count)
            else:
                continue
        return ''.join(display_numerals)

    def _convert_roman_to_arabic(self, roman: str) -> int:
        number = 0
        i = 0
        while i < len(roman):
            if i+1 < len(roman) and roman[i:i+2] in RomanNumberAlphabet.ROMAN_NUMERAL_DICT:
                number += RomanNumberAlphabet.ROMAN_NUMERAL_DICT[roman[i:i+2]]
                i += 2
            elif roman[i] in RomanNumberAlphabet.ROMAN_NUMERAL_DICT:
                number += RomanNumberAlphabet.ROMAN_NUMERAL_DICT[roman[i]]
                i += 1
            else:
                raise ValueError(f"Invalid name: {roman}")
        return number