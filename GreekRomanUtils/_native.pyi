from collections.abc import Iterable as _Iterable
from types import TracebackType as _TracebackType
from typing import Self as _Self

class ProgressBar:
    def __init__(self, total: int, message: str | None = None) -> None: ...
    @property
    def total(self) -> int: ...
    @property
    def position(self) -> int: ...
    def set_message(self, message: str) -> None: ...
    def set_position(self, position: int) -> None: ...
    def inc(self, amount: int = 1) -> None: ...
    def finish(self) -> None: ...
    def __enter__(self) -> _Self: ...
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: _TracebackType | None,
    ) -> bool: ...

def arabic_to_roman(number: float) -> str: ...


def arabic_to_roman_parallel(
    numbers: _Iterable[int | float],
    progress: bool = False,
    message: str | None = None,
) -> list[str]: ...


def roman_to_arabic(numeral: str) -> int | float: ...


def arabic_to_greek(number: float, positional: bool, capital: bool) -> str: ...


def arabic_to_greek_parallel(
    numbers: _Iterable[int | float],
    positional: bool,
    capital: bool,
    progress: bool = False,
    message: str | None = None,
) -> list[str]: ...


def greek_to_arabic(numeral: str, positional: bool, capital: bool) -> int | float: ...


def historical_arabic_to_roman(number: float) -> str: ...


def historical_roman_to_arabic(numeral: str) -> int | float: ...


def historical_arabic_to_greek(number: float, positional: bool, capital: bool) -> str: ...


def historical_greek_to_arabic(
    numeral: str,
    positional: bool,
    capital: bool,
) -> int | float: ...


def historical_arabic_to_roman_latex(number: float) -> str: ...


def historical_arabic_to_roman_mathml(number: float) -> str: ...


def historical_arabic_to_greek_latex(
    number: float,
    positional: bool,
    capital: bool,
) -> str: ...


def historical_arabic_to_greek_mathml(
    number: float,
    positional: bool,
    capital: bool,
) -> str: ...
