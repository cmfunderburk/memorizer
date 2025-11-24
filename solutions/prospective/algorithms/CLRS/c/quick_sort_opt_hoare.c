/*
Quicksort (Optimized Hoare)

Improvements:
1. Median-of-Three pivot (fixes O(n^2) on sorted arrays).
2. Uses Hoare partition (3x fewer swaps than Lomuto).
*/
// === MEMO START ===
int median_of_three(int *arr, int low, int high) {
    int mid = (low + high) / 2;
    if (arr[low] > arr[mid]) {
        int temp = arr[low]; arr[low] = arr[mid]; arr[mid] = temp;
    }
    if (arr[low] > arr[high]) {
        int temp = arr[low]; arr[low] = arr[high]; arr[high] = temp;
    }
    if (arr[mid] > arr[high]) {
        int temp = arr[mid]; arr[mid] = arr[high]; arr[high] = temp;
    }

    // Median is now at mid; swap with low to use as pivot
    int temp = arr[mid];
    arr[mid] = arr[low];
    arr[low] = temp;
    return arr[low];
}

int partition(int *arr, int low, int high) {
    int pivot = median_of_three(arr, low, high);
    int i = low - 1;
    int j = high + 1;

    while (1) {
        do {
            i++;
        } while (arr[i] < pivot);

        do {
            j--;
        } while (arr[j] > pivot);

        if (i >= j) {
            return j;
        }

        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}

void quick_sort(int *arr, int low, int high) {
    if (low < high) {
        int p = partition(arr, low, high);
        quick_sort(arr, low, p);
        quick_sort(arr, p + 1, high);
    }
}

