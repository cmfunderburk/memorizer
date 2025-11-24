/**
 * Quicksort (Optimized Hoare)
 * 
 * Improvements:
 * 1. Median-of-Three pivot (fixes O(n^2) on sorted arrays).
 * 2. Uses Hoare partition (3x fewer swaps than Lomuto).
 */
// === MEMO START ===
function medianOfThree(arr, low, high) {
    const mid = Math.floor((low + high) / 2);
    if (arr[low] > arr[mid]) [arr[low], arr[mid]] = [arr[mid], arr[low]];
    if (arr[low] > arr[high]) [arr[low], arr[high]] = [arr[high], arr[low]];
    if (arr[mid] > arr[high]) [arr[mid], arr[high]] = [arr[high], arr[mid]];

    // Median is now at mid; swap with low to use as pivot
    [arr[mid], arr[low]] = [arr[low], arr[mid]];
    return arr[low];
}

function partition(arr, low, high) {
    const pivot = medianOfThree(arr, low, high);
    let i = low - 1;
    let j = high + 1;

    while (true) {
        do {
            i++;
        } while (arr[i] < pivot);

        do {
            j--;
        } while (arr[j] > pivot);

        if (i >= j) {
            return j;
        }

        [arr[i], arr[j]] = [arr[j], arr[i]];
    }
}

function quickSort(arr, low, high) {
    if (low < high) {
        const p = partition(arr, low, high);
        quickSort(arr, low, p);
        quickSort(arr, p + 1, high);
    }
}

