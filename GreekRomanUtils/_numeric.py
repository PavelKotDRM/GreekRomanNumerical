import math
from collections.abc import Callable
from decimal import Decimal


def split_float(number: float) -> tuple[int, str, bool]:
    if not math.isfinite(number):
        raise ValueError("Float values must be finite")

    value = Decimal(str(abs(number)))
    whole = int(value)
    fraction = format(value - whole, "f").partition(".")[2].rstrip("0")
    return whole, fraction, number < 0


def format_float_numeral(number: float, convert_integer: Callable[[int], str]) -> str:
    whole, fraction, negative = split_float(number)
    numeral = convert_integer(whole)
    if fraction:
        encoded_digits = ":".join(
            "0" if digit == "0" else convert_integer(int(digit))
            for digit in fraction
        )
        numeral = f"{numeral}.({encoded_digits})"
    if negative:
        numeral = f"-{numeral}"
    return numeral


def parse_decimal_numeral(
    numeral: str,
    convert_integer: Callable[[str], int],
) -> int | float:
    negative = numeral.startswith("-")
    if negative:
        numeral = numeral[1:]

    if "." not in numeral:
        value = convert_integer(numeral)
        return -value if negative else value

    if numeral.count(".") != 1:
        raise ValueError(f"Invalid decimal numeral: {numeral}")

    integer_numeral, encoded_fraction = numeral.split(".")
    if not encoded_fraction.startswith("(") or not encoded_fraction.endswith(")"):
        raise ValueError(f"Invalid decimal numeral: {numeral}")

    fraction_tokens = encoded_fraction[1:-1].split(":")
    if not fraction_tokens or any(not token for token in fraction_tokens):
        raise ValueError(f"Invalid decimal numeral: {numeral}")

    fraction_digits = []
    for token in fraction_tokens:
        if token == "0":
            fraction_digits.append("0")
            continue
        digit = convert_integer(token)
        if not 1 <= digit <= 9:
            raise ValueError(f"Invalid decimal numeral: {numeral}")
        fraction_digits.append(str(digit))

    integer = convert_integer(integer_numeral)
    value = float(f"{integer}.{''.join(fraction_digits)}")
    if not math.isfinite(value):
        raise ValueError("Decimal numeral is outside the supported float range")
    return -value if negative else value