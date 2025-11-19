def insertion_sort(array):
    n = len(array)
    for i in range(1, n):
        j = i
        while j > 0 and array[j-1] > array[j]:
            array[j-1], array[j] = array[j], array[j-1]
            j -= 1
    return array
