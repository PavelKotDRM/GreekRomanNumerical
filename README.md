# English

## Module converting Arabic numerals to Greek and Roman numbers

### Description

The library converts Arabic numbers, such as `1234`, to Roman equivalents, such as `MCCXXXIV`, or Greek — `Α_ΣΛΔ`.

This module can also output Greek numbers in different formats. For example, the number `20005003001` can be represented as `Κ___Ε__Γ_Α` or `Κ~Ε~Γ~Α`. In addition, it is possible to output the text name of the digits, for example, `Kappa macron Epsilon macron Gamma macron Alpha`, or output them in lowercase.  

### The structure of the project

There are two main classes: `GreekConvert` and `RomanConvert`. They implement the logic of converting to the corresponding numbers. There are also classes `GreekAlphabet` and `RomanNumberAlphabet`, which are used to store lists and dictionaries.  
There are proprietary data types `GreekNumber` and `RomanNumber` for working with Greek and Roman numbers, which will allow you to perform basic mathematical operations with them.

### Main functions

**For "GreekConvert":**

- `change_capital`: A flag that controls the conversion of characters to upper or lower case.
- `create_greek_number`: creates the `GreekNumber` class
- `convert` — the function of converting an Arabic number to a Greek one, for example, the number `20005003001` is converted to `Κ___Ε__Γ_Α`.
- `convert_position` is a function for converting an Arabic number to a Greek number according to a given pattern, for example, the number `20005003001` is converted to `Κ~Ε~Γ~Α`.
- `convert_to_arabic` is a function for converting a Greek number to an Arabic one.
- `covert_to_position_arabic` — This function is used in combination with `convert_position` and converts a Greek number to an Arabic one.
- `unicode_to_name` — the function converts a Unicode character into its name.
- `name_to_unicode` is the reverse operation for unicode_to_name.

**The "GreekNumber" class:**

- `set_number`: set a new value
- `set_positional`: set the number output flag
- `set_capital`: set the upper case flag
- `get_number`: get the current number
- `get_positional`: get the flag value
- `get_capital`: get the flag value
- And basic mathematical operations

**For "RomanConvert":**

- `create_roman_number`: creates the `RomanNumber` class
- `convert` — the method converts an Arabic number to a Roman number.
- `convert_to_arabic` is the reverse method for `convert`.

**For "RomanNumber":**

- `set_number`: set a new value
- `get_number`: get the current number
- And basic mathematical operations

----------------------

## Ru

## Модуль преобразование арабских цифр в греческие и римские числа

## Описание

Библиотека преобразует арабские числа, такие как `1234`, в римские эквиваленты, например, `MCCXXXIV`, или греческие — `Α_ΣΛΔ`.

Также этот модуль может выводить греческие цифры в разных форматах. Например, число `20005003001` можно представить как `Κ___Ε__Γ_Α` или `Κ~Ε~Γ~Α`. Кроме того, есть возможность выводить текстовое название цифр, например, `Kappa macron Epsilon macron Gamma macron Alpha`, или выводить их в нижнем регистре.  

## Структура пректа

Есть два основных класса: `GreekConvert` и `RomanConvert`. Они реализуют логику преобразования в соответствующие числа. Также есть классы `GreekAlphabet` и `RomanNumberAlphabet`, которые используются для хранения списков и словарей.  
Есть собственные типы данных `GreekNumber` и `RomanNumber` для работы с греческими и римскими числами, что позволит выполнять с ними базовые математические операции.

## Основные функции

**Для «GreekConvert»:**

- `change_capital`: флаг, управляющий преобразованием символов в верхний или нижний регистр.
- `create_greek_number`: создает класс `GreekNumber`
- `convert` — функция преобразования арабского числа в греческое, например, число `20005003001` преобразуется в `Κ___Ε__Γ_Α`.
- `convert_position` — функция преобразования арабского числа в греческое в соответствии с заданным шаблоном, например, число `20005003001` преобразуется в `Κ~Ε~Γ~Α`.
- `convert_to_arabic` — функция преобразования греческого числа в арабское.
- `covert_to_position_arabic` — эта функция используется в сочетании с `convert_position` и преобразует греческое число в арабское.
- `unicode_to_name` — функция преобразует символ Unicode в его название.
- `name_to_unicode` — обратная операция для `unicode_to_name`.

**Класс «GreekNumber»:**

- `set_number`: установить новое значение
- `set_positional`: установить флаг вывода числа
- `set_capital`: установить флаг верхниго регистра
- `get_number`: получить нынешнее число
- `get_positional`: получить значение флага
- `get_capital`: получить значение флага
- И базывые математические операции

**Для «RomanConvert»:**

- `create_roman_number`: создает класс `RomanNumber`
- `convert` — метод преобразует арабское число в римское.
- `convert_to_arabic` — обратный метод для `convert`.

**Для «RomanNumber»:**

- `set_number`: установить новое значение
- `get_number`: получить нынешнее число
- И базывые математические операции

**Схема пректа**  
![ScheemProject](./Diagrams/ArabicToRoman.drawio.svg)

## License

Apache License 2.0  
