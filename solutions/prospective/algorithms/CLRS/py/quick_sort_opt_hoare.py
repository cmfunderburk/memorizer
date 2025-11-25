"""
Quicksort (Optimized Hoare)

Improvements:
1. Median-of-Three pivot (fixes O(n^2) on sorted arrays).
2. Uses Hoare partition (3x fewer swaps than Lomuto).
"""
=== MEMO START ===
def median_of_three(arr, low, high):
    mid = (low + high) // 2
    if arr[low] > arr[mid]:
        arr[low], arr[mid] = arr[mid], arr[low]
    if arr[low] > arr[high]:
        arr[low], arr[high] = arr[high], arr[low]
    if arr[mid] > arr[high]:
        arr[mid], arr[high] = arr[high], arr[mid]
    
    # Median is now at mid; swap with low to use as pivot
    arr[mid], arr[low] = arr[low], arr[mid]
    return arr[low]

def partition(arr, low, high):
    pivot = median_of_three(arr, low, high)
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
