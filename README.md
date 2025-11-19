# MEMORIZER

MEMORIZER is a single-user CLI for practicing code or text recall. It opens an empty attempt file in your terminal editor, lets you re-type a canonical solution from memory, and then prints strict line + character diffs with ANSI coloring.

## Requirements
- Python 3.8+
- A terminal editor discoverable via `$VISUAL`, `$EDITOR`, or one of `nvim`, `vim`, `vi`

## Usage
```bash
python3 memorize.py solutions/insertion_sort.py
python3 memorize.py insertion_sort.py        # also works; resolved relative to solutions/
python3 memorize.py ../some/other/file.txt   # arbitrary readable file paths allowed
```

The workflow:
1. A new attempt file is created under `attempts/` with incremental numbering (e.g., `poem-3.txt`).
2. Your editor opens the attempt file; type the solution from memory and quit the editor.
3. MEMORIZER compares the attempt against the canonical file and prints:
   - Full diff with strict whitespace sensitivity.
   - Inline character-level highlights (red background = missing/incorrect, green = extra text).
   - Summary statistics (lines, inserts/deletes, line & character accuracy).
4. The rendered MEMORIZATION CHECK + SUMMARY block is appended to the attempt file so you can review scores later without re-running the CLI.
5. Exit codes communicate the result: `0` for perfect matches, `1` for differences, `2` for errors.

Attempt files are never deleted—each run archives a permanent record in `attempts/` for future review.

## Editor Detection
Preference order: `$VISUAL` → `$EDITOR` → `nvim` → `vim` → `vi`. If no editor is available, the CLI exits with code `2` and instructs you to set an editor.

## Manual Verification
The following manual scenarios were exercised:
- **Perfect recall**: piped the canonical `poem.txt` contents through `/usr/bin/tee` (acting as the editor) and confirmed a 100% score and exit code `0`.
- **Missing lines**: repeated the run but supplied only the first two lines; the report showed deleted lines with red highlights and the process exited with code `1`.

For additional testing, repeat commands such as:
```bash
# Simulate editor input via tee (useful for non-interactive checks)
printf 'line1\nline2\n' | EDITOR=/usr/bin/tee python3 memorize.py solutions/poem.txt
```

## Repository Layout
```
memorize.py        # single-file CLI implementation
solutions/         # canonical snippets
attempts/          # auto-created, incrementally numbered attempt files (.gitignored)
README.md          # this file
```
