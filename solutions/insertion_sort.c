INSERTION-SORT(A, n)
    for i = 2 to n
        key = A[i]
        j = i - 1
        while j > 0 and A[j+1] > A[j]
            A[j+1] = A[j]
            j = j - 1
        A[j+1] = key
