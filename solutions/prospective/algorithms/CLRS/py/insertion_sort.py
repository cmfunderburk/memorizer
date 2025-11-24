"""
Insertion Sort

Time Complexity: O(n^2)
Space Complexity: O(1)

Builds the sorted array one item at a time. Efficient for small data sets.
"""
=== MEMO START ===
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i
        while j > 0 and arr[j-1] > key:
            arr[j] = arr[j-1]
            j -= 1
        arr[j] = key
    return arr

