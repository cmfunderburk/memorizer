# Sorting
def hasDuplicate(nums):
    nums.sort() # Powersort O(nlogn)
    for i in range(1, len(nums)):
        if nums[i] == nums[i-1]:
            return True
    return False

# Hash Set
def hasDuplicate(nums):
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False
