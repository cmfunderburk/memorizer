/**
 * Iterative Binary Search
 * 
 * Time Complexity: O(log n)
 * Space Complexity: O(1)
 * 
 * Returns the index of target in sorted array arr, or -1 if not found.
 */
// === MEMO START ===
function binarySearch(arr, target) {
    let low = 0;
    let high = arr.length - 1;

    while (low <= high) {
        const mid = Math.floor((low + high) / 2);
        if (arr[mid] === target) {
            return mid;
        } else if (arr[mid] < target) {
            low = mid + 1;
        } else {
            high = mid - 1;
        }
    }

    return -1;
}

