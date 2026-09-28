//! Shared numeric parsing and fractional-digit handling for both converters.

use num_bigint::BigInt;
use num_traits::ToPrimitive;
use pyo3::exceptions::{PyOverflowError, PyTypeError, PyValueError};
use pyo3::prelude::*;
use pyo3::types::PyFloat;

pub(crate) enum ArabicInput {
    Integer(BigInt),
    Float {
        whole: BigInt,
        fraction: String,
        negative: bool,
    },
}

/// Expands Python's shortest float representation into decimal integer and fractional parts.
pub(crate) fn float_decimal_parts(value: &str) -> PyResult<(BigInt, String, bool)> {
    let (negative, value) = match value.strip_prefix('-') {
        Some(value) => (true, value),
        None => (false, value),
    };
    let (mantissa, exponent) = match value.find(['e', 'E']) {
        Some(index) => {
            let exponent = value[index + 1..]
                .parse::<i64>()
                .map_err(|_| PyValueError::new_err("Invalid float representation"))?;
            (&value[..index], exponent)
        }
        None => (value, 0),
    };
    let decimal_index = mantissa.find('.').unwrap_or(mantissa.len());
    let mut digits = mantissa.replace('.', "");
    if digits.is_empty() || !digits.bytes().all(|digit| digit.is_ascii_digit()) {
        return Err(PyValueError::new_err("Invalid float representation"));
    }

    let decimal_index = decimal_index as i64 + exponent;
    let (whole_digits, fraction_digits) = if decimal_index <= 0 {
        let leading_zeroes = usize::try_from(-decimal_index)
            .map_err(|_| PyOverflowError::new_err("Float representation is too large"))?;
        (
            "0".to_owned(),
            format!("{}{}", "0".repeat(leading_zeroes), digits),
        )
    } else if decimal_index as usize >= digits.len() {
        let trailing_zeroes = decimal_index as usize - digits.len();
        digits.push_str(&"0".repeat(trailing_zeroes));
        (digits, String::new())
    } else {
        let fraction = digits.split_off(decimal_index as usize);
        (digits, fraction)
    };

    let whole_digits = whole_digits.trim_start_matches('0');
    let whole = if whole_digits.is_empty() {
        BigInt::from(0)
    } else {
        BigInt::parse_bytes(whole_digits.as_bytes(), 10)
            .ok_or_else(|| PyValueError::new_err("Invalid float representation"))?
    };
    let fraction = fraction_digits.trim_end_matches('0').to_owned();
    Ok((whole, fraction, negative))
}

pub(crate) fn extract_arabic_input(number: &Bound<'_, PyAny>) -> PyResult<ArabicInput> {
    if number.is_instance_of::<PyFloat>() {
        let value = number.extract::<f64>()?;
        if !value.is_finite() {
            return Err(PyValueError::new_err("Float values must be finite"));
        }
        let representation = number.str()?;
        let (whole, fraction, negative) = float_decimal_parts(representation.to_str()?)?;
        return Ok(ArabicInput::Float {
            whole,
            fraction,
            negative,
        });
    }

    number
        .extract::<BigInt>()
        .map(ArabicInput::Integer)
        .map_err(|_| PyTypeError::new_err("number must be an integer or float"))
}

pub(crate) fn encode_fractional_digits<F>(fraction: &str, mut convert_digit: F) -> PyResult<String>
where
    F: FnMut(u32) -> PyResult<String>,
{
    let mut encoded = String::new();
    for (index, digit) in fraction.chars().enumerate() {
        if index > 0 {
            encoded.push(':');
        }
        let value = digit
            .to_digit(10)
            .ok_or_else(|| PyValueError::new_err("Invalid decimal digit"))?;
        if value == 0 {
            encoded.push('0');
        } else {
            encoded.push_str(&convert_digit(value)?);
        }
    }
    Ok(encoded)
}

pub(crate) fn fractional_numeral_parts(numeral: &str) -> PyResult<Option<(&str, &str)>> {
    let Some(index) = numeral.find(".(") else {
        if numeral.contains('.') {
            return Err(PyValueError::new_err(format!(
                "Invalid decimal numeral: {numeral}"
            )));
        }
        return Ok(None);
    };
    let integer_numeral = &numeral[..index];
    let encoded_fraction = &numeral[index + 2..];
    let Some(fraction) = encoded_fraction.strip_suffix(')') else {
        return Err(PyValueError::new_err(format!(
            "Invalid decimal numeral: {numeral}"
        )));
    };
    if fraction.is_empty()
        || fraction.contains(['(', ')'])
        || fraction.split(':').any(|token| token.is_empty())
    {
        return Err(PyValueError::new_err(format!(
            "Invalid decimal numeral: {numeral}"
        )));
    }
    Ok(Some((integer_numeral, fraction)))
}

pub(crate) fn decode_fractional_digits<F>(fraction: &str, mut convert_digit: F) -> PyResult<String>
where
    F: FnMut(&str) -> PyResult<BigInt>,
{
    let mut digits = String::new();
    for token in fraction.split(':') {
        if token == "0" {
            digits.push('0');
            continue;
        }
        let value = convert_digit(token)?;
        let Some(value) = value.to_u32().filter(|digit| (1..=9).contains(digit)) else {
            return Err(PyValueError::new_err(
                "Fractional numeral tokens must represent digits from 1 to 9",
            ));
        };
        digits.push(char::from_digit(value, 10).expect("validated decimal digit"));
    }
    Ok(digits)
}

pub(crate) fn decimal_float_value(
    integer: &BigInt,
    fraction: &str,
    negative: bool,
) -> PyResult<f64> {
    let value = format!("{integer}.{fraction}")
        .parse::<f64>()
        .map_err(|_| {
            PyValueError::new_err("Decimal numeral is outside the supported float range")
        })?;
    if !value.is_finite() {
        return Err(PyValueError::new_err(
            "Decimal numeral is outside the supported float range",
        ));
    }
    Ok(if negative { -value } else { value })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn float_parts_preserve_decimal_zeroes_and_exponents() {
        assert_eq!(
            float_decimal_parts("1.05").unwrap(),
            (BigInt::from(1), "05".to_owned(), false)
        );
        assert_eq!(
            float_decimal_parts("-1e-7").unwrap(),
            (BigInt::from(0), "0000001".to_owned(), true)
        );
        assert_eq!(
            float_decimal_parts("2.0").unwrap(),
            (BigInt::from(2), String::new(), false)
        );
    }

    #[test]
    fn fractional_tokens_round_trip_with_zero_placeholders() {
        let encoded = encode_fractional_digits("105", |digit| Ok(digit.to_string())).unwrap();
        assert_eq!(encoded, "1:0:5");

        let decoded = decode_fractional_digits(&encoded, |token| {
            token
                .parse::<u32>()
                .map(BigInt::from)
                .map_err(|_| PyValueError::new_err("invalid test digit"))
        })
        .unwrap();
        assert_eq!(decoded, "105");
    }

    #[test]
    fn fractional_syntax_rejects_missing_or_empty_tokens() {
        assert_eq!(
            fractional_numeral_parts("I.(II:V)").unwrap(),
            Some(("I", "II:V"))
        );
        assert!(fractional_numeral_parts("I.25").is_err());
        assert!(fractional_numeral_parts("I.(II:)").is_err());
    }
}
