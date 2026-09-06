from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import threading

import pytest

from toolkit.rate_limiter import RateLimiter


class FakeClock:
    def __init__(self) -> None:
        self.now = 0.0

    def __call__(self) -> float:
        return self.now


def test_burst_then_block() -> None:
    limiter = RateLimiter(capacity=3, refill_rate=1, clock=FakeClock())

    assert limiter.try_acquire(2)
    assert limiter.try_acquire()
    assert not limiter.try_acquire()


def test_refills_over_simulated_time_up_to_capacity() -> None:
    clock = FakeClock()
    limiter = RateLimiter(capacity=4, refill_rate=2, clock=clock)
    assert limiter.try_acquire(4)

    clock.now = 0.75
    assert limiter.try_acquire(1.5)
    assert not limiter.try_acquire()

    clock.now = 10
    assert limiter.try_acquire(4)
    assert not limiter.try_acquire()


def test_concurrent_acquires_cannot_overdraw_bucket() -> None:
    capacity = 25
    attempts = 200
    limiter = RateLimiter(capacity=capacity, refill_rate=1, clock=FakeClock())
    barrier = threading.Barrier(attempts)

    def acquire() -> bool:
        barrier.wait()
        return limiter.try_acquire()

    with ThreadPoolExecutor(max_workers=attempts) as executor:
        successes = sum(executor.map(lambda _: acquire(), range(attempts)))

    assert successes == capacity
    assert not limiter.try_acquire()


@pytest.mark.parametrize("value", [0, -1, float("inf"), float("nan")])
def test_rejects_invalid_configuration(value: float) -> None:
    with pytest.raises(ValueError):
        RateLimiter(capacity=value, refill_rate=1)
    with pytest.raises(ValueError):
        RateLimiter(capacity=1, refill_rate=value)


@pytest.mark.parametrize("tokens", [0, -1, float("inf"), float("nan")])
def test_rejects_invalid_acquire_amount(tokens: float) -> None:
    limiter = RateLimiter(capacity=1, refill_rate=1)
    with pytest.raises(ValueError):
        limiter.try_acquire(tokens)
