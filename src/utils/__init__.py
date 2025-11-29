"""
Utility functions for web scraping
"""

import time
from functools import wraps
from typing import Any, Callable, Optional

from loguru import logger


def retry_on_exception(
    max_retries: int = 3,
    backoff: float = 0.5,
    exceptions: tuple = (Exception,),
) -> Callable:
    """
    Decorator to retry function on exception

    Args:
        max_retries: Maximum number of retry attempts
        backoff: Backoff multiplier between retries
        exceptions: Tuple of exception types to catch
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            attempt = 0
            wait_time = 1

            while attempt < max_retries:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempt += 1
                    if attempt >= max_retries:
                        logger.error(f"Max retries reached for {func.__name__}: {str(e)}")
                        raise

                    logger.warning(
                        f"{func.__name__} failed (attempt {attempt}/{max_retries}), "
                        f"retrying in {wait_time}s: {str(e)}"
                    )
                    time.sleep(wait_time)
                    wait_time *= backoff

        return wrapper

    return decorator


def rate_limit(calls_per_second: float = 1.0) -> Callable:
    """
    Decorator to rate limit function calls

    Args:
        calls_per_second: Maximum calls per second
    """

    def decorator(func: Callable) -> Callable:
        last_called = [0.0]
        min_interval = 1.0 / calls_per_second

        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            elapsed = time.time() - last_called[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)

            last_called[0] = time.time()
            return func(*args, **kwargs)

        return wrapper

    return decorator


def timeit(func: Callable) -> Callable:
    """Decorator to measure function execution time"""

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start

        logger.info(f"{func.__name__} took {duration:.2f}s")
        return result

    return wrapper
