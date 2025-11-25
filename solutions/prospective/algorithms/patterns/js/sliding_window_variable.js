/**
 * Variable Sliding Window Template
 * 
 * Used for finding longest/shortest subarray meeting a condition.
 * 1. Expand right pointer.
 * 2. Shrink left pointer while condition is violated.
 */
// === MEMO START ===
function slidingWindowVariable(arr) {
    let l = 0;
    let longest = 0;
    const windowState = new Set();
    
    for (let r = 0; r < arr.length; r++) {
        while (windowState.has(arr[r])) {
            windowState.delete(arr[l]);
            l++;
        }
        windowState.add(arr[r]);
        longest = Math.max(longest, r - l + 1);
    }
    
    return longest;
}

