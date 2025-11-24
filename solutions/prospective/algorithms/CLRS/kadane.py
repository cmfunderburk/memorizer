"""
Kadane's Algorithm (Maximum Subarray Sum)

Time Complexity: O(n)
Space Complexity: O(1)

Finds the contiguous subarray which has the largest sum.
"""
=== MEMO START ===
def max_subarray(nums):
    max_so_far = nums[0]
    current_max = nums[0]
    
    for i in range(1, len(nums)):
        current_max = max(nums[i], current_max + nums[i])
        max_so_far = max(max_so_far, current_max)
        
    return max_so_far

