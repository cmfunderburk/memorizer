/*
Iterative Binary Search

Time Complexity: O(log n)
Space Complexity: O(1)

Returns the index of target in sorted array arr, or -1 if not found.
*/
// === MEMO START ===
int binary_search(int *arr, int n, int target) {
    int low = 0;
    int high = n - 1;

    while (low <= high) {
        int mid = (low + high) / 2;
        if (arr[mid] == target) {
            return mid;
        } else if (arr[mid] < target) {
            low = mid + 1;
        } else {
            high = mid - 1;
        }
    }

    return -1;
}

