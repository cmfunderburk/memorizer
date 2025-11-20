def insertion_sort(A):
    for i in range(1, len(A)):
        key = A[i]
        j = i
        while j > 0 and A[j-1] > key:
            A[j] = A[j-1]
            j -= 1
        A[j] = key
    return A
