"""
Quicksort (Pythonic List-Comprehension)

Time: O(n log n) average, O(n^2) worst when pivot is poor.
Space: O(n) because every call allocates three new lists.

Useful for clarity when in-place mutation is unnecessary.
"""
=== MEMO START ===
def quick_sort(arr):
    if len(arr) < 2:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)
