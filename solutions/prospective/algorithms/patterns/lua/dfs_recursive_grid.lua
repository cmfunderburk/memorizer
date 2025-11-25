--[[
DFS on Grid (Recursive) Template

Standard flood fill or island counting pattern.
- Check bounds.
- Check visited/condition.
- Recurse neighbors.
--]]
-- === MEMO START ===
function num_islands(grid)
    if #grid == 0 then return 0 end
    local rows = #grid
    local cols = #grid[1]
    local count = 0
    
    local function dfs(r, c)
        if r < 1 or c < 1 or r > rows or c > cols or grid[r][c] == "0" then
            return
        end
        
        grid[r][c] = "0" -- Mark visited
        
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)
    end

    for r = 1, rows do
        for c = 1, cols do
            if grid[r][c] == "1" then
                count = count + 1
                dfs(r, c)
            end
        end
    end
    
    return count
end

