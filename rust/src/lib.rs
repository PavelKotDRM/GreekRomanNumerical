use num_bigint::BigInt;
use num_traits::ToPrimitive;
use pyo3::exceptions::{PyMemoryError, PyOverflowError, PyValueError};
use pyo3::prelude::*;

#[derive(Clone, Copy)]
struct GreekPair {
    numeral: &'static str,
    value: i64,
}

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

/// Returns the number of decimal digits for a positive integer.
fn digit_count(number: &BigInt) -> usize {
    number.to_str_radix(10).len()
}

/// Maps a Greek numeral character to its numeric value for selected case mode.
fn greek_char_value(ch: char, capital: bool) -> Option<i64> {
    greek_table(capital)
        .iter()
        .find(|pair| pair.numeral.chars().next() == Some(ch))
        .map(|pair| pair.value)
}

/// Parses a single Roman token and returns (value, bytes_consumed).
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
        if let Some(v) = value {
            return Some((v, 2));
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
    value.map(|v| (v, 1))
}

/// Computes 1000^power with checked exponent conversion.
fn thousand_pow(power: usize) -> PyResult<BigInt> {
    let power = u32::try_from(power)
        .map_err(|_| PyOverflowError::new_err("Exponent is too large for conversion"))?;
    Ok(BigInt::from(1000).pow(power))
}

#[pyfunction]
/// Converts Arabic integer to Roman numeral representation.
fn arabic_to_roman(number: BigInt) -> PyResult<String> {
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

#[pyfunction]
/// Converts Roman numeral representation back to Arabic integer.
fn roman_to_arabic(numeral: &str) -> PyResult<BigInt> {
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

#[pyfunction]
/// Converts Arabic integer to Greek numeral in classic or positional form.
fn arabic_to_greek(number: BigInt, positional: bool, capital: bool) -> PyResult<String> {
    if positional {
        return arabic_to_position_greek(number, capital);
    }
    arabic_to_classic_greek(number, capital)
}

/// Converts Arabic integer to classic Greek numeral format.
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

/// Converts Arabic integer to positional Greek numeral format (groups joined by '~').
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

#[pyfunction]
/// Converts Greek numeral in classic or positional form to Arabic integer.
fn greek_to_arabic(numeral: &str, positional: bool, capital: bool) -> PyResult<BigInt> {
    if positional {
        return position_greek_to_arabic(numeral, capital);
    }
    classic_greek_to_arabic(numeral, capital)
}

/// Converts classic Greek numeral format to Arabic integer.
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

/// Converts positional Greek numeral format to Arabic integer.
fn position_greek_to_arabic(numeral: &str, capital: bool) -> PyResult<BigInt> {
    let mut number = BigInt::from(0);

    for (index, part) in numeral.split('~').rev().enumerate() {
        let pow = thousand_pow(index)?;
        for ch in part.chars() {
            let Some(value) = greek_char_value(ch, capital) else {
                return Err(PyValueError::new_err(format!("Invalid symbol: {ch}")));
            };
            let scaled = BigInt::from(value) * &pow;
            number += scaled;
        }
    }

    Ok(number)
}

#[pymodule]
/// Python module entrypoint for native conversion routines.
fn _native(_py: Python<'_>, module: &Bound<'_, PyModule>) -> PyResult<()> {
    module.add_function(wrap_pyfunction!(arabic_to_roman, module)?)?;
    module.add_function(wrap_pyfunction!(roman_to_arabic, module)?)?;
    module.add_function(wrap_pyfunction!(arabic_to_greek, module)?)?;
    module.add_function(wrap_pyfunction!(greek_to_arabic, module)?)?;
    Ok(())
}
