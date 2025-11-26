# MEMORIZER

MEMORIZER is a single-user CLI for practicing code recall. You write solution files in Markdown with fenced code blocks as memorization targets. MEMORIZER opens an attempt file in your editor, you type the code from memory, and it prints strict line + character diffs with ANSI coloring.

## Requirements
- Python 3.10+
- A terminal editor discoverable via `$VISUAL`, `$EDITOR`, or one of `nvim`, `vim`, `vi`
- Optional: `fzf` for fast fuzzy-finding file selection

## Solution File Format

Solutions are Markdown files (`.md`) where fenced code blocks are the memorization targets:

```markdown
# Insertion Sort

**Time:** O(n²)  |  **Space:** O(1)

## How It Works

Builds sorted array one element at a time. For each element, shift larger 
elements right until we find where it belongs, then insert.

## Implementation

```python
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i
        while j > 0 and arr[j-1] > key:
            arr[j] = arr[j-1]
            j -= 1
        arr[j] = key
    return arr
```

## When to Use

- Small datasets
- Nearly-sorted data
```

The prose outside code blocks provides context (visible while typing). The code inside fenced blocks is what you must reproduce from memory.

### Multiple Code Blocks

Solutions can have multiple code blocks. Each is a separate target:

```markdown
# Merge Sort

## Implementation

```python
def merge(left, right):
    # ... merge function
```

```python
def merge_sort(arr):
    # ... recursive function
```
```

You must reproduce all blocks correctly for perfect recall.

### Informational Blocks

To include code blocks that shouldn't be memorized (example output, usage), prefix with `<!-- INFO -->`:

```markdown
## Example Usage

<!-- INFO -->
```bash
$ python sort.py
[1, 2, 3, 4, 5]
```
```

## Usage

### Basic Usage
```bash
# Direct file selection
python3 memorizer.py solutions/focus/insertion_sort.md

# Interactive selection (fzf if available, else nested navigation)
python3 memorizer.py

# View attempt history for a solution
python3 memorizer.py solutions/focus/insertion_sort.md --stats

# Focus mode: drill all solutions in solutions/focus/ in random order
python3 memorizer.py --focus
```

### Interactive Selection

When invoked without a solution path, MEMORIZER uses:

1. **fzf** (if installed): Fuzzy-find any solution file instantly with type-ahead search
2. **Nested navigation**: Browse directories interactively with numbered menus

### The Workflow

1. A new attempt file is created under `attempts/` with `.attempt.md` extension (e.g., `insertion_sort-3.attempt.md`).
2. The attempt file is pre-filled with the solution's Markdown, but code blocks show placeholders like `[BLOCK 1] python - 9 lines`.
3. Your editor opens; replace placeholders with code from memory, save, and quit.
4. MEMORIZER compares each block against the solution and prints:
   - Per-block accuracy scores
   - Inline character-level highlights for errors (red = missing, green = extra)
   - Document score = minimum block score
5. If not perfect, you're prompted: `[Y(retry)/n(stop)/p(peek)]`
   - **Y** or Enter: Create a new attempt and retry
   - **n**: Stop and exit
   - **p**: Peek at the solution blocks in your pager, then retry
6. Exit codes: `0` for perfect recall, `1` for stopped, `2` for quit/errors.

### Scoring

- Each code block is scored independently (line accuracy %)
- Document score = minimum of all block scores
- Perfect recall requires 100% on every block

## Stats Mode

Track your progress over time:

```bash
python3 memorizer.py solutions/focus/merge_sort.md --stats
```

Output shows:
- Attempt number and date for each historical attempt
- Accuracy percentages
- Current streak of perfect attempts

## Focus Mode

Drill all solutions in `solutions/focus/` in random order:

```bash
python3 memorizer.py --focus
```

Progress through each solution. After perfect recall, continue to the next or quit.

## Configuration

MEMORIZER respects standard environment variables:
- `$VISUAL` or `$EDITOR`: Your preferred text editor
- `$PAGER`: Viewer for peek mode (defaults to `less -r`)

## Repository Layout
```
memorizer.py                  # single-file CLI implementation
solutions/                    # canonical snippets in Markdown format
  focus/                      # solutions for --focus mode drilling
  new_format/                 # additional solutions
  algorithms/
    CLRS/
    leetcode/
  econ/
  prospective/                # solutions not yet converted/active
attempts/                     # auto-created attempt files (.gitignored)
docs/
  planning/CURRENT/           # feature proposals and design docs
README.md
```

## Example Session

```bash
$ python3 memorizer.py solutions/focus/merge_sort.md

# Editor opens attempts/merge_sort-1.attempt.md with:
#
# # Merge Sort
# 
# **Time:** O(n log n)  |  **Space:** O(n)
# 
# ## Implementation
# 
# ```python
# [BLOCK 1] python - 13 lines
# ```
# 
# ```python
# [BLOCK 2] python - 7 lines
# ```

# You replace placeholders with code from memory, save, quit

========================================
MEMORIZATION CHECK: merge_sort.md
Attempt: merge_sort-1.attempt.md
========================================

BLOCK 1 (python, 13 lines):  ✓ 100.0%

BLOCK 2 (python, 7 lines):   ✗ 85.7%

   -   5  left = merge_sort(arr[:mid])
   +   5  left = mergesort(arr[:mid])

========================================
DOCUMENT SCORE: 85.7% (min of 2 blocks)
========================================

Action? [Y(retry)/n(stop)/p(peek)]
```

## Creating Solution Files

1. Create a `.md` file in `solutions/`
2. Write explanatory prose (context you'll see while typing)
3. Add fenced code blocks for content to memorize
4. Optionally mark informational blocks with `<!-- INFO -->`

Example template:

```markdown
# Algorithm Name

**Time:** O(?)  |  **Space:** O(?)

## How It Works

Brief explanation of the algorithm.

## Implementation

```python
def algorithm():
    pass
```

## When to Use

- Use case 1
- Use case 2
```
