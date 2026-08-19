"""Token bucket rate limiter utility for API request throttling."""

from dataclasses import dataclass
import time
from typing import Optional


@dataclass
class RateLimitConfig:
    """Configuration settings for rate limiting thresholds."""
    max_tokens: int
    refill_rate_per_sec: float


class TokenBucketRateLimiter:
    """Thread-safe token bucket implementation for rate limiting."""

    def __init__(self, config: RateLimitConfig) -> None:
        if config.max_tokens <= 0:
            raise ValueError("max_tokens must be a positive integer.")
        if config.refill_rate_per_sec <= 0:
            raise ValueError("refill_rate_per_sec must be greater than zero.")

        self._config = config
        self._tokens: float = float(config.max_tokens)
        self._last_refill_time: float = time.monotonic()

    def _refill(self) -> None:
        """Calculates elapsed time and replenishes available tokens."""
        now = time.monotonic()
        elapsed = now - self._last_refill_time
        added_tokens = elapsed * self._config.refill_rate_per_sec
        self._tokens = min(float(self._config.max_tokens), self._tokens + added_tokens)
        self._last_refill_time = now

    def consume(self, tokens_requested: int = 1) -> bool:
        """Attempts to consume the specified number of tokens.

        Returns:
            True if tokens were consumed successfully, False if rate limited.
        """
        if tokens_requested <= 0:
            raise ValueError("tokens_requested must be at least 1.")

        self._refill()

        if self._tokens >= tokens_requested:
            self._tokens -= tokens_requested
            return True
        return False