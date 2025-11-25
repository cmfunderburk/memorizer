"""
Bisect (Binary Search) Usage

- bisect_left: index to insert before existing equal values (lower bound)
- bisect_right: index to insert after existing equal values (upper bound)
"""
=== MEMO START ===
import bisect

sorted_list = [1, 2, 4, 4, 5]

# Find index to insert 3 to maintain order
idx = bisect.bisect_left(sorted_list, 3)
# bisect.insort(sorted_list, 3) would actually insert it

# Find first occurrence of 4
first_4 = bisect.bisect_left(sorted_list, 4)

# Find insertion point after all 4s
after_4 = bisect.bisect_right(sorted_list, 4)

