--[[
Fixed Sliding Window Template

Used for finding something in a subarray of fixed size k.
1. Initialize window with first k elements.
2. Slide window one step at a time (add new, remove old).
--]]
-- === MEMO START ===
function sliding_window_fixed(arr, k)
    if #arr < k then
        return 0
    end
    
    -- Initial window
    local current_sum = 0
    for i = 1, k do
        current_sum = current_sum + arr[i]
    end
    local max_sum = current_sum
    
    -- Slide
    for i = 1, #arr - k do
        current_sum = current_sum - arr[i] + arr[i + k]
        if current_sum > max_sum then
            max_sum = current_sum
        end
    end
    
    return max_sum
end

