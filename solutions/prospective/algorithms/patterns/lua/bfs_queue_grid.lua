--[[
BFS on Grid (Queue) Template

Shortest path in unweighted grid.
- Use table as queue (table.remove(t, 1) is O(n), for O(1) use two-pointer index or linked list).
- Track visited to avoid cycles.
--]]
-- === MEMO START ===
function bfs_grid(grid, start_r, start_c)
    local rows = #grid
    local cols = #grid[1]
    local q = {{r = start_r, c = start_c, dist = 0}}
    local visited = {}
    visited[start_r .. "," .. start_c] = true
    
    local directions = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}}
    
    while #q > 0 do
        local current = table.remove(q, 1)
        local r, c, dist = current.r, current.c, current.dist
        
        -- if r == target_r and c == target_c then return dist end
        
        for _, dir in ipairs(directions) do
            local nr = r + dir[1]
            local nc = c + dir[2]
            
            if nr >= 1 and nr <= rows and nc >= 1 and nc <= cols then
                local key = nr .. "," .. nc
                if not visited[key] and grid[nr][nc] ~= '#' then
                    visited[key] = true
                    table.insert(q, {r = nr, c = nc, dist = dist + 1})
                end
            end
        end
    end
    
    return -1
end

