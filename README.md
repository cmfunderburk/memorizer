# MEMORIZER

MEMORIZER is a single-user CLI for practicing code or text recall. It opens an empty attempt file in your terminal editor, lets you re-type a canonical solution from memory, and then prints strict line + character diffs with ANSI coloring.

## Requirements
- Python 3.10+
- A terminal editor discoverable via `$VISUAL`, `$EDITOR`, or one of `nvim`, `vim`, `vi`
- Optional: `fzf` for fast fuzzy-finding file selection

## Usage

### Basic Usage
```bash
# Direct file selection
python3 memorizer.py solutions/algorithms/CLRS/insertion_sort.py
python3 memorizer.py insertion_sort.py        # also works; resolved relative to solutions/
python3 memorizer.py ../some/other/file.txt   # arbitrary readable file paths allowed

# Interactive selection (fzf if available, else nested navigation)
python3 memorizer.py

# View attempt history for a solution
python3 memorizer.py solutions/insertion_sort.py --stats
```

### Interactive Selection

When invoked without a solution path, MEMORIZER uses:

1. **fzf** (if installed): Fuzzy-find any solution file instantly with type-ahead search
2. **Nested navigation**: Browse directories interactively with numbered menus
   - Enter a number or exact filename to select
   - Navigate into directories, use `..` to go back
   - Files display without trailing `/`, directories with `/`

### The Workflow
1. A new attempt file is created under `attempts/` with incremental numbering (e.g., `insertion_sort-3.py`).
2. Your editor opens the attempt file; type the solution from memory and quit the editor.
3. MEMORIZER compares the attempt against the canonical file and prints:
   - Full diff with strict whitespace sensitivity.
   - Inline character-level highlights (red background = missing/incorrect, green = extra text).
   - Summary statistics (lines, inserts/deletes, line & character accuracy).
4. If not perfect, you're prompted: `[Y(retry)/n(stop)/p(peek)]`
   - **Y** or Enter: Create a new attempt and retry
   - **n**: Stop and exit with code 1
   - **p**: Peek at the solution in your pager (e.g., `less`), then retry with new attempt
5. The rendered MEMORIZATION CHECK + SUMMARY block is appended to the attempt file so you can review scores later.
6. Exit codes: `0` for perfect matches, `1` for differences, `2` for errors.

Attempt files are never deleted—each run archives a permanent record in `attempts/` for future review.

### Context Marker

Solution files can include a context section that gets pre-filled into attempts but isn't graded. Add `=== MEMO START ===` on a line by itself:

```python
# insertion_sort.py
"""Insertion sort from CLRS Chapter 2."""

def insertion_sort(arr):
    # Implementation details...
    pass

=== MEMO START ===

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr
```

Everything before the marker is pre-filled context; only content after is compared against your attempt.

## Stats Mode

Track your progress over time with the `--stats` flag:

```bash
python3 memorizer.py insertion_sort.py --stats
```

Output shows:
- Attempt number and date for each historical attempt
- Line and character accuracy percentages
- Current streak of perfect (100% line accuracy) attempts

Stats are parsed from the appended summary blocks in attempt files.

## Editor Detection
Preference order: `$VISUAL` → `$EDITOR` → `nvim` → `vim` → `vi`. If no editor is available, the CLI exits with code `2` and instructs you to set an editor.

## Configuration

MEMORIZER respects standard environment variables:
- `$VISUAL` or `$EDITOR`: Your preferred text editor
- `$PAGER`: Viewer for peek mode (defaults to `less -r`)

## Repository Layout
```
memorizer.py                  # single-file CLI implementation (~787 lines)
solutions/                    # canonical snippets, organized hierarchically
  algorithms/
    CLRS/                     # algorithms from CLRS textbook
    leetcode/
      easy/
      medium/
  econ/                       # economics problems/models
  other/
attempts/                     # auto-created, incrementally numbered attempt files (.gitignored)
docs/
  planning/CURRENT/           # feature proposals and design docs
  review/                     # code reviews from AI models
README.md                     # this file
```

## Example Session

```bash
$ python3 memorizer.py
Using nested navigation (install fzf for faster selection)
Current directory: .
  1. algorithms/
  2. econ/
  3. other/

Select a solution (number or name): 1

Current directory: algorithms
  1. ..
  2. CLRS/
  3. leetcode/

Select a solution (number or name): 2

Current directory: algorithms/CLRS
  1. ..
  2. insertion_sort.py
  3. merge_sort.py
  4. quicksort_new.py

Select a solution (number or name): 2

# Editor opens attempts/insertion_sort-15.py
# You type from memory, save, and quit

========================================
MEMORIZATION CHECK: insertion_sort.py
Attempt: insertion_sort-15.py
========================================
    1  def insertion_sort(arr):
    2      for i in range(1, len(arr)):
    3          key = arr[i]
-   4          j = i - 1
+   4          idx = i - 1
    5          while j >= 0 and arr[j] > key:
    6              arr[j + 1] = arr[j]
    7              j -= 1
    8          arr[j + 1] = key
    9      return arr
========================================

SUMMARY
========================================
Total lines (expected):      9
Total lines (yours):         9
Matching lines:              8
Changed lines:               1
Inserted lines:              0
Deleted lines:               0

Line accuracy:            88.9% (8/9)
Character accuracy:       97.4% (150/154)
========================================

Action? [Y(retry)/n(stop)/p(peek)]
```

## Testing

For non-interactive testing, use `tee` as the editor:

```bash
# Perfect recall test
cat solutions/insertion_sort.py | EDITOR=/usr/bin/tee python3 memorizer.py insertion_sort.py
echo $?  # Should be 0

# Partial recall test
printf 'def foo():\n    pass\n' | EDITOR=/usr/bin/tee python3 memorizer.py insertion_sort.py
echo $?  # Should be 1
```
