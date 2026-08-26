"""Thread-safe token bucket rate limiter for API throttling."""

import time
import threading
import logging

# Configure structured logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class TokenBucketRateLimiter:
    """Thread-safe rate limiter using a token bucket algorithm."""

    def __init__(self, capacity: int, refill_rate: float) -> None:
        """
        Initializes the rate limiter.
        
        Args:
            capacity: Maximum number of tokens the bucket can hold.
            refill_rate: Rate at which tokens regenerate per second.
        """
        self.capacity: float = float(capacity)
        self.tokens: float = float(capacity)
        self.refill_rate: float = float(refill_rate)
        self.last_refill: float = time.monotonic()
        self.lock: threading.Lock = threading.Lock()
        logger.info(f"Initialized TokenBucketRateLimiter with capacity={capacity}, refill_rate={refill_rate}")

    def acquire(self, tokens: int = 1) -> bool:
        """
        Attempts to acquire a specified number of tokens thread-safely.
        
        Args:
            tokens: Number of tokens to request.
            
        Returns:
            True if tokens were successfully acquired, False otherwise.
        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill
            self.last_refill = now

            # Refill tokens based on elapsed time
            self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)

            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            
            logger.warning("Rate limit exceeded. Token acquisition failed.")
            return False
