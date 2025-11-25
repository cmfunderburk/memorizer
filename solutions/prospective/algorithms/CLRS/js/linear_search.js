/**
 * Linear Search
 * 
 * Time Complexity: O(n)
 * Space Complexity: O(1)
 * 
 * Returns the index of target in arr, or -1 if not found.
 */
// === MEMO START ===
function linearSearch(arr, target) {
    for (let i = 0; i < arr.length; i++) {
        if (arr[i] === target) {
            return i;
        }
    }
    return -1;
}

