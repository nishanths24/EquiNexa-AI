import time
import random
import asyncio
from typing import Callable, Any

class CircuitBreakerOpen(Exception):
    pass

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 50, recovery_timeout: float = 60.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failures = 0
        self.last_failure_time = 0
        self.state = "CLOSED"

    def record_failure(self):
        self.failures += 1
        self.last_failure_time = time.time()
        if self.failures >= self.failure_threshold:
            self.state = "OPEN"

    def record_success(self):
        self.failures = 0
        self.state = "CLOSED"

    def check(self):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "HALF_OPEN"
                return True
            raise CircuitBreakerOpen("Circuit breaker is OPEN. Provider is currently failing.")
        return True

global_breaker = CircuitBreaker()

def with_retry_sync(func: Callable, max_attempts: int = 3, base_delay: float = 0.5) -> Any:
    global_breaker.check()
    for attempt in range(max_attempts):
        try:
            res = func()
            global_breaker.record_success()
            return res
        except Exception as e:
            global_breaker.record_failure()
            if attempt == max_attempts - 1:
                raise e
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            time.sleep(delay)

async def with_retry_async(func: Callable, max_attempts: int = 3, base_delay: float = 0.5) -> Any:
    global_breaker.check()
    for attempt in range(max_attempts):
        try:
            res = await func()
            global_breaker.record_success()
            return res
        except Exception as e:
            global_breaker.record_failure()
            if attempt == max_attempts - 1:
                raise e
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            await asyncio.sleep(delay)
