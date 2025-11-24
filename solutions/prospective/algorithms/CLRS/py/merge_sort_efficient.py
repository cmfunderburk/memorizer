"""
Merge Sort (Efficient Indices)

Time Complexity: O(n log n)
Space Complexity: O(n)

Avoids slicing overhead by passing indices and using a single temp array.
"""
=== MEMO START ===
def merge(arr, temp, left, mid, right):
    i = left
    j = mid + 1
    k = left
    
    while i <= mid and j <= right:
        if arr[i] <= arr[j]:
            temp[k] = arr[i]
            i += 1
        else:
            temp[k] = arr[j]
            j += 1
        k += 1
        
    while i <= mid:
        temp[k] = arr[i]
        k += 1
        i += 1
    while j <= right:
        temp[k] = arr[j]
        k += 1
        j += 1
        
    for i in range(left, right + 1):
        arr[i] = temp[i]

def merge_sort_helper(arr, temp, left, right):
    if left < right:
        mid = (left + right) // 2
        merge_sort_helper(arr, temp, left, mid)
        merge_sort_helper(arr, temp, mid + 1, right)
        merge(arr, temp, left, mid, right)

def merge_sort(arr):
    if len(arr) < 2:
        return arr
    temp = [0] * len(arr)
    merge_sort_helper(arr, temp, 0, len(arr) - 1)
    return arr

