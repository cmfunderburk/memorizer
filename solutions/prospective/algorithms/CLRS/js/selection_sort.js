/**
 * Selection Sort
 * 
 * Time Complexity: O(n^2)
 * Space Complexity: O(1)
 * 
 * In-place sort that repeatedly finds the minimum element from the unsorted
 * part and puts it at the beginning.
 */
// === MEMO START ===
function selectionSort(arr) {
    const n = arr.length;
    for (let i = 0; i < n; i++) {
        let minIdx = i;
        for (let j = i + 1; j < n; j++) {
            if (arr[j] < arr[minIdx]) {
                minIdx = j;
            }
        }

        [arr[i], arr[minIdx]] = [arr[minIdx], arr[i]];
    }
    return arr;
}

