//! Native conversion backend for Greek and Roman numerals.
//!
//! The Python extension exposes arbitrary-precision integer conversions and finite `f64`
//! conversions. Fractional digits are encoded as numeral tokens separated by `:`; `0` marks
//! a zero digit. For example, `1.25` is written as `I.(II:V)` or `α.(β:ε)`.
//!
//! Conversion implementations are organized by responsibility in [`greek`] and [`roman`].

mod common;
pub mod greek;
pub mod roman;

use greek::{arabic_to_greek, greek_to_arabic};
use pyo3::prelude::*;
use pyo3::types::PyModule;
use roman::{arabic_to_roman, roman_to_arabic};

#[pymodule]
/// Registers native numeral conversion functions in the `_native` Python module.
fn _native(_py: Python<'_>, module: &Bound<'_, PyModule>) -> PyResult<()> {
    module.add_function(wrap_pyfunction!(arabic_to_roman, module)?)?;
    module.add_function(wrap_pyfunction!(roman_to_arabic, module)?)?;
    module.add_function(wrap_pyfunction!(arabic_to_greek, module)?)?;
    module.add_function(wrap_pyfunction!(greek_to_arabic, module)?)?;
    Ok(())
}
