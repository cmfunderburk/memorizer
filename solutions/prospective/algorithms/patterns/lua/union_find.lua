--[[
Union-Find (Disjoint Set Union) Template

Efficiently tracks connected components.
- find(x): returns representative of x (with path compression).
- union(x, y): merges sets containing x and y (with rank/size).
--]]
-- === MEMO START ===
UnionFind = {}
UnionFind.__index = UnionFind

function UnionFind:new(n)
    local obj = {
        parent = {},
        rank = {}
    }
    for i = 1, n do
        obj.parent[i] = i
        obj.rank[i] = 1
    end
    setmetatable(obj, self)
    return obj
end

function UnionFind:find(x)
    if x ~= self.parent[x] then
        self.parent[x] = self:find(self.parent[x])
    end
    return self.parent[x]
end

function UnionFind:union(x, y)
    local rootX = self:find(x)
    local rootY = self:find(y)
    
    if rootX ~= rootY then
        if self.rank[rootX] < self.rank[rootY] then
            rootX, rootY = rootY, rootX
        end
        self.parent[rootY] = rootX
        self.rank[rootX] = self.rank[rootX] + self.rank[rootY]
        return true
    end
    return false
end

