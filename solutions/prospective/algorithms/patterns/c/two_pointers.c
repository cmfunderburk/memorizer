/*
Two Pointers Template

Common pattern for sorted arrays (e.g., 2Sum II) or checking palindromes.
- Left starts at 0, Right starts at len-1.
- Move pointers based on condition.
*/
#include <stdlib.h>

// === MEMO START ===
// Returns a heap-allocated array of 2 integers [index1, index2] or NULL if not found
int* two_pointers(int *arr, int n, int target) {
    int l = 0;
    int r = n - 1;
    
    while (l < r) {
        int current_sum = arr[l] + arr[r];
        if (current_sum == target) {
            int *result = (int *)malloc(2 * sizeof(int));
            result[0] = l;
            result[1] = r;
            return result;
        } else if (current_sum < target) {
            l++;
        } else {
            r--;
        }
    }
    return NULL;
}

