--[[
Merge Sort

Time Complexity: O(n log n)
Space Complexity: O(n)

Divide and conquer algorithm. Guaranteed O(n log n) performance.
--]]
-- === MEMO START ===
function merge(L, R)
    local merged = {}
    local i = 1
    local j = 1
    
    while i <= #L and j <= #R do
        if L[i] <= R[j] then
            table.insert(merged, L[i])
            i = i + 1
        else
            table.insert(merged, R[j])
            j = j + 1
        end
    end
    while i <= #L do
        table.insert(merged, L[i])
        i = i + 1
    end
    while j <= #R do
        table.insert(merged, R[j])
        j = j + 1
    end
    return merged
end

function merge_sort(arr)
    if #arr < 2 then
        return arr
    end
    local mid = math.floor(#arr / 2)
    
    local L_part = {}
    for i = 1, mid do table.insert(L_part, arr[i]) end
    
    local R_part = {}
    for i = mid + 1, #arr do table.insert(R_part, arr[i]) end
    
    local L = merge_sort(L_part)
    local R = merge_sort(R_part)
    return merge(L, R)
end

