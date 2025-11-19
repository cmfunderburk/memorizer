from __future__ import annotations


def quicksort(values):
    """Canonical quicksort implementation used for memorization."""
    if len(values) <= 1:
        return list(values)
    pivot = values[len(values) // 2]
    left = [v for v in values if v < pivot]
    mid = [v for v in values if v == pivot]
    right = [v for v in values if v > pivot]
    return quicksort(left) + mid + quicksort(right)
