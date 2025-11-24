"""
Union-Find (Disjoint Set Union) Template

Efficiently tracks connected components.
- find(x): returns representative of x (with path compression).
- union(x, y): merges sets containing x and y (with rank/size).
"""
=== MEMO START ===
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [1] * n
        
    def find(self, x):
        if x != self.parent[x]:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        rootX = self.find(x)
        rootY = self.find(y)
        
        if rootX != rootY:
            if self.rank[rootX] < self.rank[rootY]:
                rootX, rootY = rootY, rootX
            self.parent[rootY] = rootX
            self.rank[rootX] += self.rank[rootY]
            return True
        return False

