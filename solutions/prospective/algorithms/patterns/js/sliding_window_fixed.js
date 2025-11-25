/**
 * Fixed Sliding Window Template
 * 
 * Used for finding something in a subarray of fixed size k.
 * 1. Initialize window with first k elements.
 * 2. Slide window one step at a time (add new, remove old).
 */
// === MEMO START ===
function slidingWindowFixed(arr, k) {
    if (arr.length < k) {
        return 0;
    }
    
    // Initial window
    let currentSum = 0;
    for (let i = 0; i < k; i++) {
        currentSum += arr[i];
    }
    let maxSum = currentSum;
    
    // Slide
    for (let i = 0; i < arr.length - k; i++) {
        currentSum = currentSum - arr[i] + arr[i + k];
        maxSum = Math.max(maxSum, currentSum);
    }
    
    return maxSum;
}

