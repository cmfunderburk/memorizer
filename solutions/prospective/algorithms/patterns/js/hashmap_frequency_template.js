/**
 * HashMap Frequency Template
 * 
 * Standard counting pattern using object or Map.
 * Often the first step in anagrams, most frequent elements, etc.
 */
// === MEMO START ===
function countFrequencies(nums) {
    const counts = {};
    for (const num of nums) {
        counts[num] = (counts[num] || 0) + 1;
    }
    return counts;
}

// Or using Map:
// function countFrequencies(nums) {
//     const counts = new Map();
//     for (const num of nums) {
//         counts.set(num, (counts.get(num) || 0) + 1);
//     }
//     return counts;
// }

