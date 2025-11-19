# MEMORIZER AI Instructions

## Project Overview
MEMORIZER is a single-file Python CLI (`memorize.py`) for practicing code/text recall. It compares user input (typed in a terminal editor) against canonical solutions, providing strict line-by-line and character-level diffs.

## Architecture & Core Components
- **Entry Point**: `memorize.py` contains all logic (CLI parsing, file I/O, diffing, rendering).
- **Data Flow**:
  1. **Input**: User selects a file from `solutions/`.
  2. **Process**: Tool creates an incremental file in `attempts/` (e.g., `poem-1.txt`), opens it in `$EDITOR`.
  3. **Comparison**: After editor close, compares `attempts/` file vs `solutions/` file using `difflib`.
  4. **Output**: Prints ANSI-colored diff to stdout AND appends it to the attempt file.
- **Directories**:
  - `solutions/`: Canonical source files (read-only).
  - `attempts/`: User practice files (write-only, gitignored).

## Critical Workflows

### Running the Tool
```bash
python3 memorize.py solutions/insertion_sort.py
# Or relative paths (resolves to solutions/ automatically)
python3 memorize.py insertion_sort.py
```

### Testing & Verification
There is no automated test suite (`pytest`, etc.). Testing is manual or script-based using `tee` to simulate editor input.

**Simulate Perfect Recall (Pass):**
```bash
# Pipes solution content directly into the attempt file
cat solutions/poem.txt | EDITOR="tee" python3 memorize.py solutions/poem.txt
```

**Simulate Failure:**
```bash
# Writes partial content to simulate memory errors
echo "partial content" | EDITOR="tee" python3 memorize.py solutions/poem.txt
```

### Development Standards
- **Dependencies**: Standard library ONLY. No `pip install`.
- **Type Hinting**: Use `typing` (e.g., `Sequence`, `Path`, `Protocol`) for all function signatures.
- **Path Handling**: Use `pathlib.Path` exclusively.
- **Output**: Must support `TeeWriter` pattern to write to both `sys.stdout` and the attempt file simultaneously.

## Key Implementation Details
- **Path Resolution**: `validate_solution_path` attempts to resolve paths relative to CWD, script root, and `solutions/` dir.
- **Diff Logic**: `compute_line_diff` uses `difflib.SequenceMatcher(autojunk=False)` for strict comparison.
- **ANSI Codes**: Hardcoded ANSI escape sequences are used for coloring.
- **Editor Detection**: Checks `$VISUAL`, `$EDITOR`, then falls back to `nvim`/`vim`/`vi`.

## Common Patterns
- **Error Handling**: Use `die(msg, code=2)` for fatal errors.
- **File Operations**: Always specify `encoding="utf-8"`.
- **Atomic Writes**: Attempt files are created with `open("x")` to prevent race conditions/overwrites.
