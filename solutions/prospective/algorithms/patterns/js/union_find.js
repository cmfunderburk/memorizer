/**
 * Union-Find (Disjoint Set Union) Template
 * 
 * Efficiently tracks connected components.
 * - find(x): returns representative of x (with path compression).
 * - union(x, y): merges sets containing x and y (with rank/size).
 */
// === MEMO START ===
class UnionFind {
    constructor(n) {
        this.parent = Array.from({length: n}, (_, i) => i);
        this.rank = new Array(n).fill(1);
    }
    
    find(x) {
        if (x !== this.parent[x]) {
            this.parent[x] = this.find(this.parent[x]);
        }
        return this.parent[x];
    }
    
    union(x, y) {
        let rootX = this.find(x);
        let rootY = this.find(y);
        
        if (rootX !== rootY) {
            if (this.rank[rootX] < this.rank[rootY]) {
                [rootX, rootY] = [rootY, rootX];
            }
            this.parent[rootY] = rootX;
            this.rank[rootX] += this.rank[rootY];
            return true;
        }
        return false;
    }
}

