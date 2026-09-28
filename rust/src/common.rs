use greekromannumerical_core::{ArabicNumber, ConversionError};
use num_bigint::BigInt;
use pyo3::exceptions::{PyOverflowError, PyTypeError, PyValueError};
use pyo3::prelude::*;
use pyo3::types::{PyBytes, PyDict, PyFloat, PyInt, PyModule};

pub(crate) fn extract_arabic_number(number: &Bound<'_, PyAny>) -> PyResult<ArabicNumber> {
    if number.is_instance_of::<PyFloat>() {
        let value = number.extract::<f64>()?;
        if !value.is_finite() {
            return Err(PyValueError::new_err("Float values must be finite"));
        }
        return Ok(ArabicNumber::Float(value));
    }

    let py = number.py();
    let index = PyModule::import(py, "operator")?.getattr("index")?;
    let integer = index.call1((number,)).map_err(|error| {
        if error.is_instance_of::<PyTypeError>(py) {
            PyTypeError::new_err("number must be an integer or float")
        } else {
            error
        }
    })?;
    let bit_length = integer.call_method0("bit_length")?.extract::<usize>()?;
    let byte_length = bit_length
        .checked_add(8)
        .ok_or_else(|| PyOverflowError::new_err("Python integer is too large"))?
        / 8;
    let kwargs = PyDict::new(py);
    kwargs.set_item("signed", true)?;
    let bytes = integer.call_method("to_bytes", (byte_length, "big"), Some(&kwargs))?;
    let bytes = bytes.extract::<Vec<u8>>()?;
    Ok(ArabicNumber::Integer(BigInt::from_signed_bytes_be(&bytes)))
}

pub(crate) fn arabic_number_to_python<'py>(
    py: Python<'py>,
    number: ArabicNumber,
) -> PyResult<Bound<'py, PyAny>> {
    match number {
        ArabicNumber::Integer(number) => {
            let bytes = number.to_signed_bytes_be();
            let bytes = PyBytes::new_with(py, bytes.len(), |buffer| {
                buffer.copy_from_slice(&bytes);
                Ok(())
            })?;
            let kwargs = PyDict::new(py);
            kwargs.set_item("signed", true)?;
            Ok(py
                .get_type::<PyInt>()
                .call_method("from_bytes", (bytes, "big"), Some(&kwargs))?
                .into_any())
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
