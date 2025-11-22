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

def merge_sort(arr):
    if len(arr) < 2:
        return arr
    mid = len(arr) // 2
    L = merge_sort(arr[:mid])
    R = merge_sort(arr[mid:])
    return merge(L, R)
