--[[
Quicksort (Lomuto Partition)

Time Complexity: O(n log n) avg, O(n^2) worst
Space Complexity: O(log n) stack

In-place sorting using divide and conquer.
--]]
-- === MEMO START ===
function partition(arr, low, high)
    local pivot = arr[high]
    local i = low - 1
    
    for j = low, high - 1 do
        if arr[j] < pivot then
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]
        end
    end
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
end

function quick_sort(arr, low, high)
    if low < high then
        local p = partition(arr, low, high)
        quick_sort(arr, low, p - 1)
        quick_sort(arr, p + 1, high)
    end
end

