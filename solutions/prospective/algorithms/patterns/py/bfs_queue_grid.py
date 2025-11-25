"""
BFS on Grid (Queue) Template

Shortest path in unweighted grid.
- Use collections.deque for O(1) pops.
- Track visited to avoid cycles.
"""
=== MEMO START ===
from collections import deque

def bfs_grid(grid, start_r, start_c):
    rows, cols = len(grid), len(grid[0])
    q = deque([(start_r, start_c, 0)]) # r, c, dist
    visited = set([(start_r, start_c)])
    
    directions = [(0,1), (0,-1), (1,0), (-1,0)]
    
    while q:
        r, c, dist = q.popleft()
        
        # if (r, c) is target: return dist
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if (0 <= nr < rows and 0 <= nc < cols and 
                (nr, nc) not in visited and grid[nr][nc] != '#'):
                
                visited.add((nr, nc))
                q.append((nr, nc, dist + 1))
                
    return -1

