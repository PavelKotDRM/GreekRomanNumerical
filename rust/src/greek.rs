//! Greek numeral conversion in classic and positional forms.
//!
//! Fractional digits are converted independently using the selected case and Greek format.
//! For example, `1.25` in lowercase classic form is `α.(β:ε)`.

use crate::common::{
    ArabicInput, decimal_float_value, decode_fractional_digits, encode_fractional_digits,
    extract_arabic_input, fractional_numeral_parts,
};
use num_bigint::BigInt;
use pyo3::exceptions::{PyOverflowError, PyValueError};
use pyo3::prelude::*;
use pyo3::types::PyFloat;

#[derive(Clone, Copy)]
struct GreekPair {
    numeral: &'static str,
    value: i64,
}

const GREEK_NUMERAL_LIST: [GreekPair; 27] = [
    GreekPair {
        numeral: "α",
        value: 1,
    },
    GreekPair {
        numeral: "β",
        value: 2,
    },
    GreekPair {
        numeral: "γ",
        value: 3,
    },
    GreekPair {
        numeral: "δ",
        value: 4,
    },
    GreekPair {
        numeral: "ε",
        value: 5,
    },
    GreekPair {
        numeral: "ϝ",
        value: 6,
    },
    GreekPair {
        numeral: "ζ",
        value: 7,
    },
    GreekPair {
        numeral: "η",
        value: 8,
    },
    GreekPair {
        numeral: "θ",
        value: 9,
    },
    GreekPair {
        numeral: "ι",
        value: 10,
    },
    GreekPair {
        numeral: "κ",
        value: 20,
    },
    GreekPair {
        numeral: "λ",
        value: 30,
    },
    GreekPair {
        numeral: "μ",
        value: 40,
    },
    GreekPair {
        numeral: "ν",
        value: 50,
    },
    GreekPair {
        numeral: "ξ",
        value: 60,
    },
    GreekPair {
        numeral: "ο",
        value: 70,
    },
    GreekPair {
        numeral: "π",
        value: 80,
    },
    GreekPair {
        numeral: "ϙ",
        value: 90,
    },
    GreekPair {
        numeral: "ρ",
        value: 100,
    },
    GreekPair {
        numeral: "σ",
        value: 200,
    },
    GreekPair {
        numeral: "τ",
        value: 300,
    },
    GreekPair {
        numeral: "υ",
        value: 400,
    },
    GreekPair {
        numeral: "φ",
        value: 500,
    },
    GreekPair {
        numeral: "χ",
        value: 600,
    },
    GreekPair {
        numeral: "ψ",
        value: 700,
    },
    GreekPair {
        numeral: "ω",
        value: 800,
    },
    GreekPair {
        numeral: "ϡ",
        value: 900,
    },
];

const GREEK_NUMERAL_LIST_CAPITAL: [GreekPair; 27] = [
    GreekPair {
        numeral: "Α",
        value: 1,
    },
    GreekPair {
        numeral: "Β",
        value: 2,
    },
    GreekPair {
        numeral: "Γ",
        value: 3,
    },
    GreekPair {
        numeral: "Δ",
        value: 4,
    },
    GreekPair {
        numeral: "Ε",
        value: 5,
    },
    GreekPair {
        numeral: "Ϝ",
        value: 6,
    },
    GreekPair {
        numeral: "Ζ",
        value: 7,
    },
    GreekPair {
        numeral: "Η",
        value: 8,
    },
    GreekPair {
        numeral: "Θ",
        value: 9,
    },
    GreekPair {
        numeral: "Ι",
        value: 10,
    },
    GreekPair {
        numeral: "Κ",
        value: 20,
    },
    GreekPair {
        numeral: "Λ",
        value: 30,
    },
    GreekPair {
        numeral: "Μ",
        value: 40,
    },
    GreekPair {
        numeral: "Ν",
        value: 50,
    },
    GreekPair {
        numeral: "Ξ",
        value: 60,
    },
    GreekPair {
        numeral: "Ο",
        value: 70,
    },
    GreekPair {
        numeral: "Π",
        value: 80,
    },
    GreekPair {
        numeral: "Ϙ",
        value: 90,
    },
    GreekPair {
        numeral: "Ρ",
        value: 100,
    },
    GreekPair {
        numeral: "Σ",
        value: 200,
    },
    GreekPair {
        numeral: "Τ",
        value: 300,
    },
    GreekPair {
        numeral: "Υ",
        value: 400,
    },
    GreekPair {
        numeral: "Φ",
        value: 500,
    },
    GreekPair {
        numeral: "Χ",
        value: 600,
    },
    GreekPair {
        numeral: "Ψ",
        value: 700,
    },
    GreekPair {
        numeral: "Ω",
        value: 800,
    },
    GreekPair {
        numeral: "Ϡ",
        value: 900,
    },
];

fn greek_table(capital: bool) -> &'static [GreekPair] {
    if capital {
        &GREEK_NUMERAL_LIST_CAPITAL
    } else {
        &GREEK_NUMERAL_LIST
    }
}

fn digit_count(number: &BigInt) -> usize {
    number.to_str_radix(10).len()
}

fn greek_char_value(ch: char, capital: bool) -> Option<i64> {
    greek_table(capital)
        .iter()
        .find(|pair| pair.numeral.starts_with(ch))
        .map(|pair| pair.value)
}

fn thousand_pow(power: usize) -> PyResult<BigInt> {
    let power = u32::try_from(power)
        .map_err(|_| PyOverflowError::new_err("Exponent is too large for conversion"))?;
    Ok(BigInt::from(1000).pow(power))
}

/// Converts an Arabic integer or finite float to a Greek numeral.
///
/// Set `positional` to use `~`-separated groups, or leave it false for classic underscore
/// notation. `capital` selects uppercase Greek numerals. Fractional digits are converted one
/// by one and retain zero placeholders.
///
/// # Python example
///
/// ```python
/// >>> arabic_to_greek(1.05, positional=False, capital=False)
/// 'α.(0:ε)'
/// ```
#[pyfunction]
pub fn arabic_to_greek(
    number: &Bound<'_, PyAny>,
    positional: bool,
    capital: bool,
) -> PyResult<String> {
    match extract_arabic_input(number)? {
        ArabicInput::Integer(number) => arabic_to_greek_integer(number, positional, capital),
        ArabicInput::Float {
            whole,
            fraction,
            negative,
        } => {
            let mut numeral = arabic_to_greek_integer(whole, positional, capital)?;
            if !fraction.is_empty() {
                let encoded = encode_fractional_digits(&fraction, |digit| {
                    arabic_to_greek_integer(BigInt::from(digit), positional, capital)
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

fn arabic_to_greek_integer(number: BigInt, positional: bool, capital: bool) -> PyResult<String> {
    if positional {
        return arabic_to_position_greek(number, capital);
    }
    arabic_to_classic_greek(number, capital)
}

fn arabic_to_classic_greek(number: BigInt, capital: bool) -> PyResult<String> {
    if number <= BigInt::from(0) {
        return Ok(String::new());
    }
    let table = greek_table(capital);
    let mut input = number;
    let mut out = String::new();

    while input > BigInt::from(0) {
        for pair in table.iter().rev() {
            let mut value = BigInt::from(pair.value);
            let mut power_value: usize = 0;
            let mut has_power = false;

            let digits = digit_count(&input);
            if digits > 3 {
                power_value = (digits - 1) / 3;
                value *= thousand_pow(power_value)?;
                has_power = true;
            }

            if input >= value {
                input %= &value;
                out.push_str(pair.numeral);
                for _ in 0..power_value {
                    out.push('_');
                }
                if has_power {
                    break;
                }
            }
        }
    }

    Ok(out)
}

fn arabic_to_position_greek(number: BigInt, capital: bool) -> PyResult<String> {
    if number <= BigInt::from(0) {
        return Ok(String::new());
    }

    let table = greek_table(capital);
    let mut remains: Vec<BigInt> = Vec::new();
    let mut input = number;
    let mut out = String::new();
    let thousand = BigInt::from(1000);

    while input > BigInt::from(0) {
        remains.push(&input % &thousand);
        input /= &thousand;
    }

    for mut item in remains.into_iter().rev() {
        if !out.is_empty() {
            out.push('~');
        }
        for pair in table.iter().rev() {
            let value = BigInt::from(pair.value);
            if item >= value {
                out.push_str(pair.numeral);
                item %= value;
            }
        }
    }

    Ok(out)
}

/// Converts a Greek numeral in classic or positional form to an Arabic integer or float.
///
/// The `positional` and `capital` flags must match those used for the original conversion.
///
/// # Python example
///
/// ```python
/// >>> greek_to_arabic('α.(0:ε)', positional=False, capital=False)
/// 1.05
/// ```
#[pyfunction]
pub fn greek_to_arabic<'py>(
    py: Python<'py>,
    numeral: &str,
    positional: bool,
    capital: bool,
) -> PyResult<Bound<'py, PyAny>> {
    let (negative, numeral) = match numeral.strip_prefix('-') {
        Some(numeral) => (true, numeral),
        None => (false, numeral),
    };
    if let Some((integer_numeral, fraction)) = fractional_numeral_parts(numeral)? {
        let whole = greek_to_arabic_integer(integer_numeral, positional, capital)?;
        let fraction_digits = decode_fractional_digits(fraction, |digit| {
            greek_to_arabic_integer(digit, positional, capital)
        })?;
        let value = decimal_float_value(&whole, &fraction_digits, negative)?;
        return Ok(PyFloat::new(py, value).into_any());
    }

    let mut total = greek_to_arabic_integer(numeral, positional, capital)?;
    if negative {
        total = -total;
    }
    Ok(total.into_pyobject(py)?.into_any())
}

fn greek_to_arabic_integer(numeral: &str, positional: bool, capital: bool) -> PyResult<BigInt> {
    if positional {
        return position_greek_to_arabic(numeral, capital);
    }
    classic_greek_to_arabic(numeral, capital)
}

fn classic_greek_to_arabic(numeral: &str, capital: bool) -> PyResult<BigInt> {
    let mut number = BigInt::from(0);
    let mut power_num: usize = 0;
    let mut last_number = BigInt::from(0);

    for ch in numeral.chars() {
        if ch == '_' {
            power_num += 1;
            continue;
        }
        let Some(value) = greek_char_value(ch, capital) else {
            return Err(PyValueError::new_err(format!("Invalid symbol: {ch}")));
        };

        last_number *= thousand_pow(power_num)?;
        number += &last_number;
        last_number = BigInt::from(value);
        power_num = 0;
    }

    if power_num > 0 {
        last_number *= thousand_pow(power_num)?;
    }

    number += last_number;
    Ok(number)
}

fn position_greek_to_arabic(numeral: &str, capital: bool) -> PyResult<BigInt> {
    let mut number = BigInt::from(0);

    for (index, part) in numeral.split('~').rev().enumerate() {
        let pow = thousand_pow(index)?;
        for ch in part.chars() {
            let Some(value) = greek_char_value(ch, capital) else {
                return Err(PyValueError::new_err(format!("Invalid symbol: {ch}")));
            };
            number += BigInt::from(value) * &pow;
        }
    }

    Ok(number)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn classic_and_positional_forms_round_trip() {
        for (number, positional, capital, expected) in [
            (123, false, false, "ρκγ"),
            (1234, false, false, "α_σλδ"),
            (1234, true, false, "α~σλδ"),
            (1234, true, true, "Α~ΣΛΔ"),
        ] {
            let number = BigInt::from(number);
            let numeral = arabic_to_greek_integer(number.clone(), positional, capital).unwrap();
            assert_eq!(numeral, expected);
            assert_eq!(
                greek_to_arabic_integer(&numeral, positional, capital).unwrap(),
                number
            );
        }
    }

    #[test]
    fn fractional_digit_tokens_preserve_zeroes_and_case() {
        let lowercase = encode_fractional_digits("105", |digit| {
            arabic_to_greek_integer(BigInt::from(digit), false, false)
        })
        .unwrap();
        assert_eq!(lowercase, "α:0:ε");
        assert_eq!(
            decode_fractional_digits(&lowercase, |digit| {
                greek_to_arabic_integer(digit, false, false)
            })
            .unwrap(),
            "105"
        );

        let uppercase = encode_fractional_digits("105", |digit| {
            arabic_to_greek_integer(BigInt::from(digit), true, true)
        })
        .unwrap();
        assert_eq!(uppercase, "Α:0:Ε");
        assert_eq!(
            decode_fractional_digits(&uppercase, |digit| {
                greek_to_arabic_integer(digit, true, true)
            })
            .unwrap(),
            "105"
        );
    }

    #[test]
    fn invalid_case_and_symbols_are_rejected() {
        assert!(greek_to_arabic_integer("Α", false, false).is_err());
        assert!(greek_to_arabic_integer("xyz", false, false).is_err());
    }
}
