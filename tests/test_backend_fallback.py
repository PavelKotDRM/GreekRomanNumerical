import builtins

import pytest

from GreekRomanUtils import _backend


@pytest.mark.parametrize("value", ["1", "true", "yes", "on", " TRUE "])
def test_force_python_backend(monkeypatch, value):
    monkeypatch.setenv("GREEKROMAN_FORCE_PYTHON", value)
    assert _backend.get_backend_name(force_refresh=True) == "python"


@pytest.mark.parametrize("value", ["", "0", "false", "no", "off"])
def test_false_values_do_not_force_python_backend(monkeypatch, value):
    monkeypatch.setenv("GREEKROMAN_FORCE_PYTHON", value)

    assert _backend._should_force_python() is False


def test_fallback_when_rust_unavailable(monkeypatch):
    monkeypatch.delenv("GREEKROMAN_FORCE_PYTHON", raising=False)
    monkeypatch.setattr(_backend, "_load_rust_backend", lambda: None)
    assert _backend.get_backend_name(force_refresh=True) == "python"


def test_fallback_when_rust_import_fails(monkeypatch):
    original_import = builtins.__import__

    def fail_on_rust_import(name, globals=None, locals=None, fromlist=(), level=0):
        if fromlist and "_rust_impl" in fromlist:
            raise ImportError("Rust backend is not installed")
        return original_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", fail_on_rust_import)

    assert _backend._load_rust_backend() is None


def test_rust_backend_loaded_when_available():
    rust_impl = pytest.importorskip("GreekRomanUtils._rust_impl")

    assert _backend._load_rust_backend() is rust_impl


def test_rust_backend_selected_when_available(monkeypatch):
    monkeypatch.delenv("GREEKROMAN_FORCE_PYTHON", raising=False)

    rust_impl = pytest.importorskip("GreekRomanUtils._rust_impl")
    monkeypatch.setattr(_backend, "_load_rust_backend", lambda: rust_impl)

    assert _backend.get_backend_name(force_refresh=True) == "rust"
