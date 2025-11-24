"""
Naive Matrix Multiplication

Time Complexity: O(n^3) for n x n matrices
Space Complexity: O(n^2) for result

Multiplies two matrices A and B.
"""
=== MEMO START ===
def matrix_multiply(A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])
    
    if cols_A != rows_B:
        raise ValueError("Incompatible dimensions")
        
    C = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                C[i][j] += A[i][k] * B[k][j]
                
    return C

