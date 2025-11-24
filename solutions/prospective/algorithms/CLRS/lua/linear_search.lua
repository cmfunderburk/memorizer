--[[
Linear Search

Time Complexity: O(n)
Space Complexity: O(1)

Returns the index of target in arr, or -1 if not found.
--]]
-- === MEMO START ===
function linear_search(arr, target)
    for i = 1, #arr do
        if arr[i] == target then
            return i
        end
    end
    return -1
end

