--[[
Variable Sliding Window Template

Used for finding longest/shortest subarray meeting a condition.
1. Expand right pointer.
2. Shrink left pointer while condition is violated.
--]]
-- === MEMO START ===
function sliding_window_variable(arr)
    local l = 1
    local longest = 0
    local window_state = {}
    
    for r = 1, #arr do
        while window_state[arr[r]] do
            window_state[arr[l]] = nil
            l = l + 1
        end
        window_state[arr[r]] = true
        local current_len = r - l + 1
        if current_len > longest then
            longest = current_len
        end
    end
    
    return longest
end

