//! Roman numeral conversion, including the package's extended and decimal forms.
//!
//! Fractional decimal digits are encoded independently and separated by `:`. A zero digit is
//! written as `0`, preserving its place. For example, `1.05` is represented as `I.(0:V)`.

use crate::common::{
    ArabicInput, decimal_float_value, decode_fractional_digits, encode_fractional_digits,
    extract_arabic_input, fractional_numeral_parts,
};
use num_bigint::BigInt;
use num_traits::ToPrimitive;
use pyo3::exceptions::{PyMemoryError, PyOverflowError, PyValueError};
use pyo3::prelude::*;
use pyo3::types::PyFloat;

const ROMAN_NUMERAL_LIST: [(&str, i64); 19] = [
    ("~M", 1_000_000),
    ("~D", 500_000),
    ("~C", 100_000),
    ("~L", 50_000),
    ("~X", 10_000),
    ("~V", 5_000),
    ("M", 1_000),
    ("CM", 900),
    ("D", 500),
    ("CD", 400),
    ("C", 100),
    ("XC", 90),
    ("L", 50),
    ("XL", 40),
    ("X", 10),
    ("IX", 9),
    ("V", 5),
    ("IV", 4),
    ("I", 1),
];

/// Converts an Arabic integer or finite float to an extended Roman numeral.
///
/// Fractional digits are converted one at a time; zeroes remain explicit placeholders.
///
/// # Python example
///
/// ```python
/// >>> arabic_to_roman(1.25)
/// 'I.(II:V)'
/// ```
#[pyfunction]
pub fn arabic_to_roman(number: &Bound<'_, PyAny>) -> PyResult<String> {
    match extract_arabic_input(number)? {
        ArabicInput::Integer(number) => arabic_to_roman_integer(number),
        ArabicInput::Float {
            whole,
            fraction,
            negative,
        } => {
            let mut numeral = arabic_to_roman_integer(whole)?;
            if !fraction.is_empty() {
                let encoded = encode_fractional_digits(&fraction, |digit| {
                    arabic_to_roman_integer(BigInt::from(digit))
                })?;
                numeral.push_str(".(");
                numeral.push_str(&encoded);
                numeral.push(')');
            }
            if negative {
                numeral.insert(0, '-');
            }
            Ok(numeral)
        }
    }
}

fn arabic_to_roman_integer(number: BigInt) -> PyResult<String> {
    if number <= BigInt::from(0) {
        return Ok(String::new());
    }
    let mut input = number;
    let mut out = String::new();
    for (numeral, value) in ROMAN_NUMERAL_LIST {
        let value = BigInt::from(value);
        let count = (&input / &value)
            .to_usize()
            .ok_or_else(|| PyOverflowError::new_err("Roman numeral output is too large"))?;
        if count > 0 {
            let added_len = numeral
                .len()
                .checked_mul(count)
                .ok_or_else(|| PyOverflowError::new_err("Roman numeral output is too large"))?;
            out.try_reserve(added_len)
                .map_err(|_| PyMemoryError::new_err("Roman numeral output is too large"))?;
            for _ in 0..count {
                out.push_str(numeral);
            }
            input -= value * BigInt::from(count);
        }
    }
    Ok(out)
}

/// Converts an extended Roman numeral back to an Arabic integer or float.
///
/// This accepts fractional forms produced by [`arabic_to_roman`], such as `I.(0:V)`.
///
/// # Python example
///
/// ```python
/// >>> roman_to_arabic('I.(0:V)')
/// 1.05
/// ```
#[pyfunction]
pub fn roman_to_arabic<'py>(py: Python<'py>, numeral: &str) -> PyResult<Bound<'py, PyAny>> {
    let (negative, numeral) = match numeral.strip_prefix('-') {
        Some(numeral) => (true, numeral),
        None => (false, numeral),
    };
    if let Some((integer_numeral, fraction)) = fractional_numeral_parts(numeral)? {
        let whole = roman_to_arabic_integer(integer_numeral)?;
        let fraction_digits = decode_fractional_digits(fraction, roman_to_arabic_integer)?;
        let value = decimal_float_value(&whole, &fraction_digits, negative)?;
        return Ok(PyFloat::new(py, value).into_any());
    }

    let mut total = roman_to_arabic_integer(numeral)?;
    if negative {
        total = -total;
    }
    Ok(total.into_pyobject(py)?.into_any())
}

fn roman_to_arabic_integer(numeral: &str) -> PyResult<BigInt> {
    let bytes = numeral.as_bytes();
    let mut index = 0usize;
    let mut total = BigInt::from(0);

    while index < bytes.len() {
        let Some((value, consumed)) = roman_token_value(bytes, index) else {
            return Err(PyValueError::new_err(format!("Invalid name: {numeral}")));
        };
        total += value;
        index += consumed;
    }

    Ok(total)
}

fn roman_token_value(bytes: &[u8], index: usize) -> Option<(i64, usize)> {
    let first = *bytes.get(index)?;
    if first == b'~' {
        let second = *bytes.get(index + 1)?;
        let value = match second {
            b'M' => 1_000_000,
            b'D' => 500_000,
            b'C' => 100_000,
            b'L' => 50_000,
            b'X' => 10_000,
            b'V' => 5_000,
            _ => return None,
        };
        return Some((value, 2));
    }

    if let Some(&second) = bytes.get(index + 1) {
        let value = match (first, second) {
            (b'C', b'M') => Some(900),
            (b'C', b'D') => Some(400),
            (b'X', b'C') => Some(90),
            (b'X', b'L') => Some(40),
            (b'I', b'X') => Some(9),
            (b'I', b'V') => Some(4),
            _ => None,
        };
        if let Some(value) = value {
            return Some((value, 2));
        }
    }

    let value = match first {
        b'M' => Some(1_000),
        b'D' => Some(500),
        b'C' => Some(100),
        b'L' => Some(50),
        b'X' => Some(10),
        b'V' => Some(5),
        b'I' => Some(1),
        _ => None,
    };
    value.map(|value| (value, 1))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn integer_numerals_round_trip() {
        for (number, expected) in [
            (0, ""),
            (1, "I"),
            (4, "IV"),
            (9, "IX"),
            (44, "XLIV"),
            (2024, "MMXXIV"),
            (5000, "~V"),
            (123456, "~C~X~XMMMCDLVI"),
        ] {
            let number = BigInt::from(number);
            assert_eq!(arabic_to_roman_integer(number.clone()).unwrap(), expected);
            assert_eq!(roman_to_arabic_integer(expected).unwrap(), number);
        }
    }

    #[test]
    fn fractional_digit_tokens_preserve_zeroes() {
        let encoded =
            encode_fractional_digits("105", |digit| arabic_to_roman_integer(BigInt::from(digit)))
                .unwrap();
        assert_eq!(encoded, "I:0:V");
        assert_eq!(
            decode_fractional_digits(&encoded, roman_to_arabic_integer).unwrap(),
            "105"
        );
    }

    #[test]
    fn rejects_invalid_roman_tokens() {
        assert!(roman_to_arabic_integer("ABC").is_err());
        assert!(decode_fractional_digits("X", roman_to_arabic_integer).is_err());
    }
}
