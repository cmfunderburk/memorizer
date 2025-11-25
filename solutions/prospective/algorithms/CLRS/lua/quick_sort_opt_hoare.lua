--[[
Quicksort (Optimized Hoare)

Improvements:
1. Median-of-Three pivot (fixes O(n^2) on sorted arrays).
2. Uses Hoare partition (3x fewer swaps than Lomuto).
--]]
-- === MEMO START ===
function median_of_three(arr, low, high)
    local mid = math.floor((low + high) / 2)
    if arr[low] > arr[mid] then arr[low], arr[mid] = arr[mid], arr[low] end
    if arr[low] > arr[high] then arr[low], arr[high] = arr[high], arr[low] end
    if arr[mid] > arr[high] then arr[mid], arr[high] = arr[high], arr[mid] end
    
    -- Median is now at mid; swap with low to use as pivot
    arr[mid], arr[low] = arr[low], arr[mid]
    return arr[low]
end

function partition(arr, low, high)
    local pivot = median_of_three(arr, low, high)
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

