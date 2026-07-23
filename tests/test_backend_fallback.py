import pytest

from GreekRomanUtils import _backend


def test_force_python_backend(monkeypatch):
    monkeypatch.setenv("GREEKROMAN_FORCE_PYTHON", "1")
    assert _backend.get_backend_name(force_refresh=True) == "python"


def test_fallback_when_rust_unavailable(monkeypatch):
    monkeypatch.delenv("GREEKROMAN_FORCE_PYTHON", raising=False)
    monkeypatch.setattr(_backend, "_load_rust_backend", lambda: None)
    assert _backend.get_backend_name(force_refresh=True) == "python"


def test_rust_backend_selected_when_available(monkeypatch):
    monkeypatch.delenv("GREEKROMAN_FORCE_PYTHON", raising=False)

    rust_impl = pytest.importorskip("GreekRomanUtils._rust_impl")
    monkeypatch.setattr(_backend, "_load_rust_backend", lambda: rust_impl)

    assert _backend.get_backend_name(force_refresh=True) == "rust"
