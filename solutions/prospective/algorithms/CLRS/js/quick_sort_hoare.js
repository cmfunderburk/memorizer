/**
 * Quicksort (Hoare Partition)
 * 
 * Time Complexity: O(n log n) avg
 * Space Complexity: O(log n) stack
 * 
 * Hoare's partition is generally more efficient than Lomuto's (fewer swaps).
 */
// === MEMO START ===
function partition(arr, low, high) {
    const pivot = arr[low];
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

