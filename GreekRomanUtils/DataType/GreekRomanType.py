from ..DataStorage.Alphabet import GreekAlphabet, RomanNumberAlphabet
from typing import Optional, Union

class BaseNumberVirtual():
    _number: Union[int, None]
    _value: Union[str, list, None]
    _positional: bool
    _capital: bool
    _debug: bool
    _supported_type = (int,)

    def get_number(self) -> Union[int, None]:
        return self._number
    
    def set_number(self, number: Union[int, None]) -> None:
        self._number = number

    def __init__(self, number: Optional[int] = None, value: Optional[str] = None, positional: bool = False, capital: bool = False, debug: bool = False) -> None:
        raise NotImplementedError("This is an abstract class")
        self._number = number
        self._value = number
        self._positional = positional
        self._capital = capital
        self._debug = debug

    def _create_instance(self, number: Union[int, float]) -> object:
        if isinstance(number, int):
            return self.__class__(number)
        if isinstance(number, float):
            return self.__class__(int(number))
        else:
            raise TypeError("Unsupported type for instance creation")
    
    def _update_value(self, number: Union[int, float]) -> None:
        if isinstance(number, int):
            self._number = number
        elif isinstance(number, float):
            self._number = int(number)
        else:
            raise TypeError("Unsupported type for value update")

    def __add__(self, other):
        if isinstance(other, BaseNumberVirtual):
            return self._create_instance(self._number + other._number)
        elif isinstance(other, self._supported_type):
            return self._create_instance(self._number + other)
        else:
            raise TypeError("Unsupported operand type")
    
    def __sub__(self, other):
        if isinstance(other, BaseNumberVirtual):
            return self._create_instance(self._number - other._number)
        elif isinstance(other, self._supported_type):
            return self._create_instance(self._number - other)
        else:
            raise TypeError("Unsupported operand type")
        
    def __mul__(self, other):
        if isinstance(other, BaseNumberVirtual):
            return self._create_instance(self._number * other._number)
        elif isinstance(other, self._supported_type):
            return self._create_instance(self._number * other)
        else:
            raise TypeError("Unsupported operand type")
        
    def __truediv__(self, other):
        if isinstance(other, BaseNumberVirtual):
            return self._create_instance(self._number / other._number)
        elif isinstance(other, self._supported_type):
            return self._create_instance(self._number / other)
        else:
            raise TypeError("Unsupported operand type")
        
    def __floordiv__(self, other):
        if isinstance(other, BaseNumberVirtual):
            return self._create_instance(self._number // other._number)
        elif isinstance(other, self._supported_type):
            return self._create_instance(self._number // other)
        else:
            raise TypeError("Unsupported operand type")
    
    def __mod__(self, other):
        if isinstance(other, BaseNumberVirtual):
            return self._create_instance(self._number % other._number)
        elif isinstance(other, self._supported_type):
            return self._create_instance(self._number % other)
        else:
            raise TypeError("Unsupported operand type")
        
    def __pow__(self, other):
        if isinstance(other, BaseNumberVirtual):
            return self._create_instance(self._number ** other._number)
        elif isinstance(other, self._supported_type):
            return self._create_instance(self._number ** other)
        else:
            raise TypeError("Unsupported operand type")
    
    def __eq__(self, other):
        if isinstance(other, BaseNumberVirtual):
            return self._number == other._number
        elif isinstance(other, self._supported_type):
            return self._number == other
        else:
            raise TypeError("Unsupported operand type")
    
    def __ne__(self, other):
        if isinstance(other, BaseNumberVirtual):
            return self._number != other._number
        elif isinstance(other, self._supported_type):
            return self._number != other
        else:
            raise TypeError("Unsupported operand type")
        
    def __lt__(self, other):
        if isinstance(other, BaseNumberVirtual):
            return self._number < other._number
        elif isinstance(other, self._supported_type):
            return self._number < other
        else:
            raise TypeError("Unsupported operand type")
        
    def __le__(self, other):
        if isinstance(other, BaseNumberVirtual):
            return self._number <= other._number
        elif isinstance(other, self._supported_type):
            return self._number <= other
        else:
            raise TypeError("Unsupported operand type")
    
    def __gt__(self, other):
        if isinstance(other, BaseNumberVirtual):
            return self._number > other._number
        elif isinstance(other, self._supported_type):
            return self._number > other
        else:
            raise TypeError("Unsupported operand type")
        
    def __ge__(self, other):
        if isinstance(other, BaseNumberVirtual):
            return self._number >= other._number
        elif isinstance(other, self._supported_type):
            return self._number >= other
        else:
            raise TypeError("Unsupported operand type")
    
    def __iadd__(self, other):
        if isinstance(other, BaseNumberVirtual):
            self._number += other._number
            self._update_value(self._number)
        elif isinstance(other, self._supported_type):
            self._number += other
            self._update_value(self._number)
        else:
            raise TypeError("Unsupported operand type")
        return self
    
    def __isub__(self, other):
        if isinstance(other, BaseNumberVirtual):
            self._number -= other._number
            self._update_value(self._number)
        elif isinstance(other, self._supported_type):
            self._number -= other
            self._update_value(self._number)
        else:
            raise TypeError("Unsupported operand type")
        return self
    
    def __imul__(self, other):
        if isinstance(other, BaseNumberVirtual):
            self._number *= other._number
            self._update_value(self._number)
        elif isinstance(other, self._supported_type):
            self._number *= other
            self._update_value(self._number)
        else:
            raise TypeError("Unsupported operand type")
        return self
    
    def __itruediv__(self, other):
        if isinstance(other, BaseNumberVirtual):
            self._number /= other._number
            self._update_value(self._number)
        elif isinstance(other, self._supported_type):
            self._number /= other
            self._update_value(self._number)
        else:
            raise TypeError("Unsupported operand type")
        return self
    
    def __ifloordiv__(self, other):
        if isinstance(other, BaseNumberVirtual):
            self._number //= other._number
            self._update_value(self._number)
        elif isinstance(other, self._supported_type):
            self._number //= other
            self._update_value(self._number)
        else:
            raise TypeError("Unsupported operand type")
        return self
    
    def __imod__(self, other):
        if isinstance(other, BaseNumberVirtual):
            self._number %= other._number
            self._update_value(self._number)
        elif isinstance(other, self._supported_type):
            self._number %= other
            self._update_value(self._number)
        else:
            raise TypeError("Unsupported operand type")
        return self
    
    def __ipow__(self, other):
        if isinstance(other, BaseNumberVirtual):
            self._number **= other._number
            self._update_value(self._number)
        elif isinstance(other, self._supported_type):
            self._number **= other
            self._update_value(self._number)
        else:
            raise TypeError("Unsupported operand type")
        return self
    
    def __neg__(self):
        if self._number is None:
            raise TypeError("Cannot negate None value")
        return self._create_instance(-self._number)
    
    def __pos__(self):
        if self._number is None:
            raise TypeError("Cannot apply unary plus to None value")
        return self._create_instance(+self._number)

class GreekNumber(BaseNumberVirtual):

    def set_number(self, number: Union[int, None]) -> None:
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

    def __init__(self, number: Optional[int] = None, value: Optional[str] = None, positional: bool = False, capital: bool = False, debug: bool = False) -> None:
        self._capital = capital
        self._debug = debug
        self._positional = positional
        self._number = number
        self._value = value
        if number is None and value is None:
            raise ValueError("You must specify a number")
        if not value and not positional:
            self._convert_arabic_to_greek(number)
        elif not value and positional:
            self._convert_arabic_to_position_greek(number)
        elif value and not positional:
            self._convert_greek_to_arabic(value)
        elif value and positional:
            self._convert_position_greek_to_arabic(value)

    def _create_instance(self, number: Union[int, float]) -> object:
        if isinstance(number, int):
            return self.__class__(number, positional=self._positional, capital=self._capital)
        elif isinstance(number, float):
            return self.__class__(int(number), positional=self._positional, capital=self._capital)
        else:
            raise TypeError("Unsupported type for instance creation")

    def __iter__(self):
        if self._value is None:
            raise TypeError("Value is None, cannot iterate")
        for item in self._value:
            yield item

    def __str__(self) -> str:
        if isinstance(self._value, str):
            return f"{self._value}"
        elif isinstance(self._value, list):
            return f"{''.join(self._value)}"
        else:
            return "None"

    def __repr__(self) -> str:
        if isinstance(self._value, str):
            return f"{self._value}"
        elif isinstance(self._value, list):
            return f"{''.join(self._value)}"
        else:
            return "None"

    def __len__(self) -> int:
        if self._value is None:
            raise TypeError("Value is None, length is undefined")
        return len(self._value)

    def get_str(self) -> str:
        """Converting a Unicode Greek number to a name

        Raises:
            ValueError: If an invalid character is encountered

        Returns:
            str: The name of the Greek number
        """
        result = ""
        greek_alphabet = (
            GreekAlphabet.GREEK_ALPHABET_DICT_CAPITAL
            if self._capital
            else GreekAlphabet.GREEK_ALPHABET_DICT
        )
        if not isinstance(self._value, str) and not isinstance(self._value, list):
            raise TypeError("Value must be a string or a list to convert to name")
        for item in self._value:
            if item in greek_alphabet:
                result += greek_alphabet[item] + " "
            else:
                raise ValueError(f"Invalid character {item}")
        return result.strip()

    def _convert_arabic_to_greek(self, number: Union[int, None]) -> None:
        if not (isinstance(number, int)):
            raise TypeError("The number must be an integer and be of type int")
        greek_numerals_list = (
            GreekAlphabet.GREEK_NUMERAL_LIST_CAPITAL 
            if self._capital 
            else GreekAlphabet.GREEK_NUMERAL_LIST
        )
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
                    if self._debug:
                        print(f"Processing simpol:{numeral}, целое:{number // _value}, остаток:{number % _value}, число:{number}, \
                              значение:{_value}, степень:{(len(str(number)) - 1)//3}")
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
        self._value = ''.join(display_numerals)

    def _convert_arabic_to_position_greek(self, number: Union[int, None]) -> Union[str, None]:
        if not (isinstance(number, int)):
            raise TypeError("The number must be an integer and be of type int")
        greek_numerals_dict = (
            GreekAlphabet.GREEK_NUMERAL_DICT_CAPITAL 
            if self._capital 
            else GreekAlphabet.GREEK_NUMERAL_DICT
        )
        reverse_dict = {v: k for k, v in greek_numerals_dict.items()}
        result = ""
        input_num = number
        derative_remains_list = []
        if self._debug:
            print(f"_convert_arabic_to_position_greek input = {number}")
        while input_num > 0:
            if self._debug:
                print(f"numder: {input_num}, numder % 1000: {input_num % 1000}, numder // 1000: {input_num // 1000}")
            derative_remains_list.append(input_num % 1000)
            input_num = input_num // 1000
        for item in reversed(derative_remains_list):
            if self._debug:
                print(f"result = {result}, i = {item}")
            if len(result) > 0:
                if result[-1] == " ":
                    result = result.strip() + "~"
            for key, _value in reversed(reverse_dict.items()):
                if item // key > 0:
                    result += _value
                    item = item % key
                    if self._debug:
                        print(f"result = {result}, i = {item} in for, key = {key}, _value = {_value}")
            result += " "
        self._value = result.strip()

    def _convert_greek_to_arabic(self, greek_numeral: str) -> Union[int, None]:
        number = 0
        if not (isinstance(greek_numeral, str)):
            raise TypeError("The number must be a string and be of type string")
        power_num = 0
        last_number = 0
        greek_numeral_dict = (
            GreekAlphabet.GREEK_NUMERAL_DICT_CAPITAL 
            if self._capital 
            else GreekAlphabet.GREEK_NUMERAL_DICT
        )
        if self._debug:
            print(f"_convert_greek_to_arabic input = {greek_numeral}")
        for char in greek_numeral:
            if char == "_":
                power_num += 1
                continue
            if self._debug:
                print(f"Processing simpol:{char}, число:{number}, значение:{greek_numeral_dict[char]}, степень:{power_num}")
            if char in greek_numeral_dict:
                last_number *= 1000 ** power_num
                number += last_number
                last_number = greek_numeral_dict[char]
                power_num = 0
            else:
                raise ValueError(f"Invalid symbol: {char}")
        if power_num > 0:
            last_number *= 1000 ** power_num
            power_num = 0
        number += last_number
        self._number = number
    
    def _convert_position_greek_to_arabic(self, greek_numeral: str) -> Union[int, None]:
        if not (isinstance(greek_numeral, str)):
            raise TypeError("The number must be a string and be of type string")
        number = 0
        greek_numeral_dict = (
            GreekAlphabet.GREEK_NUMERAL_DICT_CAPITAL 
            if self._capital 
            else GreekAlphabet.GREEK_NUMERAL_DICT
        )
        if self._debug:
            print(f"_convert_position_greek_to_arabic input = {greek_numeral}")
        for index, item in enumerate(reversed(greek_numeral.split("~"))):
            if self._debug:
                print(f"index: {index}, item: {item}, 1000**{index}")
            for item_sub in item:
                if self._debug:
                    print(f"item_sub: {item_sub}")
                if item_sub in greek_numeral_dict:
                    number += greek_numeral_dict[item_sub] * 1000**index
                else:
                    raise ValueError(f"Invalid symbol: {item_sub}")
        self._number = number


class RomanNumber(BaseNumberVirtual):

    def get_value(self) -> str:
        if isinstance(self._value, list):
            return ''.join(self._value)
        return str(self._value)

    def __init__(self, number: int) -> None:
        if not number:
            raise ValueError("You must specify a number")
        self._number = number
        self._convert_arabic_to_roman(number)

    def _convert_arabic_to_roman(self, number: int) -> None:
        if not (isinstance(number, int)):
            raise TypeError("The number must be an integer and be of type int")
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
        if self._value is None:
            raise TypeError("Value is None, cannot iterate")
        for item in self._value:
            yield item

    def __getitem__(self, item):
        if self._value is None:
            raise TypeError("Value is None, cannot index")
        return self._value[item]

    def __str__(self) -> str:
        if isinstance(self._value, str):
            return f"{self._value}"
        elif isinstance(self._value, list):
            return f"{''.join(self._value)}"
        else:
            return "None"

    def __repr__(self) -> str:
        if isinstance(self._value, str):
            return f"{self._value}"
        elif isinstance(self._value, list):
            return f"{''.join(self._value)}"
        else:
            return "None"

    def __len__(self) -> int:
        if self._value is None:
            raise TypeError("Value is None, length is undefined")
        return len(self._value)