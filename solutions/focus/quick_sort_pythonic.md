# Quicksort (Pythonic)

**Time:** O(n log n) avg, O(n²) worst  |  **Space:** O(n)

## How It Works

Functional-style quicksort using list comprehensions:
1. Base case: arrays of length < 2 are sorted
2. Choose middle element as pivot
3. Filter into three lists: less, equal, greater
4. Recursively sort and concatenate

Key insight: Clarity over efficiency—allocates new lists each call.

## Implementation

```python
def quick_sort(arr):
    if len(arr) < 2:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)
```

## When to Use

- Code clarity is priority over performance
- In-place mutation is unnecessary
- Working with immutable data patterns
- Teaching/demonstrating quicksort concept

