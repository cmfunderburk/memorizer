/*
Kadane's Algorithm (Maximum Subarray Sum)

Time Complexity: O(n)
Space Complexity: O(1)

Finds the contiguous subarray which has the largest sum.
*/
// === MEMO START ===
int max_subarray(int *nums, int n) {
    int max_so_far = nums[0];
    int current_max = nums[0];

    for (int i = 1; i < n; i++) {
        if (nums[i] > current_max + nums[i]) {
            current_max = nums[i];
        } else {
            current_max = current_max + nums[i];
        }
        
        if (current_max > max_so_far) {
            max_so_far = current_max;
        }
    }

    return max_so_far;
}

