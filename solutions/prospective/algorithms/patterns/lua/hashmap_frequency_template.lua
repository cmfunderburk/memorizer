--[[
HashMap Frequency Template

Standard counting pattern using Lua tables.
Often the first step in anagrams, most frequent elements, etc.
--]]
-- === MEMO START ===
function count_frequencies(nums)
    local counts = {}
    for _, num in ipairs(nums) do
        counts[num] = (counts[num] or 0) + 1
    end
    return counts
end

