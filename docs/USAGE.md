# GreekRomanUtils Usage Guide

**Languages:** English | [Русский](./USAGE_RU.md)

GreekRomanUtils converts Python integers and finite `float` values to Roman or Greek numeral notation and back. Its user-facing API provides the `RomanConvert` and `GreekConvert` converters, plus the `RomanNumber` and `GreekNumber` value objects.

## Installation

Python 3.11 or newer is required:

```bash
python -m pip install GreekRomanUtils
```

When a compatible wheel is available, no Rust toolchain is needed. If the package must be built from source, Rust stable, maturin, and (on Windows) the MSVC C++ Build Tools may be required.

## Import and first conversion

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

`convert()` returns a numeral object, not a plain string. Use `str(value)` or `print(value)` to display its numeral, and `get_number()` to retrieve its Arabic numeric value.

## Roman numerals

### Converting to Roman notation

```python
from GreekRomanUtils.GreekRoman import RomanConvert

roman = RomanConvert()

print(roman.convert(4))        # IV
print(roman.convert(2024))     # MMXXIV
print(roman.convert(5000))     # ~V
print(roman.convert(-1234))    # -MCCXXXIV
```

The standard symbols are `I`, `V`, `X`, `L`, `C`, `D`, and `M`, with the subtractive pairs `IV`, `IX`, `XL`, `XC`, `CD`, and `CM`. Extended tokens represent larger values: `~V` = 5,000, `~X` = 10,000, `~L` = 50,000, `~C` = 100,000, `~D` = 500,000, and `~M` = 1,000,000.

Zero is represented by an empty string:

```python
str(roman.convert(0))  # ""
```

Python integers have arbitrary precision. In practice, the limit is the available memory and the size of the resulting numeral string.

### Converting Roman notation to an integer

```python
roman.convert_to_arabic("MMXXIV")         # 2024
roman.convert_to_arabic("~C~X~XMMMCDLVI") # 123456
roman.convert_to_arabic("-IV")            # -4
roman.convert_to_arabic("")               # 0
```

Pass Roman symbols in uppercase. The parser recognizes supported tokens and rejects unknown symbols, but it is not intended to validate every rule of canonical Roman spelling.

## Greek numerals

### Classic, positional, and uppercase modes

`GreekConvert` accepts three constructor arguments:

```python
GreekConvert(capital=False, debug=False, positional=False)
```

- `capital=False` selects lowercase Greek symbols; `True` selects uppercase symbols.
- `positional=False` selects classic notation, which uses `_` for powers of 1,000. `True` selects positional notation, with base-1,000 groups separated by `~`.
- `debug=False` disables diagnostic output by default.

```python
from GreekRomanUtils.GreekRoman import GreekConvert

classic = GreekConvert()
positional = GreekConvert(positional=True)
uppercase = GreekConvert(positional=True, capital=True)

print(classic.convert(1234))     # α_σλδ
print(positional.convert(1234))  # α~σλδ
print(uppercase.convert(1234))   # Α~ΣΛΔ
```

Use the same `positional` setting to parse a numeral as was used to produce it. The `capital` setting must also match the input symbols' case.

```python
positional.convert_to_arabic("α~σλδ")  # 1234
uppercase.convert_to_arabic("Α~ΣΛΔ")   # 1234
```

Empty groups in positional notation preserve place values. Do not remove `~` separators, even when a group between them contains no symbols.

You can change the converter's mode for subsequent conversions. Existing `GreekNumber` objects are not changed:

```python
greek = GreekConvert()
greek.change_positional(True)
greek.change_capital(True)

print(greek.convert(1234))  # Α~ΣΛΔ
```

### Converting Greek notation to an integer

```python
classic = GreekConvert()
classic.convert_to_arabic("α_σλδ")  # 1234

positional = GreekConvert(positional=True)
positional.convert_to_arabic("α~σλδ")  # 1234
```

Zero is represented by an empty string, and negative values have a leading `-`. The Greek numeral alphabet has 27 symbols for units, tens, and hundreds. Special symbols include `ϝ` (6), `ϙ` (90), and `ϡ` (900), with uppercase forms `Ϝ`, `Ϙ`, and `Ϡ`.

### Greek symbol names

`GreekConvert` provides methods for translating between Unicode symbols and their text names:

```python
greek = GreekConvert()

greek.unicode_to_name("αβγ")              # "alpha beta gamma"
greek.name_to_unicode("alpha beta gamma") # "αβγ"
```

An unknown symbol or name raises `ValueError`.

## Number objects

### `GreekNumber`

Create a `GreekNumber` from an Arabic value or a Greek numeral string:

```python
number = GreekNumber(number=1234)
print(number)              # α_σλδ
print(number.get_number()) # 1234

parsed = GreekNumber(value="α~σλδ", positional=True)
print(parsed.get_number()) # 1234
```

The `positional` and `capital` constructor arguments select the notation and case:

```python
number = GreekNumber(number=1234, positional=True, capital=True)
print(number)  # Α~ΣΛΔ
```

Provide `number` or `value`; calling `GreekNumber()` without either argument raises `ValueError`.

Main methods:

- `get_number()` returns the stored Arabic value (`int` or `float`).
- `set_number(value)` changes the value and regenerates the Greek numeral.
- `get_positional()` and `get_capital()` return the current settings.
- `set_positional(bool)` and `set_capital(bool)` change the format or case and regenerate the numeral.
- `get_str()` returns the symbol names separated by spaces. For example, `GreekNumber(number=123).get_str()` returns `"rho kappa gamma"`.

`str(number)` returns the Greek numeral itself.

### `RomanNumber`

Create a `RomanNumber` from an Arabic value:

```python
number = RomanNumber(2024)

print(number)              # MMXXIV
print(number.get_value())  # MMXXIV
print(number.get_number()) # 2024

number.set_number(2025)
print(number)              # MMXXV
```

To parse a Roman numeral string, use `RomanConvert.convert_to_arabic()`. `RomanNumber` does not have a constructor that accepts a Roman numeral string.

## Fractional numbers

The fractional part of a finite `float` is encoded digit by digit. Each decimal digit becomes a separate numeral token, and tokens are separated by colons:

| Value | Roman notation | Classic Greek | Positional uppercase Greek |
| ---: | --- | --- | --- |
| `1.25` | `I.(II:V)` | `α.(β:ε)` | `Α.(Β:Ε)` |
| `1.05` | `I.(_:V)` | `α.(_:ε)` | `Α.(~:Ε)` |

The zero fractional digit is `_` in Roman and classic Greek notation, and `~` in positional Greek notation. The parser also accepts `0` as a zero-token spelling:

```python
roman.convert_to_arabic("I.(_:V)")  # 1.05
roman.convert_to_arabic("I.(0:V)")  # 1.05

classic.convert_to_arabic("α.(_:ε)")    # 1.05
positional.convert_to_arabic("α.(~:ε)") # 1.05
```

The fractional form is `integer_part.(token:token:...)`. Values without fractional digits (for example, `2.0`) are rendered as integers (`II` in Roman notation). For exact decimal handling, use `float` only when Python's `float` semantics are appropriate: the library encodes the shortest decimal representation of the value, not the original text from which it may have been parsed.

`NaN` and infinities are not supported and raise `ValueError`. Negative values use a leading `-`; negative zero is normalized to zero.

## Arithmetic and comparisons

`GreekNumber` and `RomanNumber` support `+`, `-`, `*`, `/`, `//`, `%`, `**`, unary `+` and `-`, and comparisons. In a binary operation, the numeral object must be on the left; the right-hand operand may be another object of either type or an `int`/`float`:

```python
roman_total = RomanNumber(10) + 5
print(roman_total)              # XV
print(roman_total.get_number()) # 15

greek_total = GreekNumber(number=10, positional=True) * 3
print(greek_total)              # λ
print(greek_total.get_number()) # 30
```

Regular arithmetic creates a new object of the same type as the left operand. In-place operators (`+=`, `-=`, `*=`, `/=`, `//=`, `%=`, `**=`) update the existing object. A `GreekNumber` result keeps the notation and case of the left operand.

When both operands are integers, `/` truncates toward zero. `//` uses Python's floor-division behavior. To get a fractional result, make at least one operand a `float`, for example `RomanNumber(5) / 2.0`. Division by zero raises `ZeroDivisionError`.

## Errors and limits

- `TypeError` indicates an unsupported argument type (for example, passing a string instead of a number to `convert()` or `RomanNumber()`).
- `ValueError` indicates an unknown symbol, invalid Greek notation or case, malformed fractional notation, or a non-finite `float`.
- `ZeroDivisionError` indicates division by zero in arithmetic.
- Python `int` values are not limited to a fixed machine range, but numeral output is limited by available memory.

When parsing Greek numerals, choose the correct `positional` and `capital` settings; the converter does not infer the notation or case from the input string.

## Selecting the Python or Rust backend

By default, the package uses the Rust backend when its binary extension is available and automatically falls back to the Python backend when it is not. Public method names and numeral formats are the same for both backends.

To force the Python backend, set `GREEKROMAN_FORCE_PYTHON=1` before starting Python:

```bash
GREEKROMAN_FORCE_PYTHON=1 python app.py
```

In PowerShell:

```powershell
$env:GREEKROMAN_FORCE_PYTHON = "1"
python app.py
Remove-Item Env:GREEKROMAN_FORCE_PYTHON
```

The values `true`, `yes`, and `on` are also supported, case-insensitively. Backend selection is cached for the process, so set the environment variable before creating the first converter.
