/*
DFS on Grid (Recursive) Template

Standard flood fill or island counting pattern.
- Check bounds.
- Check visited/condition.
- Recurse neighbors.
*/
// === MEMO START ===
void dfs(char **grid, int rows, int cols, int r, int c) {
    if (r < 0 || c < 0 || r >= rows || c >= cols || grid[r][c] == '0') {
        return;
    }

    grid[r][c] = '0'; // Mark visited

    dfs(grid, rows, cols, r + 1, c);
    dfs(grid, rows, cols, r - 1, c);
    dfs(grid, rows, cols, r, c + 1);
    dfs(grid, rows, cols, r, c - 1);
}

int num_islands(char **grid, int rows, int cols) {
    if (!grid) return 0;
    int count = 0;

    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < cols; c++) {
            if (grid[r][c] == '1') {
                count++;
                dfs(grid, rows, cols, r, c);
            }
        }
    }

    return count;
}

