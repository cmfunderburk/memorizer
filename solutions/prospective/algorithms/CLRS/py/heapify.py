"""
Max-Heapify

Time Complexity: O(log n)
Space Complexity: O(1) or O(log n) recursive

Maintains the max-heap property for a subtree rooted at index i.
Assumes binary tree structure in array.
"""
=== MEMO START ===
def max_heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    
    if left < n and arr[left] > arr[largest]:
        largest = left
    
    if right < n and arr[right] > arr[largest]:
        largest = right
        
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        max_heapify(arr, n, largest)

