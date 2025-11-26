# Merge Sort

**Time:** O(n log n)  |  **Space:** O(n)

## How It Works

Divide-and-conquer algorithm:
1. Divide the array into two halves
2. Recursively sort each half
3. Merge the sorted halves

Key insight: Merging two sorted arrays is O(n).

## Implementation

The merge function combines two sorted arrays:

```python
def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

The main recursive function:

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)
```

## When to Use

- Need guaranteed O(n log n) worst case
- Stable sort required
- Sorting linked lists (no random access needed)
- External sorting (large datasets)

