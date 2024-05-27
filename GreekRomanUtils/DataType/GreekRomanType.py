from ..DataStorage.Alphabet import GreekAlphabet, RomanNumberAlphabet

class GreekNumber:
    value: str
    number: int

    def __init__(self, value: str, number: int, positional: bool) -> None:
        self.value = value
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

class RomanNumber:
    value: str
    number: int

    def __init__(self, value: str, number: int) -> None:
        self.value = value
        self.number = number

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