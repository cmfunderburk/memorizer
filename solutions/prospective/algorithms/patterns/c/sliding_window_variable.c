/*
Variable Sliding Window Template

Used for finding longest/shortest subarray meeting a condition.
1. Expand right pointer.
2. Shrink left pointer while condition is violated.
*/
#include <stdlib.h>
#include <stdbool.h>

// === MEMO START ===
// Assuming values are small positive integers for this example array-based set
#define MAX_VAL 10000

int sliding_window_variable(int *arr, int n) {
    int l = 0;
    int longest = 0;
    bool window_state[MAX_VAL] = {false};

    for (int r = 0; r < n; r++) {
        while (window_state[arr[r]]) {
            window_state[arr[l]] = false;
            l++;
        }
        window_state[arr[r]] = true;
        int current_len = r - l + 1;
        if (current_len > longest) {
            longest = current_len;
        }
    }

    return longest;
}

