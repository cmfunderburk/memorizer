--[[
Heapsort

Time Complexity: O(n log n)
Space Complexity: O(1)

Sorts an array by building a max-heap and then repeatedly extracting the max.
--]]
-- === MEMO START ===
function heapify(arr, n, i)
    local largest = i
    local l = 2 * i
    local r = 2 * i + 1
    
    if l <= n and arr[l] > arr[largest] then
        largest = l
    end
    if r <= n and arr[r] > arr[largest] then
        largest = r
    end
    
    if largest ~= i then
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)
    end
end

function heap_sort(arr)
    local n = #arr
    
    -- Build max heap
    for i = math.floor(n / 2), 1, -1 do
        heapify(arr, n, i)
    end
    
    -- Extract elements one by one
    for i = n, 2, -1 do
        arr[1], arr[i] = arr[i], arr[1] -- swap
        heapify(arr, i - 1, 1)
    end
    
    return arr
end

