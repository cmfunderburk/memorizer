# Quicksort (Hoare Partition)

**Time:** O(n log n) avg  |  **Space:** O(log n) stack

## How It Works

Hoare's partition scheme:
1. Choose pivot (first element)
2. Move pointers inward from both ends
3. Swap elements on wrong sides of pivot
4. Recurse on both partitions

Key insight: Hoare's partition is more efficient than Lomuto's (fewer swaps).

## Implementation

The partition function using Hoare's scheme:

```python
def partition_hoare(arr, low, high):
    pivot = arr[low]
    i = low - 1
    j = high + 1
    while True:
        i += 1
        while arr[i] < pivot:
            i += 1
        j -= 1
        while arr[j] > pivot:
            j -= 1  
        if i >= j:
            return j
        arr[i], arr[j] = arr[j], arr[i]
```

The main recursive function:

```python
def quick_sort(arr, low, high):
    if low < high:
        p = partition_hoare(arr, low, high)
        quick_sort(arr, low, p)
        quick_sort(arr, p + 1, high)
```

## When to Use

- Need in-place sorting with good average performance
- Memory constrained (O(log n) stack vs O(n) for merge sort)
- Data is random (not already sorted)

