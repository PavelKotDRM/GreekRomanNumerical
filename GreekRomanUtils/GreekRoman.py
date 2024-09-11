from .DataStorage.Alphabet import GreekAlphabet, RomanNumberAlphabet
from .DataType.GreekRomanType import GreekNumber, RomanNumber

class GreekConvert():

    def change_capital(self, capital:bool):
        """Changing the case

        Args:
            capital (bool): Upper or lower register
        """
        self._capital = capital

    def create_greek_number(self, number: str, positional: bool=False) -> GreekNumber:
        """Creating a Greek number

        Args:
            value (str): The value of the number
            positional (bool, optional): Positional or not. Defaults to False.

        Returns:
            GreekNumber: The Greek number
        """
        return GreekNumber(number=number, positional=positional, 
                           capital=self._capital, debug=self._debug)

    def convert(self, number: int) -> str:
        """Converting an Arabic number to a Greek one

        Args:
            number (int): The number to convert

        Returns:
            str: The converted number
        """
        return GreekNumber(number=number, positional=False, 
                           capital=self._capital, debug=self._debug)._value
        
    def convert_position(self, number: int) -> str:
        """Converting an Arabic number to a positional Greek number

        Args:
            number (int): The number to convert

        Returns:
            str: The converted number
        """
        return GreekNumber(number=number, positional=True, 
                           capital=self._capital, debug=self._debug)._value

    def convert_to_arabic(self, numeral: str) -> int:
        """Converting a Greek or Roman number to an Arabic one

        Args:
            numeral (str): The number to convert

        Returns:
            int: The converted number
        """
        return GreekNumber(value=numeral, positional=False, 
                           capital=self._capital, debug=self._debug).get_number()
    
    def covert_to_position_arabic(self, numeral: str) -> int:
        """Converting a positional Greek number to an Arabic one

        Args:
            numeral (str): The number to convert

        Returns:
            int: The converted number
        """
        return GreekNumber(value=numeral, positional=True, 
                           capital=self._capital, debug=self._debug).get_number()

    def __init__(self, capital:bool=False, debug:bool=False):
        """Initializing a class

        Args:
            capital (bool, optional): Upper or lower case. Defaults to False.
        """
        self._debug = debug
        self._capital = capital

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
    
    def convert(self, arabic_number: int) -> str:
        """Convert Arabic number to Roman numeral

        Args:
            arabic_number (int): Number to convert

        Returns:
            str: Roman numeral representation
        """
        return self._convert_arabic_to_roman(arabic_number)
    
    def create_roman_number(self, arabic_number: int) -> RomanNumber:
        """Create a Roman numeral from an Arabic number

        Args:
            arabic_number (int): The number to convert

        Returns:
            RomanNumber: The Roman numeral representation
        """
        return RomanNumber(arabic_number)
    
    def convert_to_arabic(self, roman_numeral: str) -> int:
        """Convert Roman numeral to Arabic number

        Args:
            roman_numeral (str): Roman numeral to convert

        Returns:
            int: Arabic number representation
        """
        return self._convert_roman_to_arabic(roman_numeral)
    
    def _convert_arabic_to_roman(self, number: int) -> RomanNumber:
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