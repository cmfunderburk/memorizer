/**
 * Naive Matrix Multiplication
 * 
 * Time Complexity: O(n^3) for n x n matrices
 * Space Complexity: O(n^2) for result
 * 
 * Multiplies two matrices A and B.
 */
// === MEMO START ===
function matrixMultiply(A, B) {
    const rowsA = A.length;
    const colsA = A[0].length;
    const rowsB = B.length;
    const colsB = B[0].length;

    if (colsA !== rowsB) {
        throw new Error("Incompatible dimensions");
    }

    const C = Array(rowsA).fill().map(() => Array(colsB).fill(0));

    for (let i = 0; i < rowsA; i++) {
        for (let j = 0; j < colsB; j++) {
            for (let k = 0; k < colsA; k++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }

    return C;
}

