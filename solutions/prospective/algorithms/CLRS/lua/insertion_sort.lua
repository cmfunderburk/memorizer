--[[
Insertion Sort

Time Complexity: O(n^2)
Space Complexity: O(1)

Builds the sorted array one item at a time. Efficient for small data sets.
--]]
-- === MEMO START ===
function insertion_sort(arr)
    for i = 2, #arr do
        local key = arr[i]
        local j = i - 1
        while j > 0 and arr[j] > key do
            arr[j + 1] = arr[j]
            j = j - 1
        end
        arr[j + 1] = key
    end
    return arr
end

