from ..DataStorage.Alphabet import GreekAlphabet, RomanNumberAlphabet

class GreekNumber:
    value: str
    number: int
    positional: bool
    capital: bool

    def __init__(self, value: str=None, number: int=None, positional: bool=False, capital: bool=False) -> None:
        self.capital = capital
        if not number:
            raise ValueError("Необходимо указать число")
        if not value and not positional:
            self._convert_arabic_to_greek(number)
        elif not value and positional:
            self._convert_arabic_to_position_greek(number)
        self.number = number
        self.positional = positional

    def __iter__(self):
        for item in self.value:
            yield item

    def __str__(self) -> str:
        return f"{self.value}"
    
    def __repr__(self) -> str:
        return f"{self.value}"
    
    def get_str(self) -> str:
        """Преобразовавние Unicode греческого числа в название

        Raises:
            ValueError: Если встречен неверный символ

        Returns:
            str: Название греческого числа
        """
        temp_str = ""
        for item in self.value:
            if item in GreekAlphabet.GREEK_ALPHABET_DICT:
                temp_str += GreekAlphabet.GREEK_ALPHABET_DICT[item] + " "
            elif item in GreekAlphabet.GREEK_ALPHABET_DICT_CAPITAL:
                temp_str += GreekAlphabet.GREEK_ALPHABET_DICT_CAPITAL[item] + " "
            else:
                raise ValueError("Неверный символ")
        return temp_str[:-1]
    
    def _convert_arabic_to_greek(self, number: int) -> None:
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
        self.value = ''.join(display_numerals)

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
        self.value = num_greek_str[:-1]

class RomanNumber:
    value: str
    number: int

    def __init__(self, number: int) -> None:
        if not number:
            raise ValueError("Необходимо указать число")
        self.number = number
        self._convert_arabic_to_roman(number)

    def _convert_arabic_to_roman(self, number: int) -> None:
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
        self.value = ''.join(display_numerals)

    def __iter__(self):
        for item in self.value:
            yield item

    def __getitem__(self, item):
        return self.value[item]

    def __str__(self) -> str:
        return f"{self.value}"

    def __repr__(self) -> str:
        return f"{self.value}"
    
    def __len__(self) -> int:
        return len(self.value)