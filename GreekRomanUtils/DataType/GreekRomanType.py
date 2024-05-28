from ..DataStorage.Alphabet import GreekAlphabet, RomanNumberAlphabet

class BaseNumberVirtual():
    _number: int
    _value: list
    _positional: bool
    _capital: bool
    _supported_type = (int,)

    def get_number(self) -> int:
        return self._number
    
    def set_number(self, number: int) -> None:
        self._number = number

    def __init__(self, number: int = None, value: str = None, positional: bool = False, capital: bool = False) -> None:
        raise NotImplementedError("Это абстрактный класс")
        self._number = number
        self._value = number

    def _create_instance(self, number: int) -> object:
        return self.__class__(number)
    
    def _update_value(self, number: int) -> None:
        self._number = number

    def __add__(self, other):
        if isinstance(other, BaseNumberVirtual):
            return self._create_instance(self._number + other._number)
        elif isinstance(other, self._supported_type):
            return self._create_instance(self._number + other)
        else:
            raise TypeError("Неподдерживаемый тип операнда")
    
    def __sub__(self, other):
        if isinstance(other, BaseNumberVirtual):
            return self._create_instance(self._number - other._number)
        elif isinstance(other, self._supported_type):
            return self._create_instance(self._number - other)
        else:
            raise TypeError("Неподдерживаемый тип операнда")
        
    def __mul__(self, other):
        if isinstance(other, BaseNumberVirtual):
            return self._create_instance(self._number * other._number)
        elif isinstance(other, self._supported_type):
            return self._create_instance(self._number * other)
        else:
            raise TypeError("Неподдерживаемый тип операнда")
        
    def __truediv__(self, other):
        if isinstance(other, BaseNumberVirtual):
            return self._create_instance(self._number / other._number)
        elif isinstance(other, self._supported_type):
            return self._create_instance(self._number / other)
        else:
            raise TypeError("Неподдерживаемый тип операнда")
        
    def __floordiv__(self, other):
        if isinstance(other, BaseNumberVirtual):
            return self._create_instance(self._number // other._number)
        elif isinstance(other, self._supported_type):
            return self._create_instance(self._number // other)
        else:
            raise TypeError("Неподдерживаемый тип операнда")
    
    def __mod__(self, other):
        if isinstance(other, BaseNumberVirtual):
            return self._create_instance(self._number % other._number)
        elif isinstance(other, self._supported_type):
            return self._create_instance(self._number % other)
        else:
            raise TypeError("Неподдерживаемый тип операнда")
        
    def __pow__(self, other):
        if isinstance(other, BaseNumberVirtual):
            return self._create_instance(self._number ** other._number)
        elif isinstance(other, self._supported_type):
            return self._create_instance(self._number ** other)
        else:
            raise TypeError("Неподдерживаемый тип операнда")
    
    def __eq__(self, other):
        if isinstance(other, BaseNumberVirtual):
            return self._number == other._number
        elif isinstance(other, self._supported_type):
            return self._number == other
        else:
            raise TypeError("Неподдерживаемый тип операнда")
    
    def __ne__(self, other):
        if isinstance(other, BaseNumberVirtual):
            return self._number != other._number
        elif isinstance(other, self._supported_type):
            return self._number != other
        else:
            raise TypeError("Неподдерживаемый тип операнда")
        
    def __lt__(self, other):
        if isinstance(other, BaseNumberVirtual):
            return self._number < other._number
        elif isinstance(other, self._supported_type):
            return self._number < other
        else:
            raise TypeError("Неподдерживаемый тип операнда")
        
    def __le__(self, other):
        if isinstance(other, BaseNumberVirtual):
            return self._number <= other._number
        elif isinstance(other, self._supported_type):
            return self._number <= other
        else:
            raise TypeError("Неподдерживаемый тип операнда")
    
    def __gt__(self, other):
        if isinstance(other, BaseNumberVirtual):
            return self._number > other._number
        elif isinstance(other, self._supported_type):
            return self._number > other
        else:
            raise TypeError("Неподдерживаемый тип операнда")
        
    def __ge__(self, other):
        if isinstance(other, BaseNumberVirtual):
            return self._number >= other._number
        elif isinstance(other, self._supported_type):
            return self._number >= other
        else:
            raise TypeError("Неподдерживаемый тип операнда")
    
    def __iadd__(self, other):
        if isinstance(other, BaseNumberVirtual):
            self._number += other._number
            self._update_value(self._number)
        elif isinstance(other, self._supported_type):
            self._number += other
            self._update_value(self._number)
        else:
            raise TypeError("Неподдерживаемый тип операнда")
        return self
    
    def __isub__(self, other):
        if isinstance(other, BaseNumberVirtual):
            self._number -= other._number
            self._update_value(self._number)
        elif isinstance(other, self._supported_type):
            self._number -= other
            self._update_value(self._number)
        else:
            raise TypeError("Неподдерживаемый тип операнда")
        return self
    
    def __imul__(self, other):
        if isinstance(other, BaseNumberVirtual):
            self._number *= other._number
            self._update_value(self._number)
        elif isinstance(other, self._supported_type):
            self._number *= other
            self._update_value(self._number)
        else:
            raise TypeError("Неподдерживаемый тип операнда")
        return self
    
    def __itruediv__(self, other):
        if isinstance(other, BaseNumberVirtual):
            self._number /= other._number
            self._update_value(self._number)
        elif isinstance(other, self._supported_type):
            self._number /= other
            self._update_value(self._number)
        else:
            raise TypeError("Неподдерживаемый тип операнда")
        return self
    
    def __ifloordiv__(self, other):
        if isinstance(other, BaseNumberVirtual):
            self._number //= other._number
            self._update_value(self._number)
        elif isinstance(other, self._supported_type):
            self._number //= other
            self._update_value(self._number)
        else:
            raise TypeError("Неподдерживаемый тип операнда")
        return self
    
    def __imod__(self, other):
        if isinstance(other, BaseNumberVirtual):
            self._number %= other._number
            self._update_value(self._number)
        elif isinstance(other, self._supported_type):
            self._number %= other
            self._update_value(self._number)
        else:
            raise TypeError("Неподдерживаемый тип операнда")
        return self
    
    def __ipow__(self, other):
        if isinstance(other, BaseNumberVirtual):
            self._number **= other._number
            self._update_value(self._number)
        elif isinstance(other, self._supported_type):
            self._number **= other
            self._update_value(self._number)
        else:
            raise TypeError("Неподдерживаемый тип операнда")
        return self
    
    def __neg__(self):
        return -self._number
    
    def __pos__(self):
        return +self._number

class GreekNumber(BaseNumberVirtual):

    def set_number(self, number: int) -> None:
        self._number = number
        if not self._positional:
            self._convert_arabic_to_greek(number)
        else:
            self._convert_arabic_to_position_greek(number)
    
    def set_positional(self, positional: bool) -> None:
        self._positional = positional
        if positional:
            self._convert_arabic_to_position_greek(self._number)
        else:
            self._convert_arabic_to_greek(self._number)

    def set_capital(self, capital: bool) -> None:
        self._capital = capital
        if not self._positional:
            self._convert_arabic_to_greek(self._number)
        else:
            self._convert_arabic_to_position_greek(self._number)
    
    def get_positional(self) -> bool:
        return self._positional
    
    def get_capital(self) -> bool:
        return self._capital

    def __init__(self, number: int = None, value: str = None, positional: bool = False, capital: bool = False) -> None:
        self._capital = capital
        if number == None:
            raise ValueError("Необходимо указать число")
        if not value and not positional:
            self._convert_arabic_to_greek(number)
        elif not value and positional:
            self._convert_arabic_to_position_greek(number)
        self._number = number
        self._positional = positional

    def _create_instance(self, number: int) -> object:
        return self.__class__(number, positional=self._positional, capital=self._capital)

    def __iter__(self):
        for item in self._value:
            yield item

    def __str__(self) -> str:
        return f"{''.join(self._value)}"

    def __repr__(self) -> str:
        return f"{''.join(self._value)}"

    def __len__(self) -> int:
        return len(self._value)

    def get_str(self) -> str:
        """Преобразовавние Unicode греческого числа в название

        Raises:
            ValueError: Если встречен неверный символ

        Returns:
            str: Название греческого числа
        """
        temp_str = ""
        for item in self._value:
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
        greek_numerals_list = GreekAlphabet.GREEK_NUMERAL_LIST_CAPITAL if self._capital else GreekAlphabet.GREEK_NUMERAL_LIST
        display_numerals = []
        hass_pow = False
        power_value = 0
        input_num = number
        while input_num > 0:
            for numeral, _value in reversed(greek_numerals_list):
                power_value = 0
                if len(str(input_num)) > 3:
                    power_value = ((len(str(input_num)) - 1)//3)
                    _value *= 1000**power_value
                    hass_pow = True
                if input_num // _value > 0:
                    # print(f"Processing simpol:{numeral}, целое:{_number // _value}, остаток:{_number % _value}, число:{_number}, значение:{_value}, степень:{(len(str(_number)) - 1)//3}")
                    input_num = input_num % _value
                    display_numerals.append(numeral)
                    if power_value:
                        for _ in range(power_value):
                            display_numerals.append("_")
                    if hass_pow:
                        hass_pow = False
                        break
                else:
                    continue
        self._value = display_numerals

    def _convert_arabic_to_position_greek(self, number: int) -> str:
        if not (isinstance(number, int)):
            raise TypeError("Число должно быть целым числом и иметь тип int")
        greek_numerals_dict = GreekAlphabet.GREEK_NUMERAL_DICT_CAPITAL if self._capital else GreekAlphabet.GREEK_NUMERAL_DICT
        reverse_dict = {v: k for k, v in greek_numerals_dict.items()}
        num_greek_str = ""
        input_num = number
        derative_remains_list = []
        # print(f"num = {numder}")
        while input_num > 0:
            # print(f"numder: {numder}, numder % 1000: {numder % 1000}, numder // 1000: {numder // 1000}")
            derative_remains_list.append(input_num % 1000)
            input_num = input_num // 1000
        for item in reversed(derative_remains_list):
            # print(f"num_greek_str = {num_greek_str}, i = {item}")
            if item == 0:
                num_greek_str += "_"
                num_greek_str += "~"
                continue
            for key, _value in reversed(reverse_dict.items()):
                if item // key > 0:
                    num_greek_str += _value
                    item = item % key
                    # print(f"num_greek_str = {num_greek_str}, i = {item} in for, key = {key}, _value = {_value}")
            num_greek_str += "~"
        self._value = num_greek_str[:-1]


class RomanNumber(BaseNumberVirtual):

    def get_value(self) -> str:
        return ''.join(self._value)

    def __init__(self, number: int) -> None:
        if not number:
            raise ValueError("Необходимо указать число")
        self._number = number
        self._convert_arabic_to_roman(number)

    def _convert_arabic_to_roman(self, number: int) -> None:
        if not (isinstance(number, int)):
            raise TypeError("Число должно быть целым числом и иметь тип int")
        display_numerals = []
        input_num = number
        for numeral, _value in RomanNumberAlphabet.ROMAN_NUMERAL_LIST:
            if input_num // _value > 0:
                count = input_num // _value
                input_num -= count * _value
                display_numerals.append(numeral * count)
            else:
                continue
        self._value = display_numerals

    def __iter__(self):
        for item in self._value:
            yield item

    def __getitem__(self, item):
        return self._value[item]

    def __str__(self) -> str:
        return f"{''.join(self._value)}"

    def __repr__(self) -> str:
        return f"{''.join(self._value)}"

    def __len__(self) -> int:
        return len(self._value)