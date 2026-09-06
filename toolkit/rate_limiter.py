"""Thread-safe token-bucket rate limiting."""

from __future__ import annotations

import math
import threading
import time
from collections.abc import Callable


class RateLimiter:
    """A token bucket that refills continuously at a fixed rate."""

    def __init__(
        self,
        capacity: float,
        refill_rate: float,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        if not math.isfinite(capacity) or capacity <= 0:
            raise ValueError("capacity must be finite and greater than zero")
        if not math.isfinite(refill_rate) or refill_rate <= 0:
            raise ValueError("refill_rate must be finite and greater than zero")

        self._capacity = capacity
        self._refill_rate = refill_rate
        self._clock = clock
        self._tokens = capacity
        self._last_refill = clock()
        self._lock = threading.Lock()

    def try_acquire(self, tokens: float = 1) -> bool:
        """Consume tokens if available, returning whether the request succeeded."""
        if not math.isfinite(tokens) or tokens <= 0:
            raise ValueError("tokens must be finite and greater than zero")

        with self._lock:
            now = self._clock()
            elapsed = max(0.0, now - self._last_refill)
            self._tokens = min(
                self._capacity,
                self._tokens + elapsed * self._refill_rate,
            )
            self._last_refill = max(self._last_refill, now)

            if tokens > self._tokens:
                return False
            self._tokens -= tokens
            return True
