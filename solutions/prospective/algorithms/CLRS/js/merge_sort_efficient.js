/**
 * Merge Sort (Efficient Indices)
 * 
 * Time Complexity: O(n log n)
 * Space Complexity: O(n)
 * 
 * Avoids slicing overhead by passing indices and using a single temp array.
 */
// === MEMO START ===
function merge(arr, temp, left, mid, right) {
    let i = left;
    let j = mid + 1;
    let k = left;

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

    for (let x = left; x <= right; x++) {
        arr[x] = temp[x];
    }
}

function mergeSortHelper(arr, temp, left, right) {
    if (left < right) {
        const mid = Math.floor((left + right) / 2);
        mergeSortHelper(arr, temp, left, mid);
        mergeSortHelper(arr, temp, mid + 1, right);
        merge(arr, temp, left, mid, right);
    }
}

function mergeSort(arr) {
    if (arr.length < 2) {
        return arr;
    }
    const temp = new Array(arr.length).fill(0);
    mergeSortHelper(arr, temp, 0, arr.length - 1);
    return arr;
}

