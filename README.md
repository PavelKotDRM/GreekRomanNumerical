# English

## Module converting Arabic numerals to Greek and Roman numbers

**Version:** 1.4.0\
**Supported Python:** 3.11-3.14 stable; 3.15.0rc2 provisionally tested\
**Repository:** [GitHub - GreekRomanNumerical](https://github.com/PavelKotDRM/GreekRomanNumerical)  
**License:** Apache 2.0

### Description

The library converts Arabic numbers, such as `1234`, to Roman equivalents, such as `MCCXXXIV`, or Greek — `Α_ΣΛΔ`.

This module can also output Greek numbers in different formats. For example, the number `20005003001` can be represented as `Κ___Ε__Γ_Α` or `Κ~Ε~Γ~Α`. In addition, it is possible to output the text name of the digits, for example, `Kappa macron Epsilon macron Gamma macron Alpha`, or output them in lowercase.  

Finite float fractions are encoded digit by digit, with numeral tokens separated by colons. For example, `1.25` becomes `I.(II:V)` or `α.(β:ε)`. A zero digit is written as `_` for Roman numerals and classic Greek, or `~` for positional Greek; thus `1.05` becomes `I.(_:V)`, `α.(_:ε)`, or `α.(~:ε)`.

### Historical-style fractions (optional)

The [`historical_fractions`](./docs/USAGE.md#historical-style-fractions-optional) module adds an opt-in, modern notation without changing the default decimal-fraction format. Roman fractions use `S` (1/2), the uncia sign (1/12), and the semuncia sign (1/24); the value must be representable in steps of 1/24. Greek fractions use sums of unit fractions. The module also renders these notations as LaTeX or MathML.

```python
from GreekRomanUtils import historical_fractions

historical_fractions.arabic_to_roman(0.5)  # ".(S)"
historical_fractions.arabic_to_greek(3.14)  # "γ.(α/η+α/ξζ+α/ι_γ_υ)"
historical_fractions.arabic_to_roman_latex(3.5)  # r"\text{III}+\frac{1}{2}"
```

These functions require the Rust extension. If it is unavailable or `GREEKROMAN_FORCE_PYTHON=1` selects the Python backend, historical-fraction calls raise `RuntimeError`; the existing `GreekConvert` and `RomanConvert` APIs continue to fall back to Python. See the [detailed guide](./docs/USAGE.md#historical-style-fractions-optional) for parsing and display APIs.

### Installation

Install the package using pip:

```bash
pip install GreekRomanUtils
```

### Detailed usage

For step-by-step examples of the converters, number formats, arithmetic, and backend selection, see the [detailed usage guide](./docs/USAGE.md).

### Hybrid backend (Python + Rust)

The existing `GreekConvert` and `RomanConvert` APIs select the Rust backend when available and otherwise fall back to Python. The separate `historical_fractions` API uses the Rust extension directly and does not have a Python fallback.

- Default behavior: try Rust backend first, fallback to Python automatically.
- Force Python backend:

```bash
GREEKROMAN_FORCE_PYTHON=1
```

The Rust bridge preserves Python's arbitrary-precision integers. The core library applies input, output, and Greek-group limits to bound resource use.

### Development environment and quality checks

Requirements: Python 3.11 or newer, `uv`, and [rustup](https://rustup.rs). Windows builds also require the MSVC C++ Build Tools.

The Rust core is included as the [`greekromannumerical-core`](./greekromannumerical-core) Git submodule. Clone this repository with submodules, or initialize them in an existing checkout:

```bash
git clone --recurse-submodules git@github.com:PavelKotDRM/GreekRomanNumerical.git
# Existing checkout:
git submodule update --init --recursive
```

The core repository is accessed over SSH. GitHub Actions also needs a `CORE_SUBMODULE_TOKEN` repository secret: a read-only token with `Contents: read` access to both this repository and the core repository.

Create the environment and install the project with its Rust extension:

```bash
rustup toolchain install stable
uv python install 3.11
uv sync --locked --group dev --python 3.11
```

Install the optional notebook tools only when needed:

```bash
uv sync --locked --group dev --group notebook --python 3.11
```

Run the full test suite with the Python backend:

```bash
GREEKROMAN_FORCE_PYTHON=1 uv run pytest -v
```

On Windows PowerShell:

```powershell
$env:GREEKROMAN_FORCE_PYTHON = "1"
uv run pytest -v
Remove-Item Env:GREEKROMAN_FORCE_PYTHON
```

Rebuild the Rust extension after Rust changes and test the hybrid backend:

```bash
uv run maturin develop --manifest-path rust/Cargo.toml
uv run pytest -v
```

Run Python lint and type checks:

```bash
uv run ruff check --exclude tests/
uv run ty check --exclude tests/
```

Check Rust formatting, compile the Rust crate, and build the package:

```bash
cargo fmt --manifest-path rust/Cargo.toml --check
cargo test --locked --manifest-path rust/Cargo.toml
uv build
```

Rust behavior is covered by native unit tests and Python backend-equivalence tests.

Run the opt-in performance benchmarks (the Rust extension must be built):

```bash
uv sync --locked --group dev --group performance --python 3.11
uv run maturin develop --manifest-path rust/Cargo.toml
uv run --group performance pytest benchmarks/test_backend_performance.py --benchmark-only --benchmark-sort=mean
```

The benchmark checks result equivalence before timing Roman, classic Greek, and positional Greek conversions in both backends. It reports measurements without enforcing a speed threshold because timings depend on the machine.

### Project structure

- `GreekRomanUtils/GreekRoman.py` exposes `GreekConvert` and `RomanConvert`; the number objects are `GreekNumber` and `RomanNumber`.
- `GreekRomanUtils/_backend.py` selects and caches the standard conversion backend. `GreekRomanUtils/_python_impl.py` provides its Python fallback, while `GreekRomanUtils/_rust_impl.py` wraps the native extension.
- `GreekRomanUtils/historical_fractions.py` exposes the optional historical notation and renderers. It requires the Rust extension and does not use the standard backend fallback.
- The Rust extension delegates conversions to the `greekromannumerical-core` submodule, pinned at `v0.2.0`.

See the [project architecture diagram](./Diagrams/Architecture.drawio.svg) for the module and backend relationships.

### Main functions

**For "GreekConvert":**

- `change_capital` — A flag that controls the conversion of characters to upper or lower case.
- `change_positional` — Change the positional mode for conversion.
- `convert` — The function of converting an Arabic number to a Greek one, returns `GreekNumber` object. For example, the number `20005003001` is converted to `Κ___Ε__Γ_Α` (non-positional mode) or to `Κ~Ε~Γ~Α` (positional mode).
- `convert_to_arabic` — A function for converting a Greek number to an Arabic one.
- `unicode_to_name` — The function converts a Unicode character into its name.
- `name_to_unicode` — The reverse operation for `unicode_to_name`.

**The "GreekNumber" class:**

- `set_number` — Set a new value.
- `set_positional` — Set the positional mode flag (affects display format: underscore `_` for non-positional, tilde `~` for positional).
- `set_capital` — Set the upper case flag.
- `get_number` — Get the current number.
- `get_positional` — Get the positional flag value.
- `get_capital` — Get the capital flag value.
- `get_str` — Get the textual representation of the number (e.g., "alpha beta gamma").
- And basic mathematical operations (+, -, *, /, //, %, **, ==, !=, <, <=, >, >=).

**For "RomanConvert":**

- `convert` — The method converts an Arabic number to a Roman number, returns `RomanNumber` object.
- `convert_to_arabic` — The reverse method for `convert`.

**For "RomanNumber":**

- `set_number` — Set a new value.
- `get_number` — Get the current number.
- `get_value` — Get the string representation of the Roman numeral.
- And basic mathematical operations (+, -, *, /, //, %, **, ==, !=, <, <=, >, >=).

----------------------

## Ru

## Модуль преобразование арабских цифр в греческие и римские числа

**Версия:** 1.4.0\
**Поддерживаемые версии Python:** 3.11-3.14 stable; 3.15.0rc2 проверяется предварительно\
**Репозиторий:** [GitHub - GreekRomanNumerical](https://github.com/PavelKotDRM/GreekRomanNumerical)  
**Лицензия:** Apache 2.0

## Описание

Библиотека преобразует арабские числа, такие как `1234`, в римские эквиваленты, например, `MCCXXXIV`, или греческие — `Α_ΣΛΔ`.

Также этот модуль может выводить греческие цифры в разных форматах. Например, число `20005003001` можно представить как `Κ___Ε__Γ_Α` или `Κ~Ε~Γ~Α`. Кроме того, есть возможность выводить текстовое название цифр, например, `Kappa macron Epsilon macron Gamma macron Alpha`, или выводить их в нижнем регистре.

Дробная часть конечного `float` кодируется по цифрам, разделённым двоеточиями. Например, `1.25` преобразуется в `I.(II:V)` или `α.(β:ε)`. Нулевой разряд записывается как `_` для римского и классического греческого форматов, или `~` для позиционного греческого; поэтому `1.05` выглядит как `I.(_:V)`, `α.(_:ε)` или `α.(~:ε)`.

### Дроби в исторически вдохновлённой записи (необязательно)

Модуль [`historical_fractions`](./docs/USAGE_RU.md) добавляет современный дополнительный формат, не меняя стандартную десятичную запись дробей. Римские дроби используют `S` (1/2), знак унции (1/12) и полу-унции (1/24); значение должно представляться долями 1/24. Греческие дроби записываются суммами единичных дробей. Модуль также поддерживает рендеринг этих форматов в LaTeX и MathML.

```python
from GreekRomanUtils import historical_fractions

historical_fractions.arabic_to_roman(0.5)  # ".(S)"
historical_fractions.arabic_to_greek(3.14)  # "γ.(α/η+α/ξζ+α/ι_γ_υ)"
historical_fractions.arabic_to_roman_latex(3.5)  # r"\text{III}+\frac{1}{2}"
```

Для этих функций требуется Rust-расширение. Если оно недоступно или выбран Python-backend через `GREEKROMAN_FORCE_PYTHON=1`, вызов исторических дробей приводит к `RuntimeError`; обычные API `GreekConvert` и `RomanConvert` сохраняют fallback на Python. Подробности о разборе и функциях отображения см. в [руководстве](./docs/USAGE_RU.md).

### Установка

Установите пакет с помощью pip:

```bash
pip install GreekRomanUtils
```

### Подробная документация

Подробные примеры конвертации, форматов чисел, арифметики и настройки backend собраны в [руководстве на русском языке](./docs/USAGE_RU.md). См. также [английскую версию](./docs/USAGE.md).

### Гибридный backend (Python + Rust)

Существующие API `GreekConvert` и `RomanConvert` используют Rust-backend, если он доступен, и иначе переключаются на Python. Отдельный API `historical_fractions` требует Rust-расширение и не имеет Python-fallback.

- Поведение по умолчанию: сначала попытка Rust backend, при недоступности автоматический fallback на Python.
- Принудительное отключение Rust backend:

```bash
GREEKROMAN_FORCE_PYTHON=1
```

Rust-мост сохраняет произвольную точность целых Python. Core-библиотека ограничивает размер входа и результата, а также число греческих разрядов, чтобы контролировать расход ресурсов.

### Настройка среды и проверки качества

Требования: Python 3.11 или новее, `uv` и [rustup](https://rustup.rs). Для сборки в Windows также нужны MSVC C++ Build Tools.

Rust core подключён как Git submodule [`greekromannumerical-core`](./greekromannumerical-core). Клонируйте репозиторий вместе с submodule или инициализируйте его в уже существующей копии:

```powershell
git clone --recurse-submodules git@github.com:PavelKotDRM/GreekRomanNumerical.git
# Для уже клонированного репозитория:
git submodule update --init --recursive
```

Core-репозиторий доступен по SSH. Для GitHub Actions также задайте секрет репозитория `CORE_SUBMODULE_TOKEN`: токен только для чтения с правом `Contents: read` для обоих репозиториев.

Создание окружения и установка проекта вместе с Rust-расширением:

```powershell
rustup toolchain install stable
uv python install 3.11
uv sync --locked --group dev --python 3.11
```

Дополнительные инструменты для ноутбуков устанавливаются отдельно:

```powershell
uv sync --locked --group dev --group notebook --python 3.11
```

Полный набор тестов с Python backend:

```powershell
$env:GREEKROMAN_FORCE_PYTHON = "1"
uv run pytest -v
Remove-Item Env:GREEKROMAN_FORCE_PYTHON
```

После изменений Rust пересоберите расширение и запустите тесты в hybrid-режиме:

```powershell
uv run maturin develop --manifest-path rust/Cargo.toml
uv run pytest -v
```

Проверки Python-кода:

```powershell
uv run ruff check --exclude tests/
uv run ty check --exclude tests/
```

Проверки Rust и сборка пакета:

```powershell
cargo fmt --manifest-path rust/Cargo.toml --check
cargo test --locked --manifest-path rust/Cargo.toml
uv build
```

Поведение Rust backend покрывается собственными unit-тестами и Python-тестами эквивалентности backend-ов.

Запуск opt-in тестов производительности (Rust-расширение должно быть собрано):

```powershell
uv sync --locked --group dev --group performance --python 3.11
uv run maturin develop --manifest-path rust/Cargo.toml
uv run --group performance pytest benchmarks/test_backend_performance.py --benchmark-only --benchmark-sort=mean
```

Перед замером тесты проверяют равенство результатов и затем измеряют Roman, classic Greek и positional Greek конвертации в обоих backend’ах. Порог скорости не задан: время зависит от машины и окружения.

## Структура проекта

- `GreekRomanUtils/GreekRoman.py` предоставляет `GreekConvert` и `RomanConvert`; числовые объекты — `GreekNumber` и `RomanNumber`.
- `GreekRomanUtils/_backend.py` выбирает и кэширует backend стандартных конвертеров. `GreekRomanUtils/_python_impl.py` обеспечивает Python-fallback, а `GreekRomanUtils/_rust_impl.py` вызывает нативное расширение.
- `GreekRomanUtils/historical_fractions.py` предоставляет дополнительную историческую запись и рендеринг; для неё требуется Rust-расширение без Python-fallback.
- Rust-расширение передаёт преобразования в submodule `greekromannumerical-core`, закреплённый на `v0.2.0`.

Связи модулей и backend показаны на [схеме архитектуры проекта](./Diagrams/Architecture.drawio.svg).

## Основные функции

**Для «GreekConvert»:**

- `change_capital` — Флаг, управляющий преобразованием символов в верхний или нижний регистр.
- `change_positional` — Изменить режим позиционного преобразования.
- `convert` — Функция преобразования арабского числа в греческое, возвращает объект `GreekNumber`. Например, число `20005003001` преобразуется в `Κ___Ε__Γ_Α` (непозиционный режим) или в `Κ~Ε~Γ~Α` (позиционный режим).
- `convert_to_arabic` — Функция преобразования греческого числа в арабское.
- `unicode_to_name` — Функция преобразует символ Unicode в его название.
- `name_to_unicode` — Обратная операция для `unicode_to_name`.

**Класс «GreekNumber»:**

- `set_number` — Установить новое значение.
- `set_positional` — Установить флаг позиционного режима (влияет на формат отображения: подчеркивание `_` для непозиционного, тильда `~` для позиционного).
- `set_capital` — Установить флаг верхнего регистра.
- `get_number` — Получить текущее число.
- `get_positional` — Получить значение флага позиционности.
- `get_capital` — Получить значение флага регистра.
- `get_str` — Получить текстовое представление числа (например, "alpha beta gamma").
- И базовые математические операции (+, -, *, /, //, %, **, ==, !=, <, <=, >, >=).

**Для «RomanConvert»:**

- `convert` — Метод преобразует арабское число в римское, возвращает объект `RomanNumber`.
- `convert_to_arabic` — Обратный метод для `convert`.

**Для «RomanNumber»:**

- `set_number` — Установить новое значение.
- `get_number` — Получить текущее число.
- `get_value` — Получить строковое представление римского числа.
- И базовые математические операции (+, -, *, /, //, %, **, ==, !=, <, <=, >, >=).

**Архитектура проекта**

![Архитектура проекта](./Diagrams/Architecture.drawio.svg)

## License

Apache License 2.0  
