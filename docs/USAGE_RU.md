# Руководство по использованию GreekRomanUtils

GreekRomanUtils преобразует целые числа Python и конечные значения `float` в римскую или греческую запись и обратно. Публичный объектно-ориентированный API включает конвертеры `RomanConvert` и `GreekConvert`, а также объекты чисел `RomanNumber` и `GreekNumber`.

**Языки:** [English](./USAGE.md) | Русский

## Установка

Требуется Python 3.11 или новее:

```bash
python -m pip install GreekRomanUtils
```

Если доступен совместимый wheel, Rust toolchain не нужен. Если пакет приходится собирать из исходников, могут потребоваться Rust stable, maturin и, в Windows, MSVC C++ Build Tools.

## Импорт и первая конвертация

```python
from GreekRomanUtils.GreekRoman import (
    GreekConvert,
    GreekNumber,
    RomanConvert,
    RomanNumber,
)

roman = RomanConvert()
greek = GreekConvert()

roman_number = roman.convert(2024)
greek_number = greek.convert(1234)

print(roman_number)  # MMXXIV
print(greek_number)  # α_σλδ

print(roman.convert_to_arabic(str(roman_number)))  # 2024
print(greek.convert_to_arabic(str(greek_number)))  # 1234
```

Метод `convert()` возвращает объект числового типа, а не обычную строку. Чтобы вывести запись, используйте `str(value)` или `print(value)`. Для получения арабского значения используйте `get_number()`.

## Римские числа

### Преобразование в римскую запись

```python
from GreekRomanUtils.GreekRoman import RomanConvert

roman = RomanConvert()

print(roman.convert(4))        # IV
print(roman.convert(2024))     # MMXXIV
print(roman.convert(5000))     # ~V
print(roman.convert(-1234))    # -MCCXXXIV
```

В стандартной записи используются символы `I`, `V`, `X`, `L`, `C`, `D`, `M` и вычитаемые пары `IV`, `IX`, `XL`, `XC`, `CD`, `CM`. Для больших значений используются дополнительные токены: `~V` = 5 000, `~X` = 10 000, `~L` = 50 000, `~C` = 100 000, `~D` = 500 000, `~M` = 1 000 000.

Ноль обозначается пустой строкой:

```python
str(roman.convert(0))  # ""
```

Целые числа Python имеют произвольную точность. Практическое ограничение зависит от доступной памяти и размера итоговой строки.

### Преобразование римской записи в целое число

```python
roman.convert_to_arabic("MMXXIV")         # 2024
roman.convert_to_arabic("~C~X~XMMMCDLVI") # 123456
roman.convert_to_arabic("-IV")            # -4
roman.convert_to_arabic("")               # 0
```

Римские символы нужно передавать в верхнем регистре. Парсер распознаёт поддерживаемые токены и отклоняет неизвестные символы, но не предназначен для строгой проверки всех правил канонической римской записи.

## Греческие числа

### Классический, позиционный и прописной режимы

Конструктор `GreekConvert` принимает три параметра:

```python
GreekConvert(capital=False, debug=False, positional=False)
```

- `capital=False` задаёт строчные греческие символы, `True` — прописные.
- `positional=False` выбирает классическую запись, где `_` обозначает степени 1 000. При `True` используется позиционная запись с группами по основанию 1 000, разделёнными `~`.
- `debug=False` отключает диагностический вывод по умолчанию.

```python
from GreekRomanUtils.GreekRoman import GreekConvert

classic = GreekConvert()
positional = GreekConvert(positional=True)
uppercase = GreekConvert(positional=True, capital=True)

print(classic.convert(1234))     # α_σλδ
print(positional.convert(1234))  # α~σλδ
print(uppercase.convert(1234))   # Α~ΣΛΔ
```

При разборе используйте то же значение `positional`, что и при создании записи. Параметр `capital` также должен соответствовать регистру символов во входной строке.

```python
positional.convert_to_arabic("α~σλδ")  # 1234
uppercase.convert_to_arabic("Α~ΣΛΔ")   # 1234
```

Пустые группы в позиционной записи сохраняют разряды. Не удаляйте разделители `~`, даже если между ними нет символов.

Режим конвертера можно изменить для последующих преобразований. Уже созданные объекты `GreekNumber` при этом не меняются:

```python
greek = GreekConvert()
greek.change_positional(True)
greek.change_capital(True)

print(greek.convert(1234))  # Α~ΣΛΔ
```

### Преобразование греческой записи в целое число

```python
classic = GreekConvert()
classic.convert_to_arabic("α_σλδ")  # 1234

positional = GreekConvert(positional=True)
positional.convert_to_arabic("α~σλδ")  # 1234
```

Ноль обозначается пустой строкой, отрицательные значения начинаются с `-`. Греческий числовой алфавит состоит из 27 символов для единиц, десятков и сотен. Специальные символы: `ϝ` (6), `ϙ` (90), `ϡ` (900); прописные варианты — `Ϝ`, `Ϙ`, `Ϡ`.

### Названия греческих символов

`GreekConvert` предоставляет методы для преобразования Unicode-символов в текстовые названия и обратно:

```python
greek = GreekConvert()

greek.unicode_to_name("αβγ")              # "alpha beta gamma"
greek.name_to_unicode("alpha beta gamma") # "αβγ"
```

Для неизвестного символа или названия возникает `ValueError`.

## Объекты чисел

### `GreekNumber`

Объект `GreekNumber` можно создать из арабского числа или строки с греческой записью:

```python
number = GreekNumber(number=1234)
print(number)              # α_σλδ
print(number.get_number()) # 1234

parsed = GreekNumber(value="α~σλδ", positional=True)
print(parsed.get_number()) # 1234
```

Параметры конструктора `positional` и `capital` задают формат и регистр:

```python
number = GreekNumber(number=1234, positional=True, capital=True)
print(number)  # Α~ΣΛΔ
```

Укажите `number` или `value`; вызов `GreekNumber()` без обоих параметров приводит к `ValueError`.

Основные методы:

- `get_number()` возвращает хранимое арабское значение (`int` или `float`).
- `set_number(value)` изменяет число и заново формирует греческую запись.
- `get_positional()` и `get_capital()` возвращают текущие настройки.
- `set_positional(bool)` и `set_capital(bool)` меняют формат или регистр и заново формируют запись.
- `get_str()` возвращает названия символов через пробел. Например, `GreekNumber(number=123).get_str()` вернёт `"rho kappa gamma"`.

`str(number)` возвращает саму греческую запись.

### `RomanNumber`

Объект `RomanNumber` создаётся из арабского числа:

```python
number = RomanNumber(2024)

print(number)              # MMXXIV
print(number.get_value())  # MMXXIV
print(number.get_number()) # 2024

number.set_number(2025)
print(number)              # MMXXV
```

Для разбора римской строки используйте `RomanConvert.convert_to_arabic()`. Конструктор `RomanNumber` не принимает строку с римской записью.

## Дробные числа

Дробная часть конечного `float` кодируется по десятичным цифрам. Каждая цифра становится отдельным токеном, а токены разделяются двоеточиями:

| Значение | Римская запись | Классическая греческая | Позиционная греческая, прописная |
| ---: | --- | --- | --- |
| `1.25` | `I.(II:V)` | `α.(β:ε)` | `Α.(Β:Ε)` |
| `1.05` | `I.(_:V)` | `α.(_:ε)` | `Α.(~:Ε)` |

Нулевой дробный разряд обозначается `_` в римской и классической греческой записи и `~` в позиционной греческой. Парсер также принимает `0` как вариант нулевого токена:

```python
roman.convert_to_arabic("I.(_:V)")  # 1.05
roman.convert_to_arabic("I.(0:V)")  # 1.05

classic.convert_to_arabic("α.(_:ε)")    # 1.05
positional.convert_to_arabic("α.(~:ε)") # 1.05
```

Формат дробной записи: `целая_часть.(токен:токен:...)`. Значения без дробных цифр (например, `2.0`) отображаются как целые (`II` в римской записи). Для точной обработки десятичной дроби используйте `float`, только если подходит семантика Python `float`: библиотека кодирует кратчайшее десятичное представление значения, а не исходный текст, из которого оно могло быть получено.

`NaN` и бесконечности не поддерживаются и приводят к `ValueError`. Отрицательные значения имеют префикс `-`; отрицательный ноль нормализуется до нуля.

## Арифметика и сравнения

`GreekNumber` и `RomanNumber` поддерживают `+`, `-`, `*`, `/`, `//`, `%`, `**`, унарные `+` и `-`, а также сравнения. В бинарной операции объект числового типа должен находиться слева; справа допустим другой объект одного из этих типов или `int`/`float`:

```python
roman_total = RomanNumber(10) + 5
print(roman_total)              # XV
print(roman_total.get_number()) # 15

greek_total = GreekNumber(number=10, positional=True) * 3
print(greek_total)              # λ
print(greek_total.get_number()) # 30
```

Обычная арифметическая операция создаёт новый объект того же типа, что и левый операнд. Операторы с присваиванием (`+=`, `-=`, `*=`, `/=`, `//=`, `%=`, `**=`) изменяют существующий объект. Результат `GreekNumber` сохраняет режим и регистр левого операнда.

Если оба операнда — целые числа, оператор `/` выполняет деление с усечением к нулю. Оператор `//` использует стандартное для Python округление вниз. Чтобы получить дробный результат, хотя бы один операнд должен быть `float`, например `RomanNumber(5) / 2.0`. Деление на ноль приводит к `ZeroDivisionError`.

## Ошибки и ограничения

- `TypeError` означает неподдерживаемый тип аргумента (например, строку вместо числа в `convert()` или `RomanNumber()`).
- `ValueError` означает неизвестный символ, некорректную римскую или греческую запись/регистр, неверный формат дроби или не конечный `float`.
- `ZeroDivisionError` возникает при делении на ноль в арифметических операциях.
- Целые числа Python не ограничены фиксированным машинным диапазоном, но размер записи ограничен доступной памятью.

При разборе греческих чисел задавайте правильные `positional` и `capital`: конвертер не определяет формат и регистр по входной строке автоматически.

## Выбор Python- или Rust-backend

По умолчанию пакет использует Rust-backend, если доступно бинарное расширение, и автоматически переключается на Python-backend, если расширение недоступно. Имена публичных методов и форматы чисел одинаковы для обоих backend.

Чтобы принудительно выбрать Python-backend, задайте `GREEKROMAN_FORCE_PYTHON=1` до запуска Python:

```bash
GREEKROMAN_FORCE_PYTHON=1 python app.py
```

В PowerShell:

```powershell
$env:GREEKROMAN_FORCE_PYTHON = "1"
python app.py
Remove-Item Env:GREEKROMAN_FORCE_PYTHON
```

Также поддерживаются значения `true`, `yes` и `on` без учёта регистра. Выбор backend кэшируется на время работы процесса, поэтому задавайте переменную окружения до создания первого конвертера.
