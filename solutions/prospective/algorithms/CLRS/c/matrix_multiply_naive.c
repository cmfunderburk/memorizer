/*
Naive Matrix Multiplication

Time Complexity: O(n^3) for n x n matrices
Space Complexity: O(n^2) for result

Multiplies two matrices A and B.
Returns a new dynamically allocated matrix.
*/
#include <stdlib.h>

// === MEMO START ===
int** matrix_multiply(int **A, int rows_A, int cols_A, int **B, int rows_B, int cols_B) {
    if (cols_A != rows_B) {
        return NULL; // Error: Incompatible dimensions
    }

    int **C = (int **)malloc(rows_A * sizeof(int *));
    for (int i = 0; i < rows_A; i++) {
        C[i] = (int *)calloc(cols_B, sizeof(int));
    }

    for (int i = 0; i < rows_A; i++) {
        for (int j = 0; j < cols_B; j++) {
            for (int k = 0; k < cols_A; k++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }

    return C;
}

