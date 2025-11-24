/**
 * Kadane's Algorithm (Maximum Subarray Sum)
 * 
 * Time Complexity: O(n)
 * Space Complexity: O(1)
 * 
 * Finds the contiguous subarray which has the largest sum.
 */
// === MEMO START ===
function maxSubarray(nums) {
    let maxSoFar = nums[0];
    let currentMax = nums[0];

    for (let i = 1; i < nums.length; i++) {
        currentMax = Math.max(nums[i], currentMax + nums[i]);
        maxSoFar = Math.max(maxSoFar, currentMax);
    }

    return maxSoFar;
}

