"""Tests for the token-bucket rate limiter."""

from __future__ import annotations

import math
from concurrent.futures import ThreadPoolExecutor

import pytest

from toolkit.rate_limiter import RateLimiter


class Clock:
    def __init__(self) -> None:
        self.now = 0.0

    def __call__(self) -> float:
        return self.now


def test_burst_then_block() -> None:
    limiter = RateLimiter(3, 0)

    assert [limiter.try_acquire() for _ in range(4)] == [True, True, True, False]


def test_refills_over_simulated_time_without_exceeding_capacity() -> None:
    clock = Clock()
    limiter = RateLimiter(4, 2, clock=clock)

    assert limiter.try_acquire(4)
    clock.now = 0.75
    assert limiter.try_acquire(1.5)
    assert not limiter.try_acquire()

    clock.now = 10
    assert limiter.try_acquire(4)
    assert not limiter.try_acquire()


def test_clock_moving_backwards_does_not_refill() -> None:
    clock = Clock()
    limiter = RateLimiter(1, 1, clock=clock)
    assert limiter.try_acquire()

    clock.now = -10
    assert not limiter.try_acquire()
    clock.now = 1
    assert limiter.try_acquire()


@pytest.mark.parametrize("invalid", [0, -1, math.inf, -math.inf, math.nan])
def test_rejects_invalid_capacity(invalid: float) -> None:
    with pytest.raises(ValueError):
        RateLimiter(invalid, 1)


@pytest.mark.parametrize("invalid", [-1, math.inf, -math.inf, math.nan])
def test_rejects_invalid_refill_rate(invalid: float) -> None:
    with pytest.raises(ValueError):
        RateLimiter(1, invalid)


@pytest.mark.parametrize("invalid", [0, -1, math.inf, -math.inf, math.nan])
def test_rejects_invalid_acquisition(invalid: float) -> None:
    with pytest.raises(ValueError):
        RateLimiter(1, 1).try_acquire(invalid)


@pytest.mark.parametrize("invalid", [math.inf, -math.inf, math.nan])
def test_non_finite_clock_reading_does_not_poison_refills(invalid: float) -> None:
    clock = Clock()
    limiter = RateLimiter(1, 1, clock=clock)
    assert limiter.try_acquire()

    clock.now = invalid
    with pytest.raises(ValueError):
        limiter.try_acquire()

    clock.now = 1
    assert limiter.try_acquire()


def test_concurrent_acquisitions_cannot_overdraw_bucket() -> None:
    capacity = 40
    limiter = RateLimiter(capacity, 0)

    with ThreadPoolExecutor(max_workers=32) as executor:
        results = list(executor.map(lambda _: limiter.try_acquire(), range(500)))

    assert sum(results) == capacity
    assert not limiter.try_acquire()
