"""
Iterative Binary Search

Time Complexity: O(log n)
Space Complexity: O(1)

Returns the index of target in sorted array arr, or -1 if not found.
"""
=== MEMO START ===
def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
            
    return -1

