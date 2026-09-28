use crate::common::{arabic_number_to_python, extract_arabic_number, map_conversion_error};
use greekromannumerical_core::{
    GreekCase, GreekNotation, GreekOptions, arabic_to_greek as core_arabic_to_greek,
    greek_to_arabic as core_greek_to_arabic,
};
use pyo3::prelude::*;

pub(crate) fn greek_options(positional: bool, capital: bool) -> GreekOptions {
    GreekOptions {
        notation: if positional {
            GreekNotation::Positional
        } else {
            GreekNotation::Classic
        },
        letter_case: if capital {
            GreekCase::Upper
        } else {
            GreekCase::Lower
        },
    }
}

/// Converts an Arabic integer or finite float to a Greek numeral.
///
/// Set `positional` to use `~`-separated groups, or leave it false for classic underscore
/// notation. `capital` selects uppercase Greek numerals.
///
/// # Python example
///
/// ```python
/// >>> arabic_to_greek(1.05, positional=False, capital=False)
/// 'α.(_:ε)'
/// ```
#[pyfunction]
pub fn arabic_to_greek(
    number: &Bound<'_, PyAny>,
    positional: bool,
    capital: bool,
) -> PyResult<String> {
    let number = extract_arabic_number(number)?;
    core_arabic_to_greek(&number, greek_options(positional, capital)).map_err(map_conversion_error)
}

/// Converts a Greek numeral in classic or positional form to an Arabic integer or float.
///
/// The `positional` and `capital` flags must match those used for the original conversion.
///
/// # Python example
///
/// ```python
/// >>> greek_to_arabic('α.(_:ε)', positional=False, capital=False)
/// 1.05
/// ```
#[pyfunction]
pub fn greek_to_arabic<'py>(
    py: Python<'py>,
    numeral: &str,
    positional: bool,
    capital: bool,
) -> PyResult<Bound<'py, PyAny>> {
    let number = core_greek_to_arabic(numeral, greek_options(positional, capital))
        .map_err(map_conversion_error)?;
    arabic_number_to_python(py, number)
}
