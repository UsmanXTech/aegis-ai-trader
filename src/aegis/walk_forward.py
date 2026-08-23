from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Sequence, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class WalkForwardWindow:
    train: tuple[T, ...]
    validation: tuple[T, ...]
    test: tuple[T, ...]


def _key(value: object) -> datetime:
    if isinstance(value, tuple) and value and isinstance(value[0], str):
        return datetime.fromisoformat(value[0].replace("Z", "+00:00"))
    raise TypeError("walk-forward items must be (ISO timestamp, payload) tuples")


def make_walk_forward_windows(
    snapshots: Sequence[T],
    *,
    train_size: int,
    validation_size: int,
    test_size: int,
    step: int | None = None,
) -> list[WalkForwardWindow]:
    if min(train_size, validation_size, test_size) <= 0:
        raise ValueError("window sizes must be positive")
    if step is None:
        step = test_size
    if step <= 0:
        raise ValueError("step must be positive")

    ordered = tuple(sorted(snapshots, key=_key))
    windows: list[WalkForwardWindow] = []
    start = 0
    total = train_size + validation_size + test_size
    while start + total <= len(ordered):
        train_end = start + train_size
        validation_end = train_end + validation_size
        test_end = validation_end + test_size
        windows.append(
            WalkForwardWindow(
                train=ordered[start:train_end],
                validation=ordered[train_end:validation_end],
                test=ordered[validation_end:test_end],
            )
        )
        start += step
    return windows
