"""
Functools lru_cache (Memoization)

Decorator to cache results of function calls.
maxsize=None means unlimited cache.
"""
=== MEMO START ===
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)

# Clear cache if needed
fib.cache_clear()

