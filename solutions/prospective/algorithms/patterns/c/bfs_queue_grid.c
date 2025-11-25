/*
BFS on Grid (Queue) Template

Shortest path in unweighted grid.
- Use a Queue for FIFO.
- Track visited to avoid cycles.
*/
#include <stdlib.h>
#include <stdbool.h>

// === MEMO START ===
typedef struct {
    int r;
    int c;
    int dist;
} Node;

typedef struct {
    Node *data;
    int front;
    int rear;
    int capacity;
} Queue;

Queue* createQueue(int capacity) {
    Queue *q = (Queue *)malloc(sizeof(Queue));
    q->capacity = capacity;
    q->front = 0;
    q->rear = 0;
    q->data = (Node *)malloc(capacity * sizeof(Node));
    return q;
}

void enqueue(Queue *q, int r, int c, int dist) {
    if (q->rear == q->capacity) return; // Full
    q->data[q->rear].r = r;
    q->data[q->rear].c = c;
    q->data[q->rear].dist = dist;
    q->rear++;
}

Node dequeue(Queue *q) {
    return q->data[q->front++];
}

bool isEmpty(Queue *q) {
    return q->front == q->rear;
}

int bfs_grid(char **grid, int rows, int cols, int start_r, int start_c) {
    Queue *q = createQueue(rows * cols);
    bool **visited = (bool **)malloc(rows * sizeof(bool *));
    for (int i = 0; i < rows; i++) {
        visited[i] = (bool *)calloc(cols, sizeof(bool));
    }

    enqueue(q, start_r, start_c, 0);
    visited[start_r][start_c] = true;

    int dr[] = {0, 0, 1, -1};
    int dc[] = {1, -1, 0, 0};

    while (!isEmpty(q)) {
        Node current = dequeue(q);
        int r = current.r;
        int c = current.c;
        int dist = current.dist;

        // if (r, c) is target: return dist;
        
        for (int i = 0; i < 4; i++) {
            int nr = r + dr[i];
            int nc = c + dc[i];

            if (nr >= 0 && nr < rows && nc >= 0 && nc < cols &&
                !visited[nr][nc] && grid[nr][nc] != '#') {
                
                visited[nr][nc] = true;
                enqueue(q, nr, nc, dist + 1);
            }
        }
    }

    // Cleanup
    for (int i = 0; i < rows; i++) free(visited[i]);
    free(visited);
    free(q->data);
    free(q);

    return -1;
}

