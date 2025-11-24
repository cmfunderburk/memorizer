"""
Collections Defaultdict (List)

Avoids checking if key exists before appending.
"""
=== MEMO START ===
from collections import defaultdict

# Grouping items by key
items = [('a', 1), ('b', 2), ('a', 3), ('c', 4)]
grouped = defaultdict(list)

for key, val in items:
    grouped[key].append(val)
    
# Result: {'a': [1, 3], 'b': [2], 'c': [4]}

