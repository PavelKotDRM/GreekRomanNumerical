use crate::common::{arabic_number_to_python, extract_arabic_number, map_conversion_error};
use crate::greek::greek_options;
use greekromannumerical_core::historical_fractions as core_historical_fractions;
use pyo3::prelude::*;
use pyo3::types::PyModule;

#[pyfunction]
pub fn historical_arabic_to_roman(number: &Bound<'_, PyAny>) -> PyResult<String> {
    let number = extract_arabic_number(number)?;
    core_historical_fractions::arabic_to_roman(&number).map_err(map_conversion_error)
}

#[pyfunction]
pub fn historical_roman_to_arabic<'py>(
    py: Python<'py>,
    numeral: &str,
) -> PyResult<Bound<'py, PyAny>> {
    let number =
        core_historical_fractions::roman_to_arabic(numeral).map_err(map_conversion_error)?;
    arabic_number_to_python(py, number)
}

#[pyfunction]
pub fn historical_arabic_to_greek(
    number: &Bound<'_, PyAny>,
    positional: bool,
    capital: bool,
) -> PyResult<String> {
    let number = extract_arabic_number(number)?;
    core_historical_fractions::arabic_to_greek(&number, greek_options(positional, capital))
        .map_err(map_conversion_error)
}

#[pyfunction]
pub fn historical_greek_to_arabic<'py>(
    py: Python<'py>,
    numeral: &str,
    positional: bool,
    capital: bool,
) -> PyResult<Bound<'py, PyAny>> {
    let number =
        core_historical_fractions::greek_to_arabic(numeral, greek_options(positional, capital))
            .map_err(map_conversion_error)?;
    arabic_number_to_python(py, number)
}

#[pyfunction]
pub fn historical_arabic_to_roman_latex(number: &Bound<'_, PyAny>) -> PyResult<String> {
    let number = extract_arabic_number(number)?;
    core_historical_fractions::arabic_to_roman_latex(&number).map_err(map_conversion_error)
}

#[pyfunction]
pub fn historical_arabic_to_roman_mathml(number: &Bound<'_, PyAny>) -> PyResult<String> {
    let number = extract_arabic_number(number)?;
    core_historical_fractions::arabic_to_roman_mathml(&number).map_err(map_conversion_error)
}

#[pyfunction]
pub fn historical_arabic_to_greek_latex(
    number: &Bound<'_, PyAny>,
    positional: bool,
    capital: bool,
) -> PyResult<String> {
    let number = extract_arabic_number(number)?;
    core_historical_fractions::arabic_to_greek_latex(&number, greek_options(positional, capital))
        .map_err(map_conversion_error)
}

#[pyfunction]
pub fn historical_arabic_to_greek_mathml(
    number: &Bound<'_, PyAny>,
    positional: bool,
    capital: bool,
) -> PyResult<String> {
    let number = extract_arabic_number(number)?;
    core_historical_fractions::arabic_to_greek_mathml(&number, greek_options(positional, capital))
        .map_err(map_conversion_error)
}

pub(crate) fn register(module: &Bound<'_, PyModule>) -> PyResult<()> {
    module.add_function(wrap_pyfunction!(historical_arabic_to_roman, module)?)?;
    module.add_function(wrap_pyfunction!(historical_roman_to_arabic, module)?)?;
    module.add_function(wrap_pyfunction!(historical_arabic_to_greek, module)?)?;
    module.add_function(wrap_pyfunction!(historical_greek_to_arabic, module)?)?;
    module.add_function(wrap_pyfunction!(historical_arabic_to_roman_latex, module)?)?;
    module.add_function(wrap_pyfunction!(historical_arabic_to_roman_mathml, module)?)?;
    module.add_function(wrap_pyfunction!(historical_arabic_to_greek_latex, module)?)?;
    module.add_function(wrap_pyfunction!(historical_arabic_to_greek_mathml, module)?)?;
    Ok(())
}
