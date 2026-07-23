import os
from functools import lru_cache
from typing import Protocol

from . import _python_impl


class BackendProtocol(Protocol):
    name: str

    def arabic_to_roman(self, number: int) -> str: ...

    def roman_to_arabic(self, numeral: str) -> int: ...

    def arabic_to_greek(self, number: int, positional: bool, capital: bool) -> str: ...

    def greek_to_arabic(self, numeral: str, positional: bool, capital: bool) -> int: ...


def _should_force_python() -> bool:
    value = os.getenv("GREEKROMAN_FORCE_PYTHON", "").strip().lower()
    return value in {"1", "true", "yes", "on"}


def _load_rust_backend() -> BackendProtocol | None:
    try:
        from . import _rust_impl
    except Exception:
        return None
    return _rust_impl


@lru_cache(maxsize=1)
def _select_backend_cached() -> BackendProtocol:
    if _should_force_python():
        return _python_impl

    rust_backend = _load_rust_backend()
    if rust_backend is not None:
        return rust_backend

    return _python_impl


def get_backend(force_refresh: bool = False) -> BackendProtocol:
    if force_refresh:
        _select_backend_cached.cache_clear()
    return _select_backend_cached()


def get_backend_name(force_refresh: bool = False) -> str:
    return get_backend(force_refresh=force_refresh).name
