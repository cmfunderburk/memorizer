--[[
Selection Sort

Time Complexity: O(n^2)
Space Complexity: O(1)

In-place sort that repeatedly finds the minimum element from the unsorted
part and puts it at the beginning.
--]]
-- === MEMO START ===
function selection_sort(arr)
    local n = #arr
    for i = 1, n do
        local min_idx = i
        for j = i + 1, n do
            if arr[j] < arr[min_idx] then
                min_idx = j
            end
        end
        
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    end
    return arr
end

