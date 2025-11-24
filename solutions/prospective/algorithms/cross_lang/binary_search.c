/*
Binary Search (Iterative)

Time Complexity: O(log n)
Space Complexity: O(1)

Returns index of target in sorted array arr of size n, or -1.
*/
=== MEMO START ===
int binary_search(int arr[], int n, int target) {
    int low = 0;
    int high = n - 1;
    
    while (low <= high) {
        int mid = low + (high - low) / 2;
        
        if (arr[mid] == target)
            return mid;
        
        if (arr[mid] < target)
            low = mid + 1;
        else
            high = mid - 1;
    }
    return -1;
}

