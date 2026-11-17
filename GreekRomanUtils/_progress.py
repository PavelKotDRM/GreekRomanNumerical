"""Pure-Python progress bar mirroring the ``greekromannumerical-core`` terminal renderer."""

import sys
import threading
import unicodedata
from types import TracebackType
from typing import Protocol, Self, TextIO

_BAR_WIDTH = 30


class ProgressBarProtocol(Protocol):
    @property
    def total(self) -> int: ...

    @property
    def position(self) -> int: ...

    def set_message(self, message: str) -> None: ...

    def set_position(self, position: int) -> None: ...

    def inc(self, amount: int = 1) -> None: ...

    def finish(self) -> None: ...

    def __enter__(self) -> Self: ...

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool: ...


def _check_non_negative(name: str, value: int) -> int:
    if value < 0:
        raise OverflowError(f"{name} must be non-negative")
    return value


class ProgressBar:
    """Thread-safe terminal progress bar.

    Output goes to ``stream`` when given; otherwise to ``sys.stderr`` only when it is a
    terminal. The bar is finished when used as a context manager and the block exits normally.
    """

    def __init__(
        self,
        total: int,
        message: str | None = None,
        *,
        stream: TextIO | None = None,
    ) -> None:
        self._total = _check_non_negative("total", total)
        self._position = 0
        self._message = ""
        self._finished = False
        self._lock = threading.Lock()
        if stream is None:
            stream = sys.stderr
            self._enabled = stream is not None and stream.isatty()
        else:
            self._enabled = True
        self._stream = stream
        if message is not None:
            self.set_message(message)

    @property
    def total(self) -> int:
        return self._total

    @property
    def position(self) -> int:
        with self._lock:
            return self._position

    def set_message(self, message: str) -> None:
        with self._lock:
            self._ensure_active()
            self._message = "".join(
                " " if unicodedata.category(character) == "Cc" else character
                for character in message
            )
            self._render()

    def set_position(self, position: int) -> None:
        _check_non_negative("position", position)
        with self._lock:
            self._ensure_active()
            self._position = min(position, self._total)
            self._render()

    def inc(self, amount: int = 1) -> None:
        _check_non_negative("amount", amount)
        with self._lock:
            self._ensure_active()
            self._position = min(self._position + amount, self._total)
            self._render()

    def finish(self) -> None:
        with self._lock:
            if self._finished:
                return
            self._position = self._total
            self._render()
            if self._enabled:
                self._stream.write("\n")
                self._stream.flush()
            self._finished = True

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        if exc_type is None:
            self.finish()
        return False

    def _ensure_active(self) -> None:
        if self._finished:
            raise RuntimeError("progress bar is already finished")

    def _render(self) -> None:
        if not self._enabled:
            return
        if self._total == 0:
            filled, percent = _BAR_WIDTH, 100
        else:
            filled = self._position * _BAR_WIDTH // self._total
            percent = self._position * 100 // self._total
        prefix = f"{self._message} " if self._message else ""
        bar = "=" * filled + " " * (_BAR_WIDTH - filled)
        self._stream.write(
            f"\r\x1b[2K{prefix}[{bar}] {percent:3}% ({self._position}/{self._total})"
        )
        self._stream.flush()
