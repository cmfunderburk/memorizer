/**
 * Two Pointers Template
 * 
 * Common pattern for sorted arrays (e.g., 2Sum II) or checking palindromes.
 * - Left starts at 0, Right starts at len-1.
 * - Move pointers based on condition.
 */
// === MEMO START ===
function twoPointers(arr, target) {
    let l = 0;
    let r = arr.length - 1;
    
    while (l < r) {
        const currentSum = arr[l] + arr[r];
        if (currentSum === target) {
            return [l, r];
        } else if (currentSum < target) {
            l++;
        } else {
            r--;
        }
    }
    return [];
}

