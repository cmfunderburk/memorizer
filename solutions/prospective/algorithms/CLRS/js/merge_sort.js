/**
 * Merge Sort
 * 
 * Time Complexity: O(n log n)
 * Space Complexity: O(n)
 * 
 * Divide and conquer algorithm. Guaranteed O(n log n) performance.
 */
// === MEMO START ===
function merge(L, R) {
    const merged = [];
    let i = 0;
    let j = 0;

    while (i < L.length && j < R.length) {
        if (L[i] <= R[j]) {
            merged.push(L[i]);
            i++;
        } else {
            merged.push(R[j]);
            j++;
        }
    }
    while (i < L.length) {
        merged.push(L[i]);
        i++;
    }
    while (j < R.length) {
        merged.push(R[j]);
        j++;
    }
    return merged;
}

function mergeSort(arr) {
    if (arr.length < 2) {
        return arr;
    }
    const mid = Math.floor(arr.length / 2);
    const L = mergeSort(arr.slice(0, mid));
    const R = mergeSort(arr.slice(mid));
    return merge(L, R);
}

