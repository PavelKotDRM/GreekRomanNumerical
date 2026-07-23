use pyo3::exceptions::{PyOverflowError, PyValueError};
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
    GreekPair { numeral: "α", value: 1 },
    GreekPair { numeral: "β", value: 2 },
    GreekPair { numeral: "γ", value: 3 },
    GreekPair { numeral: "δ", value: 4 },
    GreekPair { numeral: "ε", value: 5 },
    GreekPair { numeral: "ϝ", value: 6 },
    GreekPair { numeral: "ζ", value: 7 },
    GreekPair { numeral: "η", value: 8 },
    GreekPair { numeral: "θ", value: 9 },
    GreekPair { numeral: "ι", value: 10 },
    GreekPair { numeral: "κ", value: 20 },
    GreekPair { numeral: "λ", value: 30 },
    GreekPair { numeral: "μ", value: 40 },
    GreekPair { numeral: "ν", value: 50 },
    GreekPair { numeral: "ξ", value: 60 },
    GreekPair { numeral: "ο", value: 70 },
    GreekPair { numeral: "π", value: 80 },
    GreekPair { numeral: "ϙ", value: 90 },
    GreekPair { numeral: "ρ", value: 100 },
    GreekPair { numeral: "σ", value: 200 },
    GreekPair { numeral: "τ", value: 300 },
    GreekPair { numeral: "υ", value: 400 },
    GreekPair { numeral: "φ", value: 500 },
    GreekPair { numeral: "χ", value: 600 },
    GreekPair { numeral: "ψ", value: 700 },
    GreekPair { numeral: "ω", value: 800 },
    GreekPair { numeral: "ϡ", value: 900 },
];

const GREEK_NUMERAL_LIST_CAPITAL: [GreekPair; 27] = [
    GreekPair { numeral: "Α", value: 1 },
    GreekPair { numeral: "Β", value: 2 },
    GreekPair { numeral: "Γ", value: 3 },
    GreekPair { numeral: "Δ", value: 4 },
    GreekPair { numeral: "Ε", value: 5 },
    GreekPair { numeral: "Ϝ", value: 6 },
    GreekPair { numeral: "Ζ", value: 7 },
    GreekPair { numeral: "Η", value: 8 },
    GreekPair { numeral: "Θ", value: 9 },
    GreekPair { numeral: "Ι", value: 10 },
    GreekPair { numeral: "Κ", value: 20 },
    GreekPair { numeral: "Λ", value: 30 },
    GreekPair { numeral: "Μ", value: 40 },
    GreekPair { numeral: "Ν", value: 50 },
    GreekPair { numeral: "Ξ", value: 60 },
    GreekPair { numeral: "Ο", value: 70 },
    GreekPair { numeral: "Π", value: 80 },
    GreekPair { numeral: "Ϙ", value: 90 },
    GreekPair { numeral: "Ρ", value: 100 },
    GreekPair { numeral: "Σ", value: 200 },
    GreekPair { numeral: "Τ", value: 300 },
    GreekPair { numeral: "Υ", value: 400 },
    GreekPair { numeral: "Φ", value: 500 },
    GreekPair { numeral: "Χ", value: 600 },
    GreekPair { numeral: "Ψ", value: 700 },
    GreekPair { numeral: "Ω", value: 800 },
    GreekPair { numeral: "Ϡ", value: 900 },
];

fn greek_table(capital: bool) -> &'static [GreekPair] {
    if capital {
        &GREEK_NUMERAL_LIST_CAPITAL
    } else {
        &GREEK_NUMERAL_LIST
    }
}

/// Returns the number of decimal digits for a positive integer.
fn digit_count_i64(mut n: i64) -> usize {
    let mut digits = 1;
    while n >= 10 {
        n /= 10;
        digits += 1;
    }
    digits
}

/// Maps a Greek numeral character to its numeric value for selected case mode.
fn greek_char_value(ch: char, capital: bool) -> Option<i64> {
    if capital {
        match ch {
            'Α' => Some(1),
            'Β' => Some(2),
            'Γ' => Some(3),
            'Δ' => Some(4),
            'Ε' => Some(5),
            'Ϝ' => Some(6),
            'Ζ' => Some(7),
            'Η' => Some(8),
            'Θ' => Some(9),
            'Ι' => Some(10),
            'Κ' => Some(20),
            'Λ' => Some(30),
            'Μ' => Some(40),
            'Ν' => Some(50),
            'Ξ' => Some(60),
            'Ο' => Some(70),
            'Π' => Some(80),
            'Ϙ' => Some(90),
            'Ρ' => Some(100),
            'Σ' => Some(200),
            'Τ' => Some(300),
            'Υ' => Some(400),
            'Φ' => Some(500),
            'Χ' => Some(600),
            'Ψ' => Some(700),
            'Ω' => Some(800),
            'Ϡ' => Some(900),
            _ => None,
        }
    } else {
        match ch {
            'α' => Some(1),
            'β' => Some(2),
            'γ' => Some(3),
            'δ' => Some(4),
            'ε' => Some(5),
            'ϝ' => Some(6),
            'ζ' => Some(7),
            'η' => Some(8),
            'θ' => Some(9),
            'ι' => Some(10),
            'κ' => Some(20),
            'λ' => Some(30),
            'μ' => Some(40),
            'ν' => Some(50),
            'ξ' => Some(60),
            'ο' => Some(70),
            'π' => Some(80),
            'ϙ' => Some(90),
            'ρ' => Some(100),
            'σ' => Some(200),
            'τ' => Some(300),
            'υ' => Some(400),
            'φ' => Some(500),
            'χ' => Some(600),
            'ψ' => Some(700),
            'ω' => Some(800),
            'ϡ' => Some(900),
            _ => None,
        }
    }
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

/// Performs checked multiplication used by conversion routines.
fn checked_mul_i64(a: i64, b: i64) -> PyResult<i64> {
    a.checked_mul(b)
        .ok_or_else(|| PyOverflowError::new_err("Integer overflow during conversion"))
}

/// Computes 1000^power with overflow checking.
fn thousand_pow(power: usize) -> PyResult<i64> {
    let mut out: i64 = 1;
    for _ in 0..power {
        out = checked_mul_i64(out, 1000)?;
    }
    Ok(out)
}

#[pyfunction]
/// Converts Arabic integer to Roman numeral representation.
fn arabic_to_roman(number: i64) -> PyResult<String> {
    if number <= 0 {
        return Ok(String::new());
    }
    let mut input = number;
    let mut out = String::new();
    for (numeral, value) in ROMAN_NUMERAL_LIST {
        if input / value > 0 {
            let count = input / value;
            input -= count * value;
            for _ in 0..count {
                out.push_str(numeral);
            }
        }
    }
    Ok(out)
}

#[pyfunction]
/// Converts Roman numeral representation back to Arabic integer.
fn roman_to_arabic(numeral: &str) -> PyResult<i64> {
    let bytes = numeral.as_bytes();
    let mut index = 0usize;
    let mut total: i64 = 0;

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
fn arabic_to_greek(number: i64, positional: bool, capital: bool) -> PyResult<String> {
    if positional {
        return arabic_to_position_greek(number, capital);
    }
    arabic_to_classic_greek(number, capital)
}

/// Converts Arabic integer to classic Greek numeral format.
fn arabic_to_classic_greek(number: i64, capital: bool) -> PyResult<String> {
    if number <= 0 {
        return Ok(String::new());
    }
    let table = greek_table(capital);
    let mut input = number;
    let mut out = String::new();

    while input > 0 {
        for pair in table.iter().rev() {
            let mut value = pair.value;
            let mut power_value: usize = 0;
            let mut has_power = false;

            let digits = digit_count_i64(input);
            if digits > 3 {
                power_value = (digits - 1) / 3;
                value = checked_mul_i64(value, thousand_pow(power_value)?)?;
                has_power = true;
            }

            if input / value > 0 {
                input %= value;
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
fn arabic_to_position_greek(number: i64, capital: bool) -> PyResult<String> {
    if number <= 0 {
        return Ok(String::new());
    }

    let table = greek_table(capital);
    let mut remains: Vec<i64> = Vec::new();
    let mut input = number;
    let mut out = String::new();

    while input > 0 {
        remains.push(input % 1000);
        input /= 1000;
    }

    for mut item in remains.into_iter().rev() {
        if !out.is_empty() {
            out.push('~');
        }
        for pair in table.iter().rev() {
            if item / pair.value > 0 {
                out.push_str(pair.numeral);
                item %= pair.value;
            }
        }
    }

    Ok(out)
}

#[pyfunction]
/// Converts Greek numeral in classic or positional form to Arabic integer.
fn greek_to_arabic(numeral: &str, positional: bool, capital: bool) -> PyResult<i64> {
    if positional {
        return position_greek_to_arabic(numeral, capital);
    }
    classic_greek_to_arabic(numeral, capital)
}

/// Converts classic Greek numeral format to Arabic integer.
fn classic_greek_to_arabic(numeral: &str, capital: bool) -> PyResult<i64> {
    let mut number: i64 = 0;
    let mut power_num: usize = 0;
    let mut last_number: i64 = 0;

    for ch in numeral.chars() {
        if ch == '_' {
            power_num += 1;
            continue;
        }
        let Some(value) = greek_char_value(ch, capital) else {
            return Err(PyValueError::new_err(format!("Invalid symbol: {ch}")));
        };

        last_number = checked_mul_i64(last_number, thousand_pow(power_num)?)?;
        number += last_number;
        last_number = value;
        power_num = 0;
    }

    if power_num > 0 {
        last_number = checked_mul_i64(last_number, thousand_pow(power_num)?)?;
    }

    number += last_number;
    Ok(number)
}

/// Converts positional Greek numeral format to Arabic integer.
fn position_greek_to_arabic(numeral: &str, capital: bool) -> PyResult<i64> {
    let mut number: i64 = 0;

    for (index, part) in numeral.split('~').rev().enumerate() {
        let pow = thousand_pow(index)?;
        for ch in part.chars() {
            let Some(value) = greek_char_value(ch, capital) else {
                return Err(PyValueError::new_err(format!("Invalid symbol: {ch}")));
            };
            let scaled = checked_mul_i64(value, pow)?;
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
