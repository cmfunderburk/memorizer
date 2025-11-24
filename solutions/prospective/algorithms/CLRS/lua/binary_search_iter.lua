--[[
Iterative Binary Search

Time Complexity: O(log n)
Space Complexity: O(1)

Returns the index of target in sorted array arr, or -1 if not found.
--]]
-- === MEMO START ===
function binary_search(arr, target)
    local low = 1
    local high = #arr
    
    while low <= high do
        local mid = math.floor((low + high) / 2)
        if arr[mid] == target then
            return mid
        elseif arr[mid] < target then
            low = mid + 1
        else
            high = mid - 1
        end
    end
    
    return -1
end

