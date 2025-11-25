/*
Prefix Sum + HashMap Template

Used for finding subarrays with a target sum (e.g. k).
- Map stores {prefix_sum: count}
- curr_sum - target = old_prefix_sum
*/
#include <stdlib.h>

// === MEMO START ===
typedef struct {
    int key;
    int value;
    int occupied;
} HashEntry;

typedef struct {
    HashEntry *table;
    int size;
} HashMap;

HashMap* createHashMap(int size) {
    HashMap *map = (HashMap *)malloc(sizeof(HashMap));
    map->size = size;
    map->table = (HashEntry *)calloc(size, sizeof(HashEntry));
    return map;
}

void put(HashMap *map, int key, int value) {
    int idx = abs(key) % map->size;
    while (map->table[idx].occupied) {
        if (map->table[idx].key == key) {
            map->table[idx].value = value;
            return;
        }
        idx = (idx + 1) % map->size;
    }
    map->table[idx].key = key;
    map->table[idx].value = value;
    map->table[idx].occupied = 1;
}

int get(HashMap *map, int key) {
    int idx = abs(key) % map->size;
    while (map->table[idx].occupied) {
        if (map->table[idx].key == key) {
            return map->table[idx].value;
        }
        idx = (idx + 1) % map->size;
    }
    return 0;
}

int subarray_sum(int *nums, int n, int k) {
    int count = 0;
    int curr_sum = 0;
    HashMap *prefix_sums = createHashMap(n * 2);
    
    put(prefix_sums, 0, 1); // Base case: sum 0 exists once

    for (int i = 0; i < n; i++) {
        curr_sum += nums[i];
        int diff = curr_sum - k;

        count += get(prefix_sums, diff);
        int current_val = get(prefix_sums, curr_sum);
        put(prefix_sums, curr_sum, current_val + 1);
    }

    free(prefix_sums->table);
    free(prefix_sums);
    return count;
}

