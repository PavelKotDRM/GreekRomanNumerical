use crate::common::{arabic_number_to_python, extract_arabic_number, map_conversion_error};
use greekromannumerical_core::{
    arabic_to_roman as core_arabic_to_roman, roman_to_arabic as core_roman_to_arabic,
};
use pyo3::prelude::*;

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
