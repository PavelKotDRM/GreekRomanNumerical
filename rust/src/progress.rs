use std::io::{self, Stderr};
use std::thread;

use greekromannumerical_core::{
    ArabicNumber, ConversionError, ProgressBar as CoreProgressBar, SharedProgressBar,
};
use pyo3::exceptions::{PyOSError, PyRuntimeError};
use pyo3::prelude::*;
use pyo3::types::PyModule;

use crate::common::{extract_arabic_numbers, map_conversion_error};

/// Maximum number of progress updates emitted by each worker thread.
const UPDATES_PER_WORKER: usize = 100;

type ConversionResults = io::Result<Vec<Result<String, ConversionError>>>;

fn map_progress_error(error: io::Error) -> PyErr {
    if error.kind() == io::ErrorKind::InvalidInput {
        PyRuntimeError::new_err(error.to_string())
    } else {
        PyOSError::new_err(error.to_string())
    }
}

/// Terminal progress bar backed by the `greekromannumerical-core` implementation.
///
/// Output goes to standard error and is suppressed when standard error is not a terminal.
/// The bar can be used as a context manager; it is finished when the block exits normally.
#[pyclass(module = "GreekRomanUtils._native", name = "ProgressBar", frozen)]
pub struct ProgressBar {
    inner: SharedProgressBar<Stderr>,
    total: u64,
}

impl ProgressBar {
    fn create(total: u64, message: Option<&str>) -> PyResult<Self> {
        let inner = CoreProgressBar::new(total).shared();
        if let Some(message) = message {
            inner.set_message(message).map_err(map_progress_error)?;
        }
        Ok(Self { inner, total })
    }
}

#[pymethods]
impl ProgressBar {
    #[new]
    #[pyo3(signature = (total, message=None))]
    fn new(total: u64, message: Option<&str>) -> PyResult<Self> {
        Self::create(total, message)
    }

    #[getter]
    fn total(&self) -> u64 {
        self.total
    }

    #[getter]
    fn position(&self) -> PyResult<u64> {
        self.inner.position().map_err(map_progress_error)
    }

    fn set_message(&self, message: &str) -> PyResult<()> {
        self.inner.set_message(message).map_err(map_progress_error)
    }

    fn set_position(&self, position: u64) -> PyResult<()> {
        self.inner
            .set_position(position)
            .map_err(map_progress_error)
    }

    #[pyo3(signature = (amount=1))]
    fn inc(&self, amount: u64) -> PyResult<()> {
        self.inner.inc(amount).map_err(map_progress_error)
    }

    fn finish(&self) -> PyResult<()> {
        self.inner.finish().map_err(map_progress_error)
    }

    fn __enter__(slf: PyRef<'_, Self>) -> PyRef<'_, Self> {
        slf
    }

    fn __exit__(
        &self,
        exc_type: &Bound<'_, PyAny>,
        _exc_value: &Bound<'_, PyAny>,
        _traceback: &Bound<'_, PyAny>,
    ) -> PyResult<bool> {
        if exc_type.is_none() {
            self.finish()?;
        }
        Ok(false)
    }
}

/// Converts numbers on worker threads while advancing `progress` as items complete.
///
/// Rendering failures are ignored so that a broken terminal never aborts a conversion.
fn parallel_map_with_progress<F>(
    numbers: &[ArabicNumber],
    convert: F,
    progress: &SharedProgressBar<Stderr>,
) -> ConversionResults
where
    F: Fn(&ArabicNumber) -> Result<String, ConversionError> + Sync,
{
    if numbers.is_empty() {
        let _ = progress.finish();
        return Ok(Vec::new());
    }

    let workers = thread::available_parallelism()
        .map_or(1, usize::from)
        .min(numbers.len());
    let chunk_size = numbers.len().div_ceil(workers);
    let update_step = chunk_size.div_ceil(UPDATES_PER_WORKER).max(1);

    let convert_chunk = |chunk: &[ArabicNumber]| {
        let mut results = Vec::with_capacity(chunk.len());
        let mut pending = 0u64;
        for number in chunk {
            results.push(convert(number));
            pending += 1;
            if pending as usize >= update_step {
                let _ = progress.inc(pending);
                pending = 0;
            }
        }
        if pending > 0 {
            let _ = progress.inc(pending);
        }
        results
    };

    let results = thread::scope(|scope| {
        let mut handles = Vec::with_capacity(workers);
        for chunk in numbers.chunks(chunk_size) {
            let convert_chunk = &convert_chunk;
            handles.push(thread::Builder::new().spawn_scoped(scope, move || convert_chunk(chunk))?);
        }

        let mut results = Vec::with_capacity(numbers.len());
        for handle in handles {
            let chunk_results = handle
                .join()
                .map_err(|_| io::Error::other("parallel conversion worker panicked"))?;
            results.extend(chunk_results);
        }
        Ok(results)
    });
    let _ = progress.finish();
    results
}

/// Converts a Python iterable in parallel, optionally rendering a progress bar on stderr.
///
/// `parallel` is used when no progress is requested; `convert` converts a single item when
/// progress reporting is enabled.
pub(crate) fn convert_batch<P, F>(
    py: Python<'_>,
    numbers: &Bound<'_, PyAny>,
    progress: bool,
    message: Option<&str>,
    parallel: P,
    convert: F,
) -> PyResult<Vec<String>>
where
    P: FnOnce(&[ArabicNumber]) -> ConversionResults + Send,
    F: Fn(&ArabicNumber) -> Result<String, ConversionError> + Sync + Send,
{
    let numbers = extract_arabic_numbers(numbers)?;
    let results = if progress {
        let bar = ProgressBar::create(numbers.len() as u64, message)?;
        py.detach(|| parallel_map_with_progress(&numbers, convert, &bar.inner))
    } else {
        py.detach(|| parallel(&numbers))
    }
    .map_err(|error| PyRuntimeError::new_err(error.to_string()))?;

    results
        .into_iter()
        .map(|result| result.map_err(map_conversion_error))
        .collect()
}

pub(crate) fn register(module: &Bound<'_, PyModule>) -> PyResult<()> {
    module.add_class::<ProgressBar>()
}

#[cfg(test)]
mod tests {
    use super::parallel_map_with_progress;
    use greekromannumerical_core::{ArabicNumber, ProgressBar, arabic_to_roman};

    #[test]
    fn progress_map_preserves_order_and_completes_bar() {
        let numbers: Vec<_> = (1..=250).map(|n| ArabicNumber::Integer(n.into())).collect();
        let progress = ProgressBar::new(numbers.len() as u64).shared();

        let results = parallel_map_with_progress(&numbers, arabic_to_roman, &progress).unwrap();

        let expected: Vec<_> = numbers.iter().map(arabic_to_roman).collect();
        assert_eq!(results, expected);
        assert_eq!(progress.position().unwrap(), numbers.len() as u64);
    }
}
