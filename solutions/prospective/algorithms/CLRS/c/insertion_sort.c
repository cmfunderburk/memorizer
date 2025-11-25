/*
Insertion Sort

Time Complexity: O(n^2)
Space Complexity: O(1)

Builds the sorted array one item at a time. Efficient for small data sets.
*/
// === MEMO START ===
void insertion_sort(int *arr, int n) {
    for (int i = 1; i < n; i++) {
        int key = arr[i];
        int j = i;
        while (j > 0 && arr[j - 1] > key) {
            arr[j] = arr[j - 1];
            j--;
        }
        arr[j] = key;
    }
}

