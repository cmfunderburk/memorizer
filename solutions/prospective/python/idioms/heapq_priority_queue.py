"""
Heapq Usage (Min-Heap)

- heapify: O(n)
- heappush: O(log n)
- heappop: O(log n)
"""
=== MEMO START ===
import heapq

data = [5, 7, 9, 1, 3]
heapq.heapify(data) # Transform list into heap in-place

heapq.heappush(data, 4)
smallest = heapq.heappop(data)
n_smallest = heapq.nsmallest(3, data)
n_largest = heapq.nlargest(3, data)

