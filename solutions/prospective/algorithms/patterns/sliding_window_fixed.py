"""
Fixed Sliding Window Template

Used for finding something in a subarray of fixed size k.
1. Initialize window with first k elements.
2. Slide window one step at a time (add new, remove old).
"""
=== MEMO START ===
def sliding_window_fixed(arr, k):
    if len(arr) < k:
        return 0
        
    # Initial window
    current_sum = sum(arr[:k])
    max_sum = current_sum
    
    # Slide
    for i in range(len(arr) - k):
        current_sum = current_sum - arr[i] + arr[i + k]
        max_sum = max(max_sum, current_sum)
        
    return max_sum

