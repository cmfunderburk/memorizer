/*
Selection Sort

Time Complexity: O(n^2)
Space Complexity: O(1)

In-place sort that repeatedly finds the minimum element from the unsorted
part and puts it at the beginning.
*/
// === MEMO START ===
void selection_sort(int *arr, int n) {
    for (int i = 0; i < n; i++) {
        int min_idx = i;
        for (int j = i + 1; j < n; j++) {
            if (arr[j] < arr[min_idx]) {
                min_idx = j;
            }
        }

        int temp = arr[i];
        arr[i] = arr[min_idx];
        arr[min_idx] = temp;
    }
}

