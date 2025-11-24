--[[
Quicksort (Hoare Partition)

Time Complexity: O(n log n) avg
Space Complexity: O(log n) stack

Hoare's partition is generally more efficient than Lomuto's (fewer swaps).
--]]
-- === MEMO START ===
function partition(arr, low, high)
    local pivot = arr[low]
    local i = low - 1
    local j = high + 1
    
    while true do
        repeat
            i = i + 1
        until arr[i] >= pivot
        
        repeat
            j = j - 1
        until arr[j] <= pivot
        
        if i >= j then
            return j
        end
        
        arr[i], arr[j] = arr[j], arr[i]
    end
end

function quick_sort(arr, low, high)
    if low < high then
        local p = partition(arr, low, high)
        quick_sort(arr, low, p)
        quick_sort(arr, p + 1, high)
    end
end

