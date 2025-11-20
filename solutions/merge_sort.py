def merge(L, R):
    merged = []
    i = 0
    j = 0
    while i < len(L) and j < len(R):
        if L[i] <= R[j]:
            merged.append(L[i])
            i += 1
        else:
            merged.append(R[j])
            j += 1
    while i < len(L):
        merged.append(L[i])
        i += 1
    while j < len(R):
        merged.append(R[j])
        j += 1
    return merged

def merge_sort(A):
    if len(A) < 2:
        return A
    mid = len(A) // 2
    L = merge_sort(A[:mid])
    R = merge_sort(A[mid:])
    return merge(L, R)
