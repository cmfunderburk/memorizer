"""
Two Pointers Template

Common pattern for sorted arrays (e.g., 2Sum II) or checking palindromes.
- Left starts at 0, Right starts at len-1.
- Move pointers based on condition.
"""
=== MEMO START ===
def two_pointers(arr, target):
    l, r = 0, len(arr) - 1
    while l < r:
        current_sum = arr[l] + arr[r]
        if current_sum == target:
            return [l, r]
        elif current_sum < target:
            l += 1
        else:
            r -= 1
    return []

