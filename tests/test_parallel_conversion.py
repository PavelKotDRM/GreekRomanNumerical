import io

import pytest

from GreekRomanUtils import _python_impl, create_progress_bar
from GreekRomanUtils._progress import ProgressBar as PythonProgressBar
from GreekRomanUtils.GreekRoman import GreekConvert, RomanConvert


def test_python_backend_parallel_api_converts_iterables():
    assert _python_impl.arabic_to_roman_many(number for number in [4, 2024, 1.25]) == [
        "IV",
        "MMXXIV",
        "I.(II:V)",
    ]
    assert _python_impl.arabic_to_greek_many([4, 1234], positional=False, capital=False) == [
        "δ",
        "α_σλδ",
    ]


def test_converter_batch_methods():
    roman = RomanConvert()
    greek = GreekConvert(positional=True, capital=True)

    assert roman.convert_many([4, 2024]) == ["IV", "MMXXIV"]
    assert greek.convert_many(iter([4, 1234])) == ["Δ", "Α~ΣΛΔ"]


def test_rust_backend_parallel_api_matches_single_conversions():
    rust_impl = pytest.importorskip("GreekRomanUtils._rust_impl")

    numbers = [4, 2024, 1.25]
    assert rust_impl.arabic_to_roman_many(numbers) == [
        rust_impl.arabic_to_roman(number) for number in numbers
    ]
    assert rust_impl.arabic_to_greek_many(numbers, positional=True, capital=True) == [
        rust_impl.arabic_to_greek(number, positional=True, capital=True)
        for number in numbers
    ]


def test_batch_conversion_errors_are_not_silently_discarded():
    with pytest.raises(ValueError):
        RomanConvert().convert_many([4, float("inf")])


def test_python_progress_bar_renders_core_format_and_sanitizes_message():
    stream = io.StringIO()
    with PythonProgressBar(4, "Converting\nnow", stream=stream) as bar:
        bar.inc(3)
        bar.inc(10)
        assert bar.position == 4

    output = stream.getvalue()
    assert "\r\x1b[2KConverting now [======================        ]  75% (3/4)" in output
    assert output.endswith("[" + "=" * 30 + "] 100% (4/4)\n")


def test_python_progress_bar_rejects_updates_after_finish():
    bar = PythonProgressBar(2, stream=io.StringIO())
    bar.finish()
    bar.finish()
    assert bar.position == 2
    with pytest.raises(RuntimeError):
        bar.inc()


def test_python_progress_bar_is_silent_without_terminal(capsys):
    PythonProgressBar(3, "Quiet").finish()
    assert capsys.readouterr().err == ""


@pytest.mark.parametrize("backend_name", ["python", "rust"])
def test_backend_progress_bar_api(backend_name):
    impl = (
        _python_impl
        if backend_name == "python"
        else pytest.importorskip("GreekRomanUtils._rust_impl")
    )
    bar = impl.create_progress_bar(5, "Working")
    assert (bar.total, bar.position) == (5, 0)
    bar.set_position(2)
    bar.inc()
    bar.set_position(99)
    assert bar.position == 5
    bar.finish()
    with pytest.raises(RuntimeError):
        bar.set_message("done")
    with pytest.raises(OverflowError):
        impl.create_progress_bar(-1)


def test_public_progress_bar_uses_active_backend():
    with create_progress_bar(1) as bar:
        bar.inc()
    assert bar.position == 1


@pytest.mark.parametrize("backend_name", ["python", "rust"])
def test_batch_conversion_with_progress_matches_plain_results(backend_name):
    impl = (
        _python_impl
        if backend_name == "python"
        else pytest.importorskip("GreekRomanUtils._rust_impl")
    )
    numbers = list(range(1, 300)) + [1.25]

    assert impl.arabic_to_roman_many(
        iter(numbers), progress=True, message="Roman"
    ) == impl.arabic_to_roman_many(numbers)
    assert impl.arabic_to_greek_many(
        numbers, positional=True, capital=False, progress=True
    ) == impl.arabic_to_greek_many(numbers, positional=True, capital=False)
    assert impl.arabic_to_roman_many([], progress=True) == []
    with pytest.raises(ValueError):
        impl.arabic_to_roman_many([1, float("nan")], progress=True)


def test_converter_batch_methods_accept_progress():
    assert RomanConvert().convert_many([4, 9], progress=True, message="Roman") == ["IV", "IX"]
    assert GreekConvert().convert_many([4], progress=True) == ["δ"]
