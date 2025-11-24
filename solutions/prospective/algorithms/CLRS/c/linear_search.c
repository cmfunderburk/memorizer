/*
Linear Search

Time Complexity: O(n)
Space Complexity: O(1)

Returns the index of target in arr, or -1 if not found.
*/
// === MEMO START ===
int linear_search(int *arr, int n, int target) {
    for (int i = 0; i < n; i++) {
        if (arr[i] == target) {
            return i;
        }
    }
    return -1;
}

