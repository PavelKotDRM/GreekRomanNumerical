use pyo3::exceptions::{PyOverflowError, PyValueError};
use pyo3::prelude::*;
use std::collections::HashMap;

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

fn checked_mul_i64(a: i64, b: i64) -> PyResult<i64> {
    a.checked_mul(b)
        .ok_or_else(|| PyOverflowError::new_err("Integer overflow during conversion"))
}

fn thousand_pow(power: usize) -> PyResult<i64> {
    let mut out: i64 = 1;
    for _ in 0..power {
        out = checked_mul_i64(out, 1000)?;
    }
    Ok(out)
}

#[pyfunction]
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
fn roman_to_arabic(numeral: &str) -> PyResult<i64> {
    let map: HashMap<&str, i64> = ROMAN_NUMERAL_LIST.into_iter().collect();
    let chars: Vec<char> = numeral.chars().collect();
    let mut index: usize = 0;
    let mut total: i64 = 0;

    while index < chars.len() {
        if index + 1 < chars.len() {
            let two = format!("{}{}", chars[index], chars[index + 1]);
            if let Some(value) = map.get(two.as_str()) {
                total += *value;
                index += 2;
                continue;
            }
        }

        let one = chars[index].to_string();
        if let Some(value) = map.get(one.as_str()) {
            total += *value;
            index += 1;
            continue;
        }

        return Err(PyValueError::new_err(format!("Invalid name: {numeral}")));
    }

    Ok(total)
}

#[pyfunction]
fn arabic_to_greek(number: i64, positional: bool, capital: bool) -> PyResult<String> {
    if positional {
        return arabic_to_position_greek(number, capital);
    }
    arabic_to_classic_greek(number, capital)
}

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

            let digits = input.to_string().len();
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

fn arabic_to_position_greek(number: i64, capital: bool) -> PyResult<String> {
    if number <= 0 {
        return Ok(String::new());
    }

    let table = greek_table(capital);
    let reverse: Vec<(i64, &str)> = table.iter().map(|p| (p.value, p.numeral)).collect();
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
        for (value, numeral) in reverse.iter().rev() {
            if item / value > 0 {
                out.push_str(numeral);
                item %= value;
            }
        }
    }

    Ok(out)
}

#[pyfunction]
fn greek_to_arabic(numeral: &str, positional: bool, capital: bool) -> PyResult<i64> {
    if positional {
        return position_greek_to_arabic(numeral, capital);
    }
    classic_greek_to_arabic(numeral, capital)
}

fn classic_greek_to_arabic(numeral: &str, capital: bool) -> PyResult<i64> {
    let table = greek_table(capital);
    let map: HashMap<&str, i64> = table.iter().map(|p| (p.numeral, p.value)).collect();

    let mut number: i64 = 0;
    let mut power_num: usize = 0;
    let mut last_number: i64 = 0;

    for ch in numeral.chars() {
        if ch == '_' {
            power_num += 1;
            continue;
        }
        let token = ch.to_string();
        let Some(value) = map.get(token.as_str()) else {
            return Err(PyValueError::new_err(format!("Invalid symbol: {ch}")));
        };

        last_number = checked_mul_i64(last_number, thousand_pow(power_num)?)?;
        number += last_number;
        last_number = *value;
        power_num = 0;
    }

    if power_num > 0 {
        last_number = checked_mul_i64(last_number, thousand_pow(power_num)?)?;
    }

    number += last_number;
    Ok(number)
}

fn position_greek_to_arabic(numeral: &str, capital: bool) -> PyResult<i64> {
    let table = greek_table(capital);
    let map: HashMap<&str, i64> = table.iter().map(|p| (p.numeral, p.value)).collect();
    let mut number: i64 = 0;

    for (index, part) in numeral.split('~').rev().enumerate() {
        let pow = thousand_pow(index)?;
        for ch in part.chars() {
            let token = ch.to_string();
            let Some(value) = map.get(token.as_str()) else {
                return Err(PyValueError::new_err(format!("Invalid symbol: {ch}")));
            };
            let scaled = checked_mul_i64(*value, pow)?;
            number += scaled;
        }
    }

    Ok(number)
}

#[pymodule]
fn _native(_py: Python<'_>, module: &Bound<'_, PyModule>) -> PyResult<()> {
    module.add_function(wrap_pyfunction!(arabic_to_roman, module)?)?;
    module.add_function(wrap_pyfunction!(roman_to_arabic, module)?)?;
    module.add_function(wrap_pyfunction!(arabic_to_greek, module)?)?;
    module.add_function(wrap_pyfunction!(greek_to_arabic, module)?)?;
    Ok(())
}
