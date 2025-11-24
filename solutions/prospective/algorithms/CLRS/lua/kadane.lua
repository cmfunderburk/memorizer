--[[
Kadane's Algorithm (Maximum Subarray Sum)

Time Complexity: O(n)
Space Complexity: O(1)

Finds the contiguous subarray which has the largest sum.
--]]
-- === MEMO START ===
function max_subarray(nums)
    local max_so_far = nums[1]
    local current_max = nums[1]
    
    for i = 2, #nums do
        current_max = math.max(nums[i], current_max + nums[i])
        max_so_far = math.max(max_so_far, current_max)
    end
    
    return max_so_far
end

