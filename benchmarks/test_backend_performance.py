from typing import Any

import pytest

from GreekRomanUtils import _python_impl

LARGE_NUMBER = 10**30 + 123456
CLASSIC_GREEK = _python_impl.arabic_to_greek(LARGE_NUMBER, False, False)
POSITIONAL_GREEK = _python_impl.arabic_to_greek(LARGE_NUMBER, True, True)

BENCHMARK_CASES = (
    pytest.param("arabic_to_roman", (123456,), id="roman-encode"),
    pytest.param("roman_to_arabic", ("~C~X~XMMMCDLVI",), id="roman-decode"),
    pytest.param(
        "arabic_to_greek",
        (LARGE_NUMBER, False, False),
        id="greek-classic-encode",
    ),
    pytest.param(
        "greek_to_arabic",
        (CLASSIC_GREEK, False, False),
        id="greek-classic-decode",
    ),
    pytest.param(
        "arabic_to_greek",
        (LARGE_NUMBER, True, True),
        id="greek-positional-encode",
    ),
    pytest.param(
        "greek_to_arabic",
        (POSITIONAL_GREEK, True, True),
        id="greek-positional-decode",
    ),
)


def _load_backend(name: str) -> Any:
    if name == "python":
        return _python_impl

    try:
        from GreekRomanUtils import _rust_impl
    except ImportError:
        pytest.skip("Build the Rust extension with maturin develop to benchmark it")
    return _rust_impl


@pytest.mark.parametrize("backend_name", ("python", "rust"), ids=("python", "rust"))
@pytest.mark.parametrize(("operation", "arguments"), BENCHMARK_CASES)
def test_conversion_performance(
    benchmark: Any,
    backend_name: str,
    operation: str,
    arguments: tuple[Any, ...],
) -> None:
    backend = _load_backend(backend_name)
    conversion = getattr(backend, operation)
    expected = getattr(_python_impl, operation)(*arguments)

    assert conversion(*arguments) == expected

    result = benchmark.pedantic(
        conversion,
        args=arguments,
        rounds=10,
        iterations=100,
        warmup_rounds=2,
    )
    assert result == expected