"""
Selection Sort

Time Complexity: O(n^2)
Space Complexity: O(1)

In-place sort that repeatedly finds the minimum element from the unsorted
part and puts it at the beginning.
"""
=== MEMO START ===
def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

