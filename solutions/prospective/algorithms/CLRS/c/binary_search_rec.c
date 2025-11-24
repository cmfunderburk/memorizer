/*
Recursive Binary Search

Time Complexity: O(log n)
Space Complexity: O(log n) due to recursion stack

Returns the index of target in sorted array arr, or -1 if not found.
*/
// === MEMO START ===
int binary_search(int *arr, int target, int low, int high) {
    if (low > high) {
        return -1;
    }

    int mid = (low + high) / 2;

    if (arr[mid] == target) {
        return mid;
    } else if (arr[mid] < target) {
        return binary_search(arr, target, mid + 1, high);
    } else {
        return binary_search(arr, target, low, mid - 1);
    }
}

