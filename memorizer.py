#!/usr/bin/env python3
"""MEMORIZER CLI tool for practicing code recall."""

from __future__ import annotations

import argparse
import io
import os
import random
import re
import shlex
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Literal, NoReturn, Protocol, Sequence

from difflib import SequenceMatcher


# ==========================================================================
# CONSTANTS & CONFIGURATION
# ==========================================================================
BASE_DIR = Path(__file__).resolve().parent
SOLUTIONS_DIR = Path("solutions")
ATTEMPTS_DIR = Path("attempts")
SOLUTIONS_ROOT = BASE_DIR / SOLUTIONS_DIR
FOCUS_DIR = SOLUTIONS_ROOT / "focus"
ATTEMPTS_ROOT = BASE_DIR / ATTEMPTS_DIR
DEFAULT_EDITORS: Sequence[str] = ("nvim", "vim", "vi")
ANSI_RED_BG = "\033[41m"
ANSI_GREEN_BG = "\033[42m"
ANSI_RESET = "\033[0m"
ANSI_BOLD = "\033[1m"
HEADER_RULE = "=" * 40
MEMO_START_MARKER = "=== MEMO START ==="


class Writer(Protocol):
    def write(self, data: str, /) -> int: ...

    def flush(self) -> None: ...


class TeeWriter(io.TextIOBase):
    """Replicate writes across multiple text streams."""

    def __init__(self, *targets: Writer) -> None:
        self._targets = targets

    def write(self, data: str, /) -> int:
        for target in self._targets:
            target.write(data)
        return len(data)

    def flush(self) -> None:
        for target in self._targets:
            if hasattr(target, "flush"):
                target.flush()


def die(message: str, *, code: int = 2) -> NoReturn:
    """Print an error message and exit with the provided code."""
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(code)


# ==========================================================================
# CLI ARGUMENTS
# ==========================================================================

def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Practice recalling canonical snippets by typing them from memory "
            "and reviewing strict diffs."
        )
    )
    parser.add_argument(
        "solution",
        nargs="?",
        help=(
            "Path to the canonical solution file (relative to repo or absolute). "
            "If omitted, interactive selection is used."
        ),
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show progress statistics for the selected solution instead of starting a new attempt.",
    )
    parser.add_argument(
        "--focus",
        action="store_true",
        help="Run drills for every solution under solutions/focus/ in random order.",
    )
    return parser.parse_args(argv)


# ==========================================================================
# FILE / PATH UTILITIES
# ==========================================================================

def validate_solution_path(raw: str) -> Path:
    """Resolve the canonical solution path, supporting relative inputs."""

    def normalize(candidate: Path) -> Path:
        try:
            return candidate.resolve()
        except OSError:
            return candidate.absolute()

    candidates: list[Path] = []
    raw_path = Path(raw).expanduser()

    if raw_path.is_absolute():
        candidates.append(normalize(raw_path))
    else:
        candidates.append(normalize(Path.cwd() / raw_path))
        candidates.append(normalize(BASE_DIR / raw_path))
        candidates.append(normalize(BASE_DIR / SOLUTIONS_DIR / raw_path))

    seen: set[Path] = set()
    for path in candidates:
        if path in seen:
            continue
        seen.add(path)
        if path.is_file():
            try:
                path.open("r", encoding="utf-8").close()
            except OSError as exc:
                die(f"Cannot read solution '{path}': {exc}")
            return path

    search_hint = (SOLUTIONS_ROOT / raw_path.name).resolve()
    die(
        f"Solution '{raw}' not found. Expected an existing file such as '{search_hint}'."
    )


def list_contents(directory: Path) -> List[Path]:
    """List directories and files in the given directory."""
    if not directory.exists():
        return []

    items = [p for p in directory.iterdir() if not p.name.startswith(".")]
    dirs = sorted([p for p in items if p.is_dir()], key=lambda p: p.name)
    files = sorted([p for p in items if p.is_file()], key=lambda p: p.name)
    return dirs + files


def collect_focus_files() -> list[Path]:
    """Return readable, non-hidden files in the focus directory (non-recursive)."""
    if not FOCUS_DIR.exists() or not FOCUS_DIR.is_dir():
        return []

    files: list[Path] = []
    for path in FOCUS_DIR.iterdir():
        if path.name.startswith("."):
            continue
        if path.is_file() and os.access(path, os.R_OK):
            files.append(path.resolve())
    return sorted(files, key=lambda p: p.name.lower())


def _select_nested(start_dir: Path) -> Path:
    """Prompt user to select a solution from the directory structure using nested navigation."""
    current_dir = start_dir.resolve()
    root_dir = SOLUTIONS_ROOT.resolve()

    while True:
        candidates = list_contents(current_dir)
        if not candidates and current_dir == root_dir:
            die(f"No solutions found in {SOLUTIONS_ROOT}")

        # Calculate relative path for display
        try:
            rel_path = current_dir.relative_to(root_dir)
        except ValueError:
            rel_path = current_dir.name

        print(f"{ANSI_BOLD}Current directory: {rel_path}{ANSI_RESET}")
        
        display_list = []
        # Add ".." option if not at root
        if current_dir != root_dir:
            display_list.append(Path(".."))
        
        display_list.extend(candidates)

        for i, path in enumerate(display_list, 1):
            name = path.name + "/" if path.is_dir() and path.name != ".." else path.name
            print(f" {i:2}. {name}")

        try:
            raw = input("\nSelect a solution (number or name): ").strip()
            if not raw:
                continue

            selected = None

            # Try number
            if raw.isdigit():
                idx = int(raw) - 1
                if 0 <= idx < len(display_list):
                    selected = display_list[idx]

            # Try name match
            if not selected:
                for path in display_list:
                    # Match name exactly (handling the .. special case)
                    if path.name == raw:
                        selected = path
                        break
            
            if not selected:
                 print("Invalid selection. Please enter a number or exact filename.")
                 continue

            # Handle Selection
            if selected.name == "..":
                current_dir = current_dir.parent
            elif selected.is_dir():
                current_dir = selected
            else:
                return selected

        except (KeyboardInterrupt, EOFError):
            print()
            sys.exit(130)


def _select_with_fzf(start_dir: Path) -> Path:
    """Use fzf to select a solution file with fuzzy finding."""
    root = SOLUTIONS_ROOT.resolve()
    
    # Collect all solution files
    files = []
    for path in root.rglob("*"):
        if path.is_file() and not path.name.startswith("."):
            try:
                rel = path.relative_to(root)
                files.append((str(rel), path))
            except ValueError:
                continue
    
    if not files:
        die(f"No solutions found in {SOLUTIONS_ROOT}")
    
    # Format for fzf: one path per line
    input_text = "\n".join(rel for rel, _ in files)
    
    # Run fzf with minimal flags
    cmd = ["fzf", "--height=40%", "--reverse"]
    
    try:
        result = subprocess.run(
            cmd,
            input=input_text.encode("utf-8"),
            capture_output=True,
            check=True,
        )
    except subprocess.CalledProcessError:
        # User cancelled (Ctrl-C or Esc)
        raise SystemExit(130)
    except FileNotFoundError:
        # fzf binary not found
        raise ValueError("fzf command not found")
    
    selected_rel = result.stdout.decode("utf-8").strip()
    if not selected_rel:
        raise ValueError("No selection made")
    
    # Find corresponding absolute path
    for rel, abs_path in files:
        if rel == selected_rel:
            return abs_path
    
    raise ValueError(f"Selected path '{selected_rel}' not found")


def interactive_select(start_dir: Path) -> Path:
    """Select a solution file: fzf if available, else nested navigation."""
    if shutil.which("fzf"):
        try:
            return _select_with_fzf(start_dir)
        except (subprocess.SubprocessError, ValueError):
            print("fzf selection failed; using nested navigation")
    else:
        print("Using nested navigation (install fzf for faster selection)")
    return _select_nested(start_dir)


def get_next_attempt_path(solution_path: Path) -> Path:
    """Determine the next numbered attempt filename for the solution."""
    ATTEMPTS_ROOT.mkdir(exist_ok=True)
    basename = solution_path.stem or solution_path.name
    suffix = solution_path.suffix
    pattern = f"{basename}-*{suffix}" if suffix else f"{basename}-*"

    highest = 0
    regex = re.compile(rf"{re.escape(basename)}-(\d+)$")
    for path in ATTEMPTS_ROOT.glob(pattern):
        match = regex.search(path.stem)
        if match:
            highest = max(highest, int(match.group(1)))

    next_number = highest + 1
    return ATTEMPTS_ROOT / f"{basename}-{next_number}{suffix}"


def create_attempt_file(solution_path: Path) -> Path:
    """Create the next attempt file on disk, ensuring unique numbering."""
    while True:
        attempt_path = get_next_attempt_path(solution_path)
        try:
            with attempt_path.open("x", encoding="utf-8"):
                pass
            return attempt_path
        except FileExistsError:
            # A concurrent process created this attempt number; try the next one.
            continue


def prefill_attempt_file(attempt_path: Path, context_lines: List[str]) -> None:
    """Write context header to a new attempt file."""
    if not context_lines:
        return
    try:
        with attempt_path.open("w", encoding="utf-8") as f:
            f.write("\n".join(context_lines))
            f.write(f"\n{MEMO_START_MARKER}\n\n")
    except OSError as exc:
        die(f"Failed to write context to '{attempt_path}': {exc}")


# ==========================================================================
# EDITOR MANAGEMENT
# ==========================================================================

def detect_editor() -> List[str]:
    """Resolve the editor command via $VISUAL, $EDITOR, then fallbacks."""
    visual = os.environ.get("VISUAL")
    editor = os.environ.get("EDITOR")

    for candidate in (visual, editor):
        if candidate:
            tokens = shlex.split(candidate)
            if tokens:
                return tokens

    for name in DEFAULT_EDITORS:
        if shutil.which(name):
            return [name]

    die(
        "No editor detected. Set $VISUAL or $EDITOR, or install one of: "
        + ", ".join(DEFAULT_EDITORS)
    )


def launch_editor(editor_cmd: Sequence[str], attempt_path: Path) -> None:
    """Open the attempt file in the detected editor and block until exit."""
    cmd = [*editor_cmd, str(attempt_path)]
    try:
        subprocess.run(cmd, check=True)
    except FileNotFoundError:
        die(f"Editor command '{cmd[0]}' not found in PATH.")
    except subprocess.CalledProcessError as exc:
        die(f"Editor exited with code {exc.returncode}.")
    except OSError as exc:
        die(f"Failed to launch editor: {exc}")


# ==========================================================================
# FILE READING HELPERS
# ==========================================================================

def read_file_lines(path: Path) -> List[str]:
    """Read a file using UTF-8 and return a list of lines without newlines."""
    try:
        with path.open("r", encoding="utf-8") as handle:
            return handle.read().splitlines(keepends=False)
    except OSError as exc:
        die(f"Failed to read '{path}': {exc}")


def extract_context_and_target(lines: List[str]) -> tuple[List[str], List[str]]:
    """
    Split content into context (before marker) and target (after marker).
    If no marker is found, context is empty and target is all lines.
    """
    for i, line in enumerate(lines):
        if MEMO_START_MARKER in line:
            return lines[:i], lines[i + 1 :]
    return [], lines


# ==========================================================================
# DIFF COMPUTATION
# ==========================================================================

def compute_line_diff(expected: Sequence[str], actual: Sequence[str]):
    """Return line-level diff opcodes using difflib.SequenceMatcher."""
    matcher = SequenceMatcher(a=expected, b=actual, autojunk=False)
    return matcher.get_opcodes()


def render_char_diff(expected: str, actual: str) -> tuple[str, str]:
    """Render two strings with inline ANSI highlighting for differences."""
    matcher = SequenceMatcher(a=expected, b=actual, autojunk=False)
    expected_parts: List[str] = []
    actual_parts: List[str] = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        exp_segment = expected[i1:i2]
        act_segment = actual[j1:j2]

        if tag == "equal":
            expected_parts.append(exp_segment)
            actual_parts.append(act_segment)
        elif tag == "delete":
            expected_parts.append(f"{ANSI_RED_BG}{exp_segment}{ANSI_RESET}")
        elif tag == "insert":
            actual_parts.append(f"{ANSI_GREEN_BG}{act_segment}{ANSI_RESET}")
        elif tag == "replace":
            expected_parts.append(f"{ANSI_RED_BG}{exp_segment}{ANSI_RESET}")
            actual_parts.append(f"{ANSI_GREEN_BG}{act_segment}{ANSI_RESET}")

    return "".join(expected_parts), "".join(actual_parts)


# ==========================================================================
# OUTPUT RENDERING & STATS
# ==========================================================================

def render_diff_report(
    solution_path: Path,
    attempt_path: Path,
    diff_ops,
    expected: Sequence[str],
    actual: Sequence[str],
    *,
    out: Writer = sys.stdout,
) -> None:
    """Print the full diff report with headers and inline highlights."""
    print(HEADER_RULE, file=out)
    print(f"{ANSI_BOLD}MEMORIZATION CHECK:{ANSI_RESET} {solution_path.name}", file=out)
    print(f"Attempt: {attempt_path.name}", file=out)
    print(HEADER_RULE, file=out)

    for tag, i1, i2, j1, j2 in diff_ops:
        if tag == "equal":
            for idx in range(i1, i2):
                line_no = idx + 1
                print(f" {line_no:>4}  {expected[idx]}", file=out)
        elif tag == "replace":
            exp_block = expected[i1:i2]
            act_block = actual[j1:j2]
            max_block = max(len(exp_block), len(act_block))
            for offset in range(max_block):
                exp_line = exp_block[offset] if offset < len(exp_block) else ""
                act_line = act_block[offset] if offset < len(act_block) else ""
                colored_exp, colored_act = render_char_diff(exp_line, act_line)
                if offset < len(exp_block):
                    exp_no = i1 + offset + 1
                    print(f"-{exp_no:>4}  {colored_exp}", file=out)
                if offset < len(act_block):
                    act_no = j1 + offset + 1
                    print(f"+{act_no:>4}  {colored_act}", file=out)
        elif tag == "delete":
            for idx in range(i1, i2):
                exp_line = expected[idx]
                colored_exp, _ = render_char_diff(exp_line, "")
                print(f"-{idx + 1:>4}  {colored_exp}", file=out)
        elif tag == "insert":
            for idx in range(j1, j2):
                _, colored_act = render_char_diff("", actual[idx])
                print(f"+{idx + 1:>4}  {colored_act}", file=out)

    print(HEADER_RULE, file=out)


def compute_stats(
    diff_ops, expected: Sequence[str], actual: Sequence[str]
) -> dict:
    """Compute summary statistics. Returns the stats dict."""
    total_expected = len(expected)
    total_actual = len(actual)
    matching_lines = sum(i2 - i1 for tag, i1, i2, _, _ in diff_ops if tag == "equal")
    changed_lines = sum(i2 - i1 for tag, i1, i2, _, _ in diff_ops if tag == "replace")
    deleted_lines = sum(i2 - i1 for tag, i1, i2, _, _ in diff_ops if tag == "delete")
    inserted_lines = sum(j2 - j1 for tag, _, _, j1, j2 in diff_ops if tag == "insert")

    expected_text = "\n".join(expected)
    actual_text = "\n".join(actual)
    matcher = SequenceMatcher(a=expected_text, b=actual_text, autojunk=False)
    matching_chars = sum(size for _, _, size in matcher.get_matching_blocks())
    total_expected_chars = len(expected_text)

    def percentage(match: int, total: int, *, zero_case: float = 100.0) -> float:
        if total == 0:
            return zero_case
        return (match / total) * 100

    line_accuracy = percentage(
        matching_lines,
        total_expected,
        zero_case=100.0 if total_actual == 0 else 0.0,
    )
    char_accuracy = percentage(
        matching_chars,
        total_expected_chars,
        zero_case=100.0 if len(actual_text) == 0 else 0.0,
    )

    return {
        "total_expected_lines": total_expected,
        "total_actual_lines": total_actual,
        "matching_lines": matching_lines,
        "changed_lines": changed_lines,
        "deleted_lines": deleted_lines,
        "inserted_lines": inserted_lines,
        "line_accuracy": line_accuracy,
        "matching_chars": matching_chars,
        "total_expected_chars": total_expected_chars,
        "char_accuracy": char_accuracy,
    }


def print_stats(stats: dict, *, out: Writer = sys.stdout) -> None:
    """Print summary statistics from the stats dict."""
    print(f"{ANSI_BOLD}SUMMARY{ANSI_RESET}", file=out)
    print(HEADER_RULE, file=out)
    print(f"Total lines (expected): {stats['total_expected_lines']:>6}", file=out)
    print(f"Total lines (yours):    {stats['total_actual_lines']:>6}", file=out)
    print(f"Matching lines:         {stats['matching_lines']:>6}", file=out)
    print(f"Changed lines:          {stats['changed_lines']:>6}", file=out)
    print(f"Inserted lines:         {stats['inserted_lines']:>6}", file=out)
    print(f"Deleted lines:          {stats['deleted_lines']:>6}", file=out)
    print(file=out)

    total_expected = stats["total_expected_lines"]
    matching_lines = stats["matching_lines"]
    line_ratio = (
        f"({matching_lines}/{total_expected})"
        if total_expected
        else "(n/a)"
    )

    total_expected_chars = stats["total_expected_chars"]
    matching_chars = stats["matching_chars"]
    char_ratio = (
        f"({matching_chars}/{total_expected_chars})"
        if total_expected_chars
        else "(n/a)"
    )

    print(f"Line accuracy:          {stats['line_accuracy']:>6.1f}% {line_ratio}", file=out)
    print(f"Character accuracy:     {stats['char_accuracy']:>6.1f}% {char_ratio}", file=out)
    print(HEADER_RULE, file=out)


def strip_ansi(text: str) -> str:
    """Remove ANSI escape sequences from the string."""
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return ansi_escape.sub("", text)


def append_report_to_attempt(attempt_path: Path, report: str) -> None:
    """Append the rendered report to the attempt file for later review."""
    clean_report = strip_ansi(report)
    try:
        with attempt_path.open("a", encoding="utf-8") as handle:
            handle.write("\n")
            if not clean_report.endswith("\n"):
                clean_report = clean_report + "\n"
            handle.write(clean_report)
    except OSError as exc:
        die(f"Failed to append report to '{attempt_path}': {exc}")


def compute_perfect_match(diff_ops, stats: dict) -> bool:
    """Determine if the attempt is a perfect match."""
    differences_found = any(tag != "equal" for tag, *_ in diff_ops)
    return (
        not differences_found
        and stats["total_expected_lines"] == stats["total_actual_lines"]
        and stats["matching_chars"] == stats["total_expected_chars"]
    )


def show_solution_pager(content: List[str]) -> None:
    """Display the solution content in a pager."""
    if not content:
        print("No solution content to display.")
        return

    text = "\n".join(content)
    pager_cmd = os.environ.get("PAGER", "less -r")

    try:
        subprocess.run(
            shlex.split(pager_cmd),
            input=text.encode("utf-8"),
            check=True,
        )
    except (subprocess.SubprocessError, OSError):
        # Fallback to printing if pager fails
        print(text)


def prompt_next_action(*, allow_quit: bool = False) -> str:
    """
    Prompt user for the next action.
    Returns: 'retry', 'stop', 'peek', or 'quit'.
    """
    while True:
        try:
            prompt = "Action? [Y(retry)/n(stop)/p(peek)"
            if allow_quit:
                prompt += "/q(quit)"
            prompt += "] "
            response = input(prompt).strip().lower()
            if response == "" or response == "y":
                return "retry"
            elif response == "n":
                return "stop"
            elif response == "p":
                return "peek"
            elif allow_quit and response in {"q", "quit"}:
                return "quit"
            else:
                print("Please enter Y, n, p", end="")
                if allow_quit:
                    print(", or q")
                else:
                    print()
        except KeyboardInterrupt:
            print()
            raise SystemExit(130)
        except EOFError:
            print()
            return "stop"


def run_drill(
    solution_path: Path, *, allow_quit: bool = False
) -> Literal["perfect", "stopped", "quit"]:
    """Run the full drill loop for a solution and return its outcome."""
    editor_cmd = detect_editor()
    solution_full_lines = read_file_lines(solution_path)
    context_lines, target_lines = extract_context_and_target(solution_full_lines)

    def fresh_attempt() -> Path:
        attempt = create_attempt_file(solution_path)
        if context_lines:
            prefill_attempt_file(attempt, context_lines)
        return attempt

    attempt_path = fresh_attempt()

    while True:
        launch_editor(editor_cmd, attempt_path)

        attempt_full_lines = read_file_lines(attempt_path)
        _, attempt_target_lines = extract_context_and_target(attempt_full_lines)

        diff_ops = compute_line_diff(target_lines, attempt_target_lines)
        stats = compute_stats(diff_ops, target_lines, attempt_target_lines)

        if compute_perfect_match(diff_ops, stats):
            message = (
                f"*** Perfect recall: {solution_path.name} matches exactly "
                f"({attempt_path.name})."
            )
            print(message)
            append_report_to_attempt(attempt_path, message)
            return "perfect"

        report_buffer = io.StringIO()
        tee = TeeWriter(sys.stdout, report_buffer)
        render_diff_report(
            solution_path,
            attempt_path,
            diff_ops,
            target_lines,
            attempt_target_lines,
            out=tee,
        )
        print_stats(stats, out=tee)
        append_report_to_attempt(attempt_path, report_buffer.getvalue())

        action = prompt_next_action(allow_quit=allow_quit)
        if action == "stop":
            return "stopped"
        if action == "quit":
            return "quit"
        if action == "peek":
            show_solution_pager(target_lines)
            attempt_path = fresh_attempt()
            continue
        if action == "retry":
            attempt_path = fresh_attempt()
            continue


def run_focus_session(files: list[Path]) -> int:
    """Run focus drills sequentially, honoring quit requests with exit code 2."""
    if not files:
        return 0

    queue = files[:]
    random.shuffle(queue)
    total = len(queue)

    for idx, solution_path in enumerate(queue, start=1):
        print(f"[{idx}/{total}] {solution_path.name}")
        outcome = run_drill(solution_path, allow_quit=True)
        if outcome == "quit":
            return 2

    return 0
# ==========================================================================
# STATS & HISTORY
# ==========================================================================

def get_attempt_history(solution_path: Path) -> List[dict]:
    """Parse attempt history for the given solution."""
    basename = solution_path.stem or solution_path.name
    suffix = solution_path.suffix
    pattern = f"{basename}-*{suffix}" if suffix else f"{basename}-*"

    attempts = []
    line_acc_re = re.compile(r"Line accuracy:\s+(\d+\.\d+)%")
    char_acc_re = re.compile(r"Character accuracy:\s+(\d+\.\d+)%")

    for path in ATTEMPTS_ROOT.glob(pattern):
        # Ensure strict naming convention match to avoid partial prefix matches
        if not re.search(rf"{re.escape(basename)}-\d+{re.escape(suffix)}$", path.name):
            continue

        try:
            content = path.read_text(encoding="utf-8")
            line_matches = line_acc_re.findall(content)
            char_matches = char_acc_re.findall(content)

            if not line_matches or not char_matches:
                continue

            # Take the last report found in the file
            line_acc = float(line_matches[-1])
            char_acc = float(char_matches[-1])
            timestamp = path.stat().st_mtime

            match = re.search(rf"{re.escape(basename)}-(\d+)", path.name)
            number = int(match.group(1)) if match else 0

            attempts.append(
                {
                    "number": number,
                    "timestamp": timestamp,
                    "line_acc": line_acc,
                    "char_acc": char_acc,
                    "path": path,
                }
            )
        except OSError:
            continue

    return sorted(attempts, key=lambda x: x["number"])


def render_stats(solution_path: Path, history: List[dict]) -> None:
    """Print a history table and summary stats."""
    print(HEADER_RULE)
    print(f"{ANSI_BOLD}HISTORY:{ANSI_RESET} {solution_path.name}")
    print(HEADER_RULE)

    if not history:
        print("No attempts found.")
        return

    print(f"{'Attempt':<8} {'Date':<12} {'Line Acc':<10} {'Char Acc':<10}")
    print("-" * 44)

    for item in history:
        dt = datetime.fromtimestamp(item["timestamp"])
        date_str = dt.strftime("%Y-%m-%d")
        print(
            f"{item['number']:<8} {date_str:<12} {item['line_acc']:>5.1f}%    {item['char_acc']:>5.1f}%"
        )

    print(HEADER_RULE)

    # Calculate current streak of 100% line accuracy
    streak = 0
    for item in reversed(history):
        if item["line_acc"] == 100.0:
            streak += 1
        else:
            break

    if streak > 0:
        print(f"Current Streak: {streak} perfect attempt{'s' if streak != 1 else ''}!")
    print()


# ==========================================================================
# MAIN
# ==========================================================================

def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)

    if args.stats and args.focus:
        die("--stats cannot be combined with --focus.")

    solution_path: Path | None = None
    if args.solution:
        solution_path = validate_solution_path(args.solution)

    if args.stats:
        if solution_path is None:
            solution_path = interactive_select(SOLUTIONS_ROOT)
        history = get_attempt_history(solution_path)
        render_stats(solution_path, history)
        return 0

    exit_codes: dict[str, int] = {"perfect": 0, "stopped": 1, "quit": 2}

    if solution_path is not None:
        result = run_drill(solution_path)
        return exit_codes[result]

    if args.focus:
        focus_files = collect_focus_files()
        if not focus_files:
            die(f"No readable solutions found under '{FOCUS_DIR}'.")
        return run_focus_session(focus_files)

    solution_path = interactive_select(SOLUTIONS_ROOT)
    result = run_drill(solution_path)
    return exit_codes[result]


if __name__ == "__main__":
    sys.exit(main())
