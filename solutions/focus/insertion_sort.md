# Insertion Sort

**Time:** O(n²)  |  **Space:** O(1)

## How It Works

Builds sorted array one element at a time. For each element, shift larger 
elements right until we find where it belongs, then insert.

Key insight: the subarray `arr[0:i]` is always sorted.

## Implementation

```python
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i
        while j > 0 and arr[j-1] > key:
            arr[j] = arr[j-1]
            j -= 1
        arr[j] = key
    return arr
```

## When to Use

- Small datasets (n < ~50)
- Nearly-sorted data (runs in O(n))
- Online sorting (can sort as elements arrive)