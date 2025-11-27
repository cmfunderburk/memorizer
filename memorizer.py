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
from dataclasses import dataclass
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
ANSI_GREEN = "\033[32m"
ANSI_YELLOW = "\033[33m"
ANSI_BRIGHT_GREEN = "\033[92m"
ANSI_BRIGHT_YELLOW = "\033[93m"
ANSI_DIM = "\033[2m"
HEADER_RULE = "=" * 40
INFO_MARKER = "<!-- INFO -->"

# Regex for fenced code blocks: ```lang\ncontent\n```
CODE_BLOCK_PATTERN = re.compile(
    r'^```(\w*)\n(.*?)^```',
    re.MULTILINE | re.DOTALL
)


# ==========================================================================
# MARKDOWN PARSING
# ==========================================================================

@dataclass
class CodeBlock:
    """A fenced code block extracted from markdown."""
    language: str
    content: str
    start_pos: int  # character position in raw text where ``` starts
    end_pos: int    # character position where closing ``` ends
    is_target: bool  # True unless preceded by <!-- INFO -->


@dataclass
class ParsedMarkdown:
    """Result of parsing a markdown file."""
    raw_text: str
    blocks: list[CodeBlock]
    target_blocks: list[CodeBlock]


def parse_markdown(text: str) -> ParsedMarkdown:
    """
    Extract fenced code blocks from markdown text.
    
    Blocks preceded by <!-- INFO --> (within 50 chars) are marked as non-targets.
    Returns ParsedMarkdown with all blocks and filtered target_blocks.
    """
    blocks: list[CodeBlock] = []
    
    for match in CODE_BLOCK_PATTERN.finditer(text):
        language = match.group(1)
        content = match.group(2)
        start_pos = match.start()
        end_pos = match.end()
        
        # Check for INFO marker in preceding 50 characters
        lookback_start = max(0, start_pos - 50)
        preceding_text = text[lookback_start:start_pos]
        is_target = INFO_MARKER not in preceding_text
        
        # Strip trailing newline from content if present
        if content.endswith('\n'):
            content = content[:-1]
        
        blocks.append(CodeBlock(
            language=language,
            content=content,
            start_pos=start_pos,
            end_pos=end_pos,
            is_target=is_target,
        ))
    
    target_blocks = [b for b in blocks if b.is_target]
    
    return ParsedMarkdown(
        raw_text=text,
        blocks=blocks,
        target_blocks=target_blocks,
    )


def render_attempt_template(parsed: ParsedMarkdown) -> str:
    """
    Generate attempt file content with placeholders for target blocks.
    
    Replaces each target block's content with [BLOCK N] placeholder,
    preserving the fence markers and surrounding markdown.
    """
    result = parsed.raw_text
    
    # Process blocks in reverse order to preserve positions
    for i, block in enumerate(reversed(parsed.target_blocks)):
        block_num = len(parsed.target_blocks) - i
        line_count = block.content.count('\n') + 1 if block.content else 0
        lang_str = block.language if block.language else "code"
        placeholder = f"[BLOCK {block_num}] {lang_str} - {line_count} lines"
        
        # Find the content portion within the fenced block
        # The block goes from start_pos to end_pos
        # Format: ```lang\ncontent\n```
        block_text = result[block.start_pos:block.end_pos]
        
        # Find where content starts (after ```lang\n)
        first_newline = block_text.find('\n')
        if first_newline == -1:
            continue
            
        # Find where content ends (before \n```)
        last_fence = block_text.rfind('```')
        if last_fence == -1:
            continue
        
        # Build new block with placeholder
        opening = block_text[:first_newline + 1]  # ```lang\n
        closing = block_text[last_fence:]          # ```
        new_block = f"{opening}{placeholder}\n{closing}"
        
        # Replace in result
        result = result[:block.start_pos] + new_block + result[block.end_pos:]
    
    return result


@dataclass
class BlockResult:
    """Result of comparing a single code block."""
    block_index: int
    language: str
    expected_lines: int
    actual_lines: int
    line_accuracy: float
    char_accuracy: float
    is_perfect: bool
    diff_ops: list  # For rendering diffs
    expected: list[str]
    actual: list[str]


def compare_blocks(
    expected_blocks: list[CodeBlock],
    actual_blocks: list[str],
) -> list[BlockResult]:
    """
    Compare expected code blocks against actual attempt blocks.
    
    Returns per-block results. Missing actual blocks score 0%.
    Extra actual blocks are ignored.
    """
    results: list[BlockResult] = []
    
    for i, expected_block in enumerate(expected_blocks):
        expected_lines = expected_block.content.splitlines()
        expected_lines = strip_trailing_blank_lines(expected_lines)
        
        if i < len(actual_blocks):
            actual_lines = actual_blocks[i].splitlines()
            actual_lines = strip_trailing_blank_lines(actual_lines)
        else:
            # Missing block
            actual_lines = []
        
        diff_ops = compute_line_diff(expected_lines, actual_lines)
        stats = compute_stats(diff_ops, expected_lines, actual_lines)
        is_perfect = compute_perfect_match(diff_ops, stats)
        
        results.append(BlockResult(
            block_index=i + 1,
            language=expected_block.language,
            expected_lines=len(expected_lines),
            actual_lines=len(actual_lines),
            line_accuracy=stats["line_accuracy"],
            char_accuracy=stats["char_accuracy"],
            is_perfect=is_perfect,
            diff_ops=diff_ops,
            expected=expected_lines,
            actual=actual_lines,
        ))
    
    return results


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
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Show progress summary for all solutions.",
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
    
    suffix = ".attempt.md"
    pattern = f"{basename}-*.attempt.md"
    # Match basename-N where N is a number, before .attempt.md
    regex = re.compile(rf"{re.escape(basename)}-(\d+)\.attempt$")

    highest = 0
    for path in ATTEMPTS_ROOT.glob(pattern):
        match = regex.search(path.stem)
        if match:
            highest = max(highest, int(match.group(1)))

    next_number = highest + 1
    return ATTEMPTS_ROOT / f"{basename}-{next_number}{suffix}"


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


def strip_trailing_blank_lines(lines: List[str]) -> List[str]:
    """Remove trailing blank lines from a list of lines."""
    result = lines[:]
    while result and result[-1].strip() == "":
        result.pop()
    return result


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
    
    # Character accuracy ignoring whitespace
    expected_no_ws = re.sub(r'\s', '', expected_text)
    actual_no_ws = re.sub(r'\s', '', actual_text)
    matcher = SequenceMatcher(a=expected_no_ws, b=actual_no_ws, autojunk=False)
    matching_chars = sum(size for _, _, size in matcher.get_matching_blocks())
    total_expected_chars = len(expected_no_ws)

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
        zero_case=100.0 if len(actual_no_ws) == 0 else 0.0,
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


def render_markdown_report(
    solution_path: Path,
    attempt_path: Path,
    block_results: list[BlockResult],
    *,
    out: Writer = sys.stdout,
) -> None:
    """Print per-block scores and document summary for markdown solutions."""
    print(HEADER_RULE, file=out)
    print(f"{ANSI_BOLD}MEMORIZATION CHECK:{ANSI_RESET} {solution_path.name}", file=out)
    print(f"Attempt: {attempt_path.name}", file=out)
    print(HEADER_RULE, file=out)
    print(file=out)
    
    for result in block_results:
        lang_str = result.language if result.language else "code"
        if result.is_perfect:
            status = f"{ANSI_GREEN}✓{ANSI_RESET}"
            accuracy_str = f"{ANSI_GREEN}100.0%{ANSI_RESET}"
        else:
            status = f"{ANSI_YELLOW}✗{ANSI_RESET}"
            accuracy_str = f"{ANSI_YELLOW}{result.char_accuracy:.1f}%{ANSI_RESET}"
        
        print(
            f"BLOCK {result.block_index} ({lang_str}, {result.expected_lines} lines):  "
            f"{status} {accuracy_str}",
            file=out,
        )
        
        # Show diff for imperfect blocks
        if not result.is_perfect:
            print(file=out)
            for tag, i1, i2, j1, j2 in result.diff_ops:
                if tag == "equal":
                    for idx in range(i1, i2):
                        print(f"    {idx + 1:>4}  {result.expected[idx]}", file=out)
                elif tag == "replace":
                    exp_block = result.expected[i1:i2]
                    act_block = result.actual[j1:j2]
                    max_block = max(len(exp_block), len(act_block))
                    for offset in range(max_block):
                        exp_line = exp_block[offset] if offset < len(exp_block) else ""
                        act_line = act_block[offset] if offset < len(act_block) else ""
                        colored_exp, colored_act = render_char_diff(exp_line, act_line)
                        if offset < len(exp_block):
                            print(f"   -{i1 + offset + 1:>4}  {colored_exp}", file=out)
                        if offset < len(act_block):
                            print(f"   +{j1 + offset + 1:>4}  {colored_act}", file=out)
                elif tag == "delete":
                    for idx in range(i1, i2):
                        colored_exp, _ = render_char_diff(result.expected[idx], "")
                        print(f"   -{idx + 1:>4}  {colored_exp}", file=out)
                elif tag == "insert":
                    for idx in range(j1, j2):
                        _, colored_act = render_char_diff("", result.actual[idx])
                        print(f"   +{idx + 1:>4}  {colored_act}", file=out)
        print(file=out)
    
    # Document summary
    print(HEADER_RULE, file=out)
    min_accuracy = min(r.char_accuracy for r in block_results) if block_results else 0.0
    num_blocks = len(block_results)
    print(f"DOCUMENT SCORE: {min_accuracy:.1f}% (min of {num_blocks} block{'s' if num_blocks != 1 else ''})", file=out)
    print(HEADER_RULE, file=out)
    
    if all(r.is_perfect for r in block_results):
        # Celebratory banner for perfect recall
        print(file=out)
        print(f"{ANSI_BOLD}    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓{ANSI_RESET}", file=out)
        print(f"{ANSI_BOLD}    ┃                              ┃{ANSI_RESET}", file=out)
        print(f"{ANSI_BOLD}    ┃    ★  PERFECT RECALL  ★      ┃{ANSI_RESET}", file=out)
        print(f"{ANSI_BOLD}    ┃                              ┃{ANSI_RESET}", file=out)
        print(f"{ANSI_BOLD}    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{ANSI_RESET}", file=out)
        print(file=out)


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
            if allow_quit:
                prompt = "Action? [Y(retry)/n(skip)/p(peek)/q(quit session)] "
            else:
                prompt = "Action? [Y(retry)/n(stop)/p(peek)] "
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


def prompt_continue_after_perfect(next_solution: Path | None) -> Literal["continue", "quit"]:
    """
    Prompt user after perfect recall to continue with next solution or quit.
    Returns: 'continue' or 'quit'.
    """
    while True:
        try:
            if next_solution is not None:
                prompt = f"Next solution: {ANSI_BOLD}{ANSI_BRIGHT_GREEN}{next_solution.name}{ANSI_RESET}\nContinue? [Y(continue)/q(quit)] "
                response = input(prompt).strip().lower()
                if response == "" or response == "y":
                    return "continue"
                elif response in {"q", "quit"}:
                    return "quit"
                else:
                    print("Please enter Y or q")
            else:
                # All solutions completed - any input exits successfully
                input("All solutions completed! Press Enter to exit. ")
                return "continue"
        except KeyboardInterrupt:
            print()
            raise SystemExit(130)
        except EOFError:
            print()
            return "quit"


def run_drill(
    solution_path: Path, *, allow_quit: bool = False
) -> Literal["perfect", "stopped", "quit"]:
    """Run drill loop for markdown solutions with multi-block support."""
    editor_cmd = detect_editor()
    
    # Parse solution file
    solution_text = solution_path.read_text(encoding="utf-8")
    parsed_solution = parse_markdown(solution_text)
    
    if not parsed_solution.target_blocks:
        die(f"No target code blocks found in '{solution_path}'")
    
    # Generate attempt template
    template = render_attempt_template(parsed_solution)
    
    def fresh_attempt() -> Path:
        # Atomic file creation to handle concurrent processes
        max_retries = 100
        for _ in range(max_retries):
            attempt = get_next_attempt_path(solution_path)
            try:
                # "x" mode: exclusive creation, fails if file exists
                with attempt.open("x", encoding="utf-8") as f:
                    f.write(template)
                return attempt
            except FileExistsError:
                # Another process created this file, retry with next number
                continue
        die(f"Failed to create attempt file after {max_retries} retries")
    
    attempt_path = fresh_attempt()
    
    while True:
        launch_editor(editor_cmd, attempt_path)
        
        # Parse attempt file
        attempt_text = attempt_path.read_text(encoding="utf-8")
        parsed_attempt = parse_markdown(attempt_text)
        # Use target_blocks to match only user-filled blocks (excludes INFO blocks)
        actual_contents = [b.content for b in parsed_attempt.target_blocks]
        
        # Warn if block count mismatch
        expected_count = len(parsed_solution.target_blocks)
        actual_count = len(actual_contents)
        if actual_count > expected_count:
            print(
                f"{ANSI_YELLOW}Warning: Found {actual_count} code blocks, "
                f"expected {expected_count}. Ignoring extra blocks.{ANSI_RESET}"
            )
        
        # Compare blocks
        block_results = compare_blocks(parsed_solution.target_blocks, actual_contents)
        
        # Check if all blocks are perfect
        all_perfect = all(r.is_perfect for r in block_results)
        
        # Always show the report (includes celebration banner if perfect)
        report_buffer = io.StringIO()
        tee = TeeWriter(sys.stdout, report_buffer)
        render_markdown_report(solution_path, attempt_path, block_results, out=tee)
        append_report_to_attempt(attempt_path, report_buffer.getvalue())
        
        if all_perfect:
            return "perfect"
        
        action = prompt_next_action(allow_quit=allow_quit)
        if action == "stop":
            return "stopped"
        if action == "quit":
            return "quit"
        if action == "peek":
            # Show all target blocks
            peek_content = []
            for i, block in enumerate(parsed_solution.target_blocks, 1):
                lang = block.language if block.language else "code"
                peek_content.append(f"=== BLOCK {i} ({lang}) ===")
                peek_content.append(block.content)
                peek_content.append("")
            show_solution_pager(peek_content)
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
        elif outcome == "stopped":
            print("(Skipping this snippet, moving to next...)")
        elif outcome == "perfect":
            # After perfect recall, show celebration and prompt for next action
            print()  # Add spacing after celebration message
            next_idx = idx  # Current index (0-based after enumerate)
            next_solution = queue[next_idx] if next_idx < len(queue) else None
            action = prompt_continue_after_perfect(next_solution)
            if action == "quit":
                return 2
            # Continue to next iteration

    return 0
# ==========================================================================
# STATS & HISTORY
# ==========================================================================

def get_attempt_history(solution_path: Path) -> List[dict]:
    """Parse attempt history for the given solution."""
    basename = solution_path.stem or solution_path.name
    
    pattern = f"{basename}-*.attempt.md"
    name_regex = re.compile(rf"{re.escape(basename)}-(\d+)\.attempt\.md$")

    attempts = []
    doc_score_re = re.compile(r"DOCUMENT SCORE:\s+(\d+\.\d+)%")

    for path in ATTEMPTS_ROOT.glob(pattern):
        # Ensure strict naming convention match to avoid partial prefix matches
        if not name_regex.search(path.name):
            continue

        try:
            content = path.read_text(encoding="utf-8")
            
            doc_matches = doc_score_re.findall(content)
            if not doc_matches:
                # Check for perfect recall message (no DOCUMENT SCORE printed)
                if "Perfect recall:" in content:
                    line_acc = 100.0
                else:
                    continue
            else:
                line_acc = float(doc_matches[-1])

            timestamp = path.stat().st_mtime

            match = re.search(rf"{re.escape(basename)}-(\d+)", path.name)
            number = int(match.group(1)) if match else 0

            attempts.append(
                {
                    "number": number,
                    "timestamp": timestamp,
                    "line_acc": line_acc,
                    "char_acc": line_acc,  # Same value for consistency
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

    print(f"{'Attempt':<8} {'Date':<12} {'Line Acc':<12} {'Char Acc':<10}")
    print("-" * 46)

    for item in history:
        dt = datetime.fromtimestamp(item["timestamp"])
        date_str = dt.strftime("%Y-%m-%d")
        if item["line_acc"] == 100.0:
            line_str = f"{ANSI_GREEN}100.0% ★{ANSI_RESET}"
            char_str = f"{ANSI_GREEN}100.0% ★{ANSI_RESET}"
        else:
            line_str = f"{item['line_acc']:>5.1f}%  "
            char_str = f"{item['char_acc']:>5.1f}%  "
        print(f"{item['number']:<8} {date_str:<12} {line_str:<21} {char_str}")

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

    # Show best score achieved
    best = max(item["line_acc"] for item in history)
    if best == 100.0:
        print(f"Best Score: {ANSI_GREEN}100.0%{ANSI_RESET}")
    else:
        print(f"Best Score: {best:.1f}% (not yet perfect)")
    print()


# ==========================================================================
# PROGRESS SUMMARY
# ==========================================================================

@dataclass
class SolutionSummary:
    """Summary statistics for a single solution file."""
    path: Path
    relative_path: str  # e.g., "focus/insertion_sort.md"
    attempted: bool
    last_date: datetime | None
    last_score: float | None
    best_score: float | None
    streak: int  # consecutive 100% at end of history
    mastered: bool  # last_score == 100.0


def compute_summary(solution_path: Path, history: List[dict]) -> SolutionSummary:
    """Derive summary statistics for a solution from its attempt history."""
    try:
        relative = solution_path.relative_to(SOLUTIONS_ROOT)
    except ValueError:
        relative = solution_path
    
    if not history:
        return SolutionSummary(
            path=solution_path,
            relative_path=str(relative),
            attempted=False,
            last_date=None,
            last_score=None,
            best_score=None,
            streak=0,
            mastered=False,
        )
    
    last_item = history[-1]
    last_date = datetime.fromtimestamp(last_item["timestamp"])
    last_score = last_item["line_acc"]
    best_score = max(item["line_acc"] for item in history)
    
    # Calculate streak of consecutive 100% at end
    streak = 0
    for item in reversed(history):
        if item["line_acc"] == 100.0:
            streak += 1
        else:
            break
    
    return SolutionSummary(
        path=solution_path,
        relative_path=str(relative),
        attempted=True,
        last_date=last_date,
        last_score=last_score,
        best_score=best_score,
        streak=streak,
        mastered=(last_score == 100.0),
    )


def collect_all_summaries() -> List[SolutionSummary]:
    """Gather summary statistics for all solution files."""
    summaries = []
    for solution in SOLUTIONS_ROOT.rglob("*.md"):
        if solution.name.startswith("."):
            continue
        history = get_attempt_history(solution)
        summaries.append(compute_summary(solution, history))
    return summaries


def render_summary(summaries: List[SolutionSummary]) -> None:
    """Print progress summary grouped by directory."""
    print(HEADER_RULE)
    print(f"{ANSI_BOLD}PROGRESS SUMMARY{ANSI_RESET}")
    print(HEADER_RULE)
    print()
    
    if not summaries:
        print("No solution files found.")
        return
    
    # Group by parent directory
    groups: dict[str, List[SolutionSummary]] = {}
    for s in summaries:
        parent = str(Path(s.relative_path).parent)
        if parent == ".":
            parent = "(root)"
        groups.setdefault(parent, []).append(s)
    
    # Sort groups: focus first, then alphabetically
    def group_sort_key(name: str) -> tuple[int, str]:
        if name == "focus":
            return (0, name)
        return (1, name)
    
    sorted_groups = sorted(groups.keys(), key=group_sort_key)
    
    total_attempted = 0
    total_mastered = 0
    total_solutions = len(summaries)
    latest_date: datetime | None = None
    
    collapse_threshold = 10
    
    for group_name in sorted_groups:
        group = sorted(groups[group_name], key=lambda s: s.path.name)
        attempted_in_group = sum(1 for s in group if s.attempted)
        mastered_in_group = sum(1 for s in group if s.mastered)
        
        total_attempted += attempted_in_group
        total_mastered += mastered_in_group
        
        # Track latest date
        for s in group:
            if s.last_date and (latest_date is None or s.last_date > latest_date):
                latest_date = s.last_date
        
        # Collapse large unattempted directories
        if len(group) > collapse_threshold and attempted_in_group == 0:
            print(f"{ANSI_DIM}{SOLUTIONS_DIR}/{group_name}/{ANSI_RESET}")
            print(f"  {ANSI_DIM}({len(group)} files, 0 attempted){ANSI_RESET}")
            print()
            continue
        
        print(f"{SOLUTIONS_DIR}/{group_name}/")
        
        for s in group:
            name = s.path.name
            if not s.attempted:
                print(f"  {ANSI_DIM}{name:<28} —  (no attempts){ANSI_RESET}")
            elif s.mastered:
                date_str = s.last_date.strftime("%Y-%m-%d") if s.last_date else ""
                streak_str = f"streak: {s.streak}" if s.streak > 0 else ""
                print(f"  {ANSI_GREEN}{name:<28} ✓ 100%  {date_str}  {streak_str}{ANSI_RESET}")
            else:
                date_str = s.last_date.strftime("%Y-%m-%d") if s.last_date else ""
                score_str = f"{s.last_score:>3.0f}%" if s.last_score else ""
                print(f"  {ANSI_YELLOW}{name:<28} ✗ {score_str}  {date_str}{ANSI_RESET}")
        
        print()
    
    # Totals
    print("-" * 40)
    mastery_str = f"{total_mastered}/{total_solutions} mastered (last attempt 100%)"
    print(f"TOTALS: {total_attempted}/{total_solutions} attempted | {mastery_str}")
    if latest_date:
        print(f"Last practice: {latest_date.strftime('%Y-%m-%d')}")
    print(HEADER_RULE)


# ==========================================================================
# MAIN
# ==========================================================================

def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)

    if args.stats and args.focus:
        die("--stats cannot be combined with --focus.")

    if args.summary:
        if args.stats or args.focus or args.solution:
            die("--summary cannot be combined with other options.")
        summaries = collect_all_summaries()
        render_summary(summaries)
        return 0

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
