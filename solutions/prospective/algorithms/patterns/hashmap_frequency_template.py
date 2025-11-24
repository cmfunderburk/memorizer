"""
HashMap Frequency Template

Standard counting pattern using dict or Counter.
Often the first step in anagrams, most frequent elements, etc.
"""
=== MEMO START ===
def count_frequencies(nums):
    counts = {}
    for num in nums:
        counts[num] = counts.get(num, 0) + 1
    return counts

# Or manually:
# counts = {}
# for x in s:
#     if x not in counts:
#         counts[x] = 0
#     counts[x] += 1

