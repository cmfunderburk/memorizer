--[[
Two Pointers Template

Common pattern for sorted arrays (e.g., 2Sum II) or checking palindromes.
- Left starts at 1, Right starts at #arr.
- Move pointers based on condition.
--]]
-- === MEMO START ===
function two_pointers(arr, target)
    local l = 1
    local r = #arr
    
    while l < r do
        local current_sum = arr[l] + arr[r]
        if current_sum == target then
            return {l, r}
        elseif current_sum < target then
            l = l + 1
        else
            r = r - 1
        end
    end
    return {}
end

