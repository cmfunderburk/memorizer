--[[
Merge Sort (Efficient Indices)

Time Complexity: O(n log n)
Space Complexity: O(n)

Avoids slicing overhead by passing indices and using a single temp array.
--]]
-- === MEMO START ===
function merge(arr, temp, left, mid, right)
    local i = left
    local j = mid + 1
    local k = left
    
    while i <= mid and j <= right do
        if arr[i] <= arr[j] then
            temp[k] = arr[i]
            i = i + 1
        else
            temp[k] = arr[j]
            j = j + 1
        end
        k = k + 1
    end
    
    while i <= mid do
        temp[k] = arr[i]
        k = k + 1
        i = i + 1
    end
    while j <= right do
        temp[k] = arr[j]
        k = k + 1
        j = j + 1
    end
    
    for x = left, right do
        arr[x] = temp[x]
    end
end

function merge_sort_helper(arr, temp, left, right)
    if left < right then
        local mid = math.floor((left + right) / 2)
        merge_sort_helper(arr, temp, left, mid)
        merge_sort_helper(arr, temp, mid + 1, right)
        merge(arr, temp, left, mid, right)
    end
end

function merge_sort(arr)
    if #arr < 2 then
        return arr
    end
    local temp = {} -- In Lua tables grow dynamically, but we can treat as array
    for i=1, #arr do temp[i] = 0 end
    
    merge_sort_helper(arr, temp, 1, #arr)
    return arr
end

