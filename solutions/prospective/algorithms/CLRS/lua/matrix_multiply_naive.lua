--[[
Naive Matrix Multiplication

Time Complexity: O(n^3) for n x n matrices
Space Complexity: O(n^2) for result

Multiplies two matrices A and B.
--]]
-- === MEMO START ===
function matrix_multiply(A, B)
    local rows_A = #A
    local cols_A = #A[1]
    local rows_B = #B
    local cols_B = #B[1]
    
    if cols_A ~= rows_B then
        error("Incompatible dimensions")
    end
    
    local C = {}
    for i = 1, rows_A do
        C[i] = {}
        for j = 1, cols_B do
            C[i][j] = 0
            for k = 1, cols_A do
                C[i][j] = C[i][j] + A[i][k] * B[k][j]
            end
        end
    end
    
    return C
end

