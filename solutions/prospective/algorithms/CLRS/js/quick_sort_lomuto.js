/**
 * Quicksort (Lomuto Partition)
 * 
 * Time Complexity: O(n log n) avg, O(n^2) worst
 * Space Complexity: O(log n) stack
 * 
 * In-place sorting using divide and conquer.
 */
// === MEMO START ===
function partition(arr, low, high) {
    const pivot = arr[high];
    let i = low - 1;

    for (let j = low; j < high; j++) {
        if (arr[j] < pivot) {
            i++;
            [arr[i], arr[j]] = [arr[j], arr[i]];
        }
    }
    [arr[i + 1], arr[high]] = [arr[high], arr[i + 1]];
    return i + 1;
}

function quickSort(arr, low, high) {
    if (low < high) {
        const p = partition(arr, low, high);
        quickSort(arr, low, p - 1);
        quickSort(arr, p + 1, high);
    }
}

