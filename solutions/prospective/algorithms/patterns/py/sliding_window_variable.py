"""
Variable Sliding Window Template

Used for finding longest/shortest subarray meeting a condition.
1. Expand right pointer.
2. Shrink left pointer while condition is violated.
"""
=== MEMO START ===
def sliding_window_variable(arr):
    l = 0
    longest = 0
    window_state = set() # or count map
    
    for r in range(len(arr)):
        while arr[r] in window_state:
            window_state.remove(arr[l])
            l += 1
        window_state.add(arr[r])
        longest = max(longest, r - l + 1)
        
    return longest

