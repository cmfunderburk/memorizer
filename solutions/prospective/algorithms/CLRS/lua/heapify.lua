--[[
Max-Heapify

Time Complexity: O(log n)
Space Complexity: O(1) or O(log n) recursive

Maintains the max-heap property for a subtree rooted at index i.
Assumes binary tree structure in array.
Note: Lua uses 1-based indexing. Children of i are 2*i and 2*i+1.
--]]
-- === MEMO START ===
function max_heapify(arr, n, i)
    local largest = i
    local left = 2 * i
    local right = 2 * i + 1
    
    if left <= n and arr[left] > arr[largest] then
        largest = left
    end
    
    if right <= n and arr[right] > arr[largest] then
        largest = right
    end
    
    if largest ~= i then
        arr[i], arr[largest] = arr[largest], arr[i]
        max_heapify(arr, n, largest)
    end
end

