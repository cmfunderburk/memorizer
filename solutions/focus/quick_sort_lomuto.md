# Quicksort (Lomuto Partition)

**Time:** O(n log n) avg, O(n²) worst  |  **Space:** O(log n) stack

## How It Works

Lomuto's partition scheme:
1. Choose pivot (last element)
2. Maintain boundary of elements less than pivot
3. Scan left to right, swapping smaller elements to the left
4. Place pivot in final position

Key insight: Simpler than Hoare but does more swaps.

## Implementation

The partition function using Lomuto's scheme:

```python
def partition_lomuto(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i+1], arr[high] = arr[high], arr[i+1]
    return i + 1
```

The main recursive function:

```python
def quick_sort(arr, low, high):
    if low < high:
        p = partition_lomuto(arr, low, high)
        quick_sort(arr, low, p - 1)
        quick_sort(arr, p + 1, high)
```

## When to Use

- Learning quicksort (simpler to understand than Hoare)
- Need in-place sorting
- Data is random (not already sorted)

