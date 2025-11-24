/*
Merge Sort (Efficient Indices)

Time Complexity: O(n log n)
Space Complexity: O(n)

Avoids slicing overhead by passing indices and using a single temp array.
*/
#include <stdlib.h>

// === MEMO START ===
void merge(int *arr, int *temp, int left, int mid, int right) {
    int i = left;
    int j = mid + 1;
    int k = left;

    while (i <= mid && j <= right) {
        if (arr[i] <= arr[j]) {
            temp[k] = arr[i];
            i++;
        } else {
            temp[k] = arr[j];
            j++;
        }
        k++;
    }

    while (i <= mid) {
        temp[k] = arr[i];
        k++;
        i++;
    }
    while (j <= right) {
        temp[k] = arr[j];
        k++;
        j++;
    }

    for (int x = left; x <= right; x++) {
        arr[x] = temp[x];
    }
}

void merge_sort_helper(int *arr, int *temp, int left, int right) {
    if (left < right) {
        int mid = (left + right) / 2;
        merge_sort_helper(arr, temp, left, mid);
        merge_sort_helper(arr, temp, mid + 1, right);
        merge(arr, temp, left, mid, right);
    }
}

void merge_sort(int *arr, int n) {
    if (n < 2) {
        return;
    }
    int *temp = (int *)malloc(n * sizeof(int));
    if (temp != NULL) {
        merge_sort_helper(arr, temp, 0, n - 1);
        free(temp);
    }
}

