/*
Fixed Sliding Window Template

Used for finding something in a subarray of fixed size k.
1. Initialize window with first k elements.
2. Slide window one step at a time (add new, remove old).
*/
// === MEMO START ===
int sliding_window_fixed(int *arr, int n, int k) {
    if (n < k) return 0;

    int current_sum = 0;
    for (int i = 0; i < k; i++) {
        current_sum += arr[i];
    }
    
    int max_sum = current_sum;

    for (int i = 0; i < n - k; i++) {
        current_sum = current_sum - arr[i] + arr[i + k];
        if (current_sum > max_sum) {
            max_sum = current_sum;
        }
    }

    return max_sum;
}

