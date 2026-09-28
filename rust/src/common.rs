use core_bigint::BigInt as CoreBigInt;
use greekromannumerical_core::{ArabicNumber, ConversionError};
use num_bigint::BigInt;
use pyo3::exceptions::{PyOverflowError, PyTypeError, PyValueError};
use pyo3::prelude::*;
use pyo3::types::PyFloat;

pub(crate) fn extract_arabic_number(number: &Bound<'_, PyAny>) -> PyResult<ArabicNumber> {
    if number.is_instance_of::<PyFloat>() {
        let value = number.extract::<f64>()?;
        if !value.is_finite() {
            return Err(PyValueError::new_err("Float values must be finite"));
        }
        return Ok(ArabicNumber::Float(value));
    }

    let number = number
        .extract::<BigInt>()
        .map_err(|_| PyTypeError::new_err("number must be an integer or float"))?;
    let digits = number.to_str_radix(10);
    let number = CoreBigInt::parse_bytes(digits.as_bytes(), 10)
        .ok_or_else(|| PyValueError::new_err("Failed to convert Python integer"))?;
    Ok(ArabicNumber::Integer(number))
}

pub(crate) fn arabic_number_to_python<'py>(
    py: Python<'py>,
    number: ArabicNumber,
) -> PyResult<Bound<'py, PyAny>> {
    match number {
        ArabicNumber::Integer(number) => {
            let digits = number.to_str_radix(10);
            let number = BigInt::parse_bytes(digits.as_bytes(), 10)
                .ok_or_else(|| PyValueError::new_err("Failed to convert core integer"))?;
            Ok(number.into_pyobject(py)?.into_any())
        }
        ArabicNumber::Float(number) => Ok(PyFloat::new(py, number).into_any()),
    }
}

pub(crate) fn map_conversion_error(error: ConversionError) -> PyErr {
    let message = error.to_string();
    match error {
        ConversionError::OutputLimitExceeded | ConversionError::ResourceLimitExceeded => {
            PyOverflowError::new_err(message)
        }
        _ => PyValueError::new_err(message),
    }
}
