/**
 * Insertion Sort
 * 
 * Time Complexity: O(n^2)
 * Space Complexity: O(1)
 * 
 * Builds the sorted array one item at a time. Efficient for small data sets.
 */
// === MEMO START ===
function insertionSort(arr) {
    for (let i = 1; i < arr.length; i++) {
        const key = arr[i];
        let j = i;
        while (j > 0 && arr[j - 1] > key) {
            arr[j] = arr[j - 1];
            j--;
        }
        arr[j] = key;
    }
    return arr;
}

