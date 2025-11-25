/**
 * BFS on Grid (Queue) Template
 * 
 * Shortest path in unweighted grid.
 * - Use array as queue (shift is O(n), for O(1) use a real Queue class).
 * - Track visited to avoid cycles.
 */
// === MEMO START ===
function bfsGrid(grid, startR, startC) {
    const rows = grid.length;
    const cols = grid[0].length;
    const q = [[startR, startC, 0]]; // r, c, dist
    const visited = new Set([`${startR},${startC}`]);
    
    const directions = [[0, 1], [0, -1], [1, 0], [-1, 0]];
    
    while (q.length > 0) {
        const [r, c, dist] = q.shift();
        
        // if (r, c) is target: return dist
        
        for (const [dr, dc] of directions) {
            const nr = r + dr;
            const nc = c + dc;
            
            if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && 
                !visited.has(`${nr},${nc}`) && grid[nr][nc] !== '#') {
                
                visited.add(`${nr},${nc}`);
                q.push([nr, nc, dist + 1]);
            }
        }
    }
    
    return -1;
}

