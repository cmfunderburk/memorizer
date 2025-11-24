/*
Union-Find (Disjoint Set Union) Template

Efficiently tracks connected components.
- find(x): returns representative of x (with path compression).
- union(x, y): merges sets containing x and y (with rank/size).
*/
#include <stdlib.h>
#include <stdbool.h>

// === MEMO START ===
typedef struct {
    int *parent;
    int *rank;
    int n;
} UnionFind;

UnionFind* createUnionFind(int n) {
    UnionFind *uf = (UnionFind *)malloc(sizeof(UnionFind));
    uf->n = n;
    uf->parent = (int *)malloc(n * sizeof(int));
    uf->rank = (int *)malloc(n * sizeof(int));
    
    for (int i = 0; i < n; i++) {
        uf->parent[i] = i;
        uf->rank[i] = 1;
    }
    return uf;
}

int find(UnionFind *uf, int x) {
    if (x != uf->parent[x]) {
        uf->parent[x] = find(uf, uf->parent[x]);
    }
    return uf->parent[x];
}

bool union_sets(UnionFind *uf, int x, int y) {
    int rootX = find(uf, x);
    int rootY = find(uf, y);

    if (rootX != rootY) {
        if (uf->rank[rootX] < uf->rank[rootY]) {
            int temp = rootX; rootX = rootY; rootY = temp;
        }
        uf->parent[rootY] = rootX;
        uf->rank[rootX] += uf->rank[rootY];
        return true;
    }
    return false;
}

void freeUnionFind(UnionFind *uf) {
    free(uf->parent);
    free(uf->rank);
    free(uf);
}

