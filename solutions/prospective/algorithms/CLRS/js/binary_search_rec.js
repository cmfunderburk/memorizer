/**
 * Recursive Binary Search
 * 
 * Time Complexity: O(log n)
 * Space Complexity: O(log n) due to recursion stack
 * 
 * Returns the index of target in sorted array arr, or -1 if not found.
 */
// === MEMO START ===
function binarySearch(arr, target, low, high) {
    if (low > high) {
        return -1;
    }

    const mid = Math.floor((low + high) / 2);

    if (arr[mid] === target) {
        return mid;
    } else if (arr[mid] < target) {
        return binarySearch(arr, target, mid + 1, high);
    } else {
        return binarySearch(arr, target, low, mid - 1);
    }
}

