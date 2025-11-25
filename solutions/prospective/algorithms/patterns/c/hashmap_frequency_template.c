/*
HashMap Frequency Template

Standard counting pattern.
Implementation uses a simple open-addressing hash table.
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
    return 0; // Default value
}

HashMap* count_frequencies(int *nums, int n) {
    HashMap *counts = createHashMap(n * 2); // Simple sizing strategy
    for (int i = 0; i < n; i++) {
        int current_count = get(counts, nums[i]);
        put(counts, nums[i], current_count + 1);
    }
    return counts;
}

