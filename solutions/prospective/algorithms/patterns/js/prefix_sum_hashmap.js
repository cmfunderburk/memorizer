/**
 * Prefix Sum + HashMap Template
 * 
 * Used for finding subarrays with a target sum (e.g. k).
 * - Map stores {prefix_sum: count}
 * - curr_sum - target = old_prefix_sum
 */
// === MEMO START ===
function subarraySum(nums, k) {
    let count = 0;
    let currSum = 0;
    const prefixSums = new Map();
    prefixSums.set(0, 1); // Base case: sum 0 exists once
    
    for (const num of nums) {
        currSum += num;
        const diff = currSum - k;
        
        count += prefixSums.get(diff) || 0;
        prefixSums.set(currSum, (prefixSums.get(currSum) || 0) + 1);
    }
    
    return count;
}

