/**
 * Max-Heapify
 * 
 * Time Complexity: O(log n)
 * Space Complexity: O(1) or O(log n) recursive
 * 
 * Maintains the max-heap property for a subtree rooted at index i.
 * Assumes binary tree structure in array.
 */
// === MEMO START ===
function maxHeapify(arr, n, i) {
    let largest = i;
    const left = 2 * i + 1;
    const right = 2 * i + 2;

    if (left < n && arr[left] > arr[largest]) {
        largest = left;
    }

    if (right < n && arr[right] > arr[largest]) {
        largest = right;
    }

    if (largest !== i) {
        [arr[i], arr[largest]] = [arr[largest], arr[i]];
        maxHeapify(arr, n, largest);
    }
}

