"""
Quicksort (Hoare Partition)

Time Complexity: O(n log n) avg
Space Complexity: O(log n) stack

Hoare's partition is generally more efficient than Lomuto's (fewer swaps).
"""
=== MEMO START ===
def partition(arr, low, high):
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

def quick_sort(arr, low, high):
    if low < high:
        p = partition(arr, low, high)
        quick_sort(arr, low, p)
        quick_sort(arr, p + 1, high)