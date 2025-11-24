--[[
Prefix Sum + HashMap Template

Used for finding subarrays with a target sum (e.g. k).
- Map stores {prefix_sum: count}
- curr_sum - target = old_prefix_sum
--]]
-- === MEMO START ===
function subarray_sum(nums, k)
    local count = 0
    local curr_sum = 0
    local prefix_sums = {[0] = 1} -- Base case: sum 0 exists once
    
    for _, num in ipairs(nums) do
        curr_sum = curr_sum + num
        local diff = curr_sum - k
        
        count = count + (prefix_sums[diff] or 0)
        prefix_sums[curr_sum] = (prefix_sums[curr_sum] or 0) + 1
    end
    
    return count
end

