use crate::common::{
    arabic_number_to_python, extract_arabic_number, extract_arabic_numbers, map_conversion_error,
};
use greekromannumerical_core::{
    arabic_to_roman as core_arabic_to_roman,
    arabic_to_roman_parallel as core_arabic_to_roman_parallel,
    roman_to_arabic as core_roman_to_arabic,
};
use pyo3::{exceptions::PyRuntimeError, prelude::*};

/// Converts an Arabic integer or finite float to an extended Roman numeral.
///
/// # Python example
///
/// ```python
/// >>> arabic_to_roman(1.25)
/// 'I.(II:V)'
/// ```
#[pyfunction]
pub fn arabic_to_roman(number: &Bound<'_, PyAny>) -> PyResult<String> {
    let number = extract_arabic_number(number)?;
    core_arabic_to_roman(&number).map_err(map_conversion_error)
}

/// Converts an iterable of Arabic integers or finite floats to Roman numerals in parallel.
#[pyfunction]
pub fn arabic_to_roman_parallel(
    py: Python<'_>,
    numbers: &Bound<'_, PyAny>,
) -> PyResult<Vec<String>> {
    let numbers = extract_arabic_numbers(numbers)?;
    let results = py
        .detach(|| core_arabic_to_roman_parallel(&numbers))
        .map_err(|error| PyRuntimeError::new_err(error.to_string()))?;
    results
        .into_iter()
        .map(|result| result.map_err(map_conversion_error))
        .collect()
}

/// Converts an extended Roman numeral back to an Arabic integer or float.
///
/// # Python example
///
/// ```python
/// >>> roman_to_arabic('I.(_:V)')
/// 1.05
/// ```
#[pyfunction]
pub fn roman_to_arabic<'py>(py: Python<'py>, numeral: &str) -> PyResult<Bound<'py, PyAny>> {
    let number = core_roman_to_arabic(numeral).map_err(map_conversion_error)?;
    arabic_number_to_python(py, number)
}
