"""Terminal progress bars for long-running conversions.

The bar is provided by the ``greekromannumerical-core`` Rust crate when the native backend is
available, and by an equivalent pure-Python implementation otherwise.
"""

from ._backend import get_backend
from ._progress import ProgressBar as PythonProgressBar
from ._progress import ProgressBarProtocol


def create_progress_bar(total: int, message: str | None = None) -> ProgressBarProtocol:
    """Create a progress bar for ``total`` steps using the active backend.

    Output goes to stderr and is suppressed when stderr is not a terminal.
    """
    return get_backend().create_progress_bar(total, message)


__all__ = ["ProgressBarProtocol", "PythonProgressBar", "create_progress_bar"]
