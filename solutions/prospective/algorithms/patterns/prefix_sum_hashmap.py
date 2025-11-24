"""
Prefix Sum + HashMap Template

Used for finding subarrays with a target sum (e.g. k).
- Map stores {prefix_sum: count_or_index}
- curr_sum - target = old_prefix_sum
"""
=== MEMO START ===
def subarray_sum(nums, k):
    count = 0
    curr_sum = 0
    prefix_sums = {0: 1} # Base case: sum 0 exists once
    
    for num in nums:
        curr_sum += num
        diff = curr_sum - k
        
        count += prefix_sums.get(diff, 0)
        prefix_sums[curr_sum] = prefix_sums.get(curr_sum, 0) + 1
        
    return count

