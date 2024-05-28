from .DataStorage.Alphabet import GreekAlphabet, RomanNumberAlphabet
from .DataType.GreekRomanType import GreekNumber, RomanNumber

class GreekConvert():

    def change_capital(self, capital:bool):
        """Изменение регистра

        Args:
            capital (bool): Верхний или нижний регист
        """
        self.capital = capital

    def create_greek_number(self, number: str, positional: bool=False) -> GreekNumber:
        """Создание греческого числа

        Args:
            value (str): Значение числа
            positional (bool, optional): Позиционное или нет. Defaults to False.

        Returns:
            GreekNumber: Греческое число
        """
        return GreekNumber(number=number, positional=positional, capital=self.capital)

    def convert(self, number: int) -> str:
        """Преобразование арабского числа в греческое

        Args:
            number (int): Число для преобразования

        Returns:
            str: Преобразованное число
        """
        return self._convert_arabic_to_greek(number)
        
    def convert_position(self, number: int) -> str:
        """Преобразование арабского числа в позиционное греческое

        Args:
            number (int): Число для преобразования

        Returns:
            str: Преобразованное число
        """
        return self._convert_arabic_to_position_greek(number)

    def convert_to_arabic(self, numeral: str) -> int:
        """Преобразование греческого или римского числа в арабское

        Args:
            numeral (str): Число для преобразования

        Returns:
            int: Преобразованное число
        """
        return self._convert_greek_to_arabic(numeral)
    
    def covert_to_position_arabic(self, numeral: str) -> int:
        """Преобразование позиционного греческого числа в арабское

        Args:
            numeral (str): Число для преобразования

        Returns:
            int: Преобразованное число
        """
        return self._convert_position_greek_to_arabic(numeral)

    def __init__(self, capital:bool=False):
        """Инициализация класса

        Args:
            capital (bool, optional): Верхний или нижний регист. Defaults to False.
        """
        self.capital = capital
    
    def _convert_arabic_to_greek(self, number: int) -> str:
        if not (isinstance(number, int)):
            raise TypeError("Число должно быть целым числом и иметь тип int")
        greek_numerals_list = GreekAlphabet.GREEK_NUMERAL_LIST_CAPITAL if self.capital else GreekAlphabet.GREEK_NUMERAL_LIST
        display_numerals = []
        hass_pow = False
        power_value = 0
        input_num = number
        while input_num > 0:
            for numeral, value in reversed(greek_numerals_list):
                power_value = 0
                if len(str(input_num)) > 3:
                    power_value = ((len(str(input_num)) - 1)//3)
                    value *= 1000**power_value
                    hass_pow = True
                if input_num // value > 0:
                    # print(f"Processing simpol:{numeral}, целое:{number // value}, остаток:{number % value}, число:{number}, значение:{value}, степень:{(len(str(number)) - 1)//3}")
                    input_num = input_num % value
                    display_numerals.append(numeral)
                    if power_value:
                        for _ in range(power_value):
                            display_numerals.append("_")
                    if hass_pow:
                        hass_pow = False
                        break
                else:
                    continue
        return ''.join(display_numerals)#''.join(display_numerals)
    
    def _convert_arabic_to_position_greek(self, number: int) -> str:
        if not (isinstance(number, int)):
            raise TypeError("Число должно быть целым числом и иметь тип int")
        greek_numerals_dict = GreekAlphabet.GREEK_NUMERAL_DICT_CAPITAL if self.capital else GreekAlphabet.GREEK_NUMERAL_DICT
        reverse_dict = {v: k for k, v in greek_numerals_dict.items()}
        num_greek_str = ""
        input_num = number
        derative_remains_list = []
        #print(f"num = {numder}")
        while input_num > 0:
            #print(f"numder: {numder}, numder % 1000: {numder % 1000}, numder // 1000: {numder // 1000}")
            derative_remains_list.append(input_num % 1000)
            input_num = input_num // 1000
        for item in reversed(derative_remains_list):
            #print(f"num_greek_str = {num_greek_str}, i = {item}")
            if item == 0:
                num_greek_str += "_"
                num_greek_str += "~"
                continue
            for key, value in reversed(reverse_dict.items()):
                if item // key > 0:
                    num_greek_str += value
                    item = item % key
                    #print(f"num_greek_str = {num_greek_str}, i = {item} in for, key = {key}, value = {value}")
            num_greek_str += "~"
        return num_greek_str[:-1]#num_greek_str[:-1]
        
    def _convert_greek_to_arabic(self, greek_numeral: str) -> int:
        number = 0
        if not (isinstance(greek_numeral, str)):
            raise TypeError("Число должно быть строкой и иметь тип str")
        power_num = 0
        last_number = 0
        for char in greek_numeral:
            if char == "_":
                power_num += 1
                continue
            # print(f"Processing simpol:{char}, число:{number}, значение:{GREEK_NUMERAL_DICT[char]}, степень:{power_num}")
            if char in GreekAlphabet.GREEK_NUMERAL_DICT:
                last_number *= 1000 ** power_num
                number += last_number
                last_number = GreekAlphabet.GREEK_NUMERAL_DICT[char]
                power_num = 0
            elif char in GreekAlphabet.GREEK_NUMERAL_DICT_CAPITAL:
                last_number *= 1000 ** power_num
                number += last_number
                last_number = GreekAlphabet.GREEK_NUMERAL_DICT_CAPITAL[char]
                power_num = 0
            else:
                raise ValueError("Неверный символ")
        number += last_number
        return number
    
    def _convert_position_greek_to_arabic(self, greek_numeral: str) -> int:
        if not (isinstance(greek_numeral, str)):
            raise TypeError("Число должно быть строкой и иметь тип str")
        out_num = 0
        for index, item in enumerate(reversed(greek_numeral.split("~"))):
            #print(f"index: {index}, item: {item}, 1000**{index}")
            if item == "_":
                continue
            for item_sub in item:
                #print(f"item_sub: {item_sub}")
                if item_sub in GreekAlphabet.GREEK_NUMERAL_DICT:
                    out_num += GreekAlphabet.GREEK_NUMERAL_DICT[item_sub] * 1000**index
                elif item_sub in GreekAlphabet.GREEK_NUMERAL_DICT_CAPITAL:
                    out_num += GreekAlphabet.GREEK_NUMERAL_DICT_CAPITAL[item_sub] * 1000**index
                else:
                    raise ValueError("Неверный символ")
        return out_num

    def unicode_to_name(self, greek_numeral: str) -> str:
        """Преобразовавние Unicode греческого числа в название

        Args:
            greek_numeral (str): Греческое число в Unicode

        Raises:
            ValueError: Если встречен неверный символ

        Returns:
            str: Название греческого числа
        """
        temp_str = ""
        for item in greek_numeral:
            if item in GreekAlphabet.GREEK_ALPHABET_DICT:
                temp_str += GreekAlphabet.GREEK_ALPHABET_DICT[item] + " "
            elif item in GreekAlphabet.GREEK_ALPHABET_DICT_CAPITAL:
                temp_str += GreekAlphabet.GREEK_ALPHABET_DICT_CAPITAL[item] + " "
            else:
                raise ValueError("Неверный символ")
        return temp_str[:-1]

    def name_to_unicode(self, name: str) -> str:
        """Преобразование названия греческого числа в Unicode

        Args:
            name (str): Название греческого числа

        Raises:
            ValueError: Если встречен неверное название

        Returns:
            str: Греческое число в Unicode
        """
        reverse_dict = {v: k for k, v in GreekAlphabet.GREEK_ALPHABET_DICT.items()}
        reverse_dic_capital = {v: k for k, v in GreekAlphabet.GREEK_ALPHABET_DICT_CAPITAL.items()}
        final_str = ""
        for item in name.split():
            if item in reverse_dict:
                final_str += reverse_dict[item]
            elif item in reverse_dic_capital:
                final_str += reverse_dic_capital[item]
            else:
                raise ValueError("Неверное название")
        return final_str

class RomanConvert():
    
    def convert(self, number: int) -> str:
        """Преобразование арабского числа в римское

        Args:
            number (int): Число для преобразования

        Returns:
            RomanNumber: Римское число
        """
        return self._convert_arabic_to_roman(number)
    
    def create_roman_number(self, number: int) -> RomanNumber:
        """Создание римского числа

        Args:
            number (int): Число

        Returns:
            RomanNumber: Римское число
        """
        return RomanNumber(number=number)
    
    def convert_to_arabic(self, roman: str) -> int:
        """Преобразование римского числа в арабское

        Args:
            roman (str): Римское число

        Returns:
            int: Арабское число
        """
        return self._convert_roman_to_arabic(roman)
    
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
        return ''.join(display_numerals)#''.join(display_numerals)

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
                raise ValueError("Неверный символ")
        return number