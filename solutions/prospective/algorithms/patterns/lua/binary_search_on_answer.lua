--[[
Binary Search on Answer Template

Used when the answer space is monotonic (e.g., min capacity, max speed).
1. Define search space [low, high].
2. Check feasibility of mid.
3. Adjust range based on feasibility.
--]]
-- === MEMO START ===
function check(x)
    -- Implementation depends on problem
    return true
end

function solve_binary_search(low, high)
    local ans = high
    
    while low <= high do
        local mid = math.floor((low + high) / 2)
        if check(mid) then
            ans = mid
            high = mid - 1 -- Try smaller
        else
            low = mid + 1
        end
    end
    
    return ans
end

