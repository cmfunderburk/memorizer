"""
Binary Search on Answer Template

Used when the answer space is monotonic (e.g., min capacity, max speed).
1. Define search space [low, high].
2. Check feasibility of mid.
3. Adjust range based on feasibility.
"""
=== MEMO START ===
def check(x):
    # Implementation depends on problem
    return True

def solve_binary_search(low, high):
    ans = high
    
    while low <= high:
        mid = (low + high) // 2
        if check(mid):
            ans = mid
            high = mid - 1 # Try smaller
        else:
            low = mid + 1
            
    return ans

