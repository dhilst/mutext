"""Lint the Jekyll post against the puzzle YAML: evidence list, answer widget,
select options and grid structure."""

import re
import unicodedata
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path

from .findings import Finding, finding
from .model import Puzzle

ITEM_RE = re.compile(r"^\s{0,3}(\d+)\.\s+(.*)$")
PANEL_RE = r"\{%\s*include\s+panel\.html[^%]*title=\"TITLE\""
PANEL_END_RE = re.compile(r"{%\s*include\s+panel_end\.html")
ANSWER_RE = re.compile(r'data-puzzle-answer="([^"]*)"')
ANSWER_SPLIT_RE = re.compile(r'data-puzzle-answer="')
SELECT_RE = re.compile(r'<select[^>]*data-answer-dim="(\d+)"(.*?)</select>', re.S)
OPTION_RE = re.compile(r'<option value="([^"]*)"[^>]*>(.*?)</option>', re.S)
ZEBRA_RE = re.compile(r"{%\s*include\s+zebra-table\.html(.*?)%}", re.S)
ARG_RE = re.compile(r'(\w+)="([^"]*)"')
PERMALINK_RE = re.compile(r"^permalink:\s*(\S+)\s*$", re.M)


@dataclass
class EvidenceItem:
    number: int
    text: str
    line: int


def normalize_prose(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    return re.sub(r"\s+", " ", text).strip()


def parse_evidence_items(lines: list[str], panel_title: str) -> list[EvidenceItem]:
    start = None
    opener = re.compile(PANEL_RE.replace("TITLE", re.escape(panel_title)))
    for idx, line in enumerate(lines):
        if opener.search(line):
            start = idx + 1
            break
    if start is None:
        return []
    items: list[EvidenceItem] = []
    for idx in range(start, len(lines)):
        line = lines[idx]
        if PANEL_END_RE.search(line):
            break
        match = ITEM_RE.match(line)
        if match:
            items.append(EvidenceItem(int(match.group(1)), match.group(2).rstrip(), idx + 1))
        elif items and line.strip() and "{%" not in line:
            items[-1] = EvidenceItem(items[-1].number,
                                     items[-1].text + " " + line.strip(),
                                     items[-1].line)
    return items


def split_answer_blocks(body: str) -> list[tuple[list[str], str]]:
    """Each [data-puzzle-answer] block with the markup that follows it.

    A multi-stage chapter has more than one — chapter 10's archive selector
    lives inside the first stage's reveal — so the lint matches the block whose
    tuple is the puzzle's answer and leaves the story stages alone.
    """
    parts = ANSWER_SPLIT_RE.split(body)
    blocks = []
    for chunk in parts[1:]:
        value, _, rest = chunk.partition('"')
        blocks.append(([v.strip() for v in value.split(",")], rest))
    return blocks


def parse_selects(body: str) -> list[tuple[int, list[str], str]]:
    out = []
    for match in SELECT_RE.finditer(body):
        dim = int(match.group(1))
        options = OPTION_RE.findall(match.group(2))
        placeholder = ""
        values = []
        for value, label in options:
            if value == "":
                placeholder = re.sub(r"[—\-\s]", "", label).strip()
            else:
                values.append(value)
        out.append((dim, values, placeholder))
    return out


def parse_zebra(body: str) -> dict[str, list[str]] | None:
    match = ZEBRA_RE.search(body)
    if not match:
        return None
    return {k: v.split("|") for k, v in ARG_RE.findall(match.group(1))}


def _grid_findings(puzzle: Puzzle, grid: dict[str, list[str]], rel: str) -> list[Finding]:
    out: list[Finding] = []
    by_items = {cat.items: cat.name for cat in puzzle.categories}

    def groups(prefix: str) -> list[list[str]]:
        result = []
        for suffix in "abcd":
            key = f"{prefix}_{suffix}"
            if key in grid:
                result.append(grid[key])
            else:
                break
        return result

    cols, rows = groups("cols"), groups("rows")
    if not cols or not rows:
        out.append(finding("E407", "zebra-table is missing cols_a/rows_a", file=rel))
        return out

    def resolve(group: list[str], label: str) -> str | None:
        name = by_items.get(tuple(group))
        if name:
            return name
        same_set = [c for c in puzzle.categories if set(c.items) == set(group)]
        if same_set:
            out.append(finding(
                "E407",
                f"{label} lists category '{same_set[0].name}' in a different order "
                f"than the puzzle declares",
                file=rel,
                hint=f"expected: {'|'.join(same_set[0].items)}"))
        else:
            out.append(finding(
                "E407", f"{label} does not match any category's items", file=rel,
                hint=f"got: {'|'.join(group)}"))
        return None

    col_names = [resolve(g, f"cols_{s}") for g, s in zip(cols, "abcd")]
    row_names = [resolve(g, f"rows_{s}") for g, s in zip(rows, "abcd")]
    if any(n is None for n in col_names + row_names):
        return out

    pairs: list[frozenset] = []
    for r, row_name in enumerate(row_names):
        for c, col_name in enumerate(col_names):
            if r + c < len(col_names):
                if row_name == col_name:
                    out.append(finding(
                        "E407",
                        f"grid block rows_{'abcd'[r]} x cols_{'abcd'[c]} pairs category "
                        f"'{row_name}' with itself",
                        file=rel,
                        hint="rows must be listed in reverse category order: "
                             "cols = G1..G(D-1), rows = GD..G2"))
                pairs.append(frozenset((row_name, col_name)))

    wanted = {frozenset(p) for p in combinations(puzzle.category_names, 2)}
    if len(pairs) != len(set(pairs)) or set(pairs) != wanted:
        missing = wanted - set(pairs)
        extra = [p for p in set(pairs) if p not in wanted]
        detail = []
        if missing:
            detail.append("missing " + ", ".join(" x ".join(sorted(p)) for p in missing))
        if extra:
            detail.append("unexpected " + ", ".join(" x ".join(sorted(p)) for p in extra))
        if len(pairs) != len(set(pairs)):
            detail.append("a category pair is covered twice")
        out.append(finding(
            "E407",
            "grid blocks do not cover each category pair exactly once: " + "; ".join(detail),
            file=rel,
            hint="cols = G1..G(D-1), rows = GD..G2 (reverse)"))
    return out


def lint_post(puzzle: Puzzle, repo_root: Path) -> list[Finding]:
    if puzzle.post is None:
        return [finding("I401", "no post declared; sync lint skipped", file=str(puzzle.path),
                        hint="add a post: block to enable the post <-> yaml lint")]

    path = repo_root / puzzle.post.path
    rel = puzzle.post.path
    if not path.exists():
        return [finding("E409", f"post file not found: {path}", file=str(puzzle.path),
                        line=puzzle.post.line)]

    text = path.read_text()
    lines = text.splitlines()
    out: list[Finding] = []

    # --- evidence list ----------------------------------------------------
    items = parse_evidence_items(lines, puzzle.post.panel_title)
    if not items:
        out.append(finding("E402",
                           f"no numbered evidence items found in the "
                           f"'{puzzle.post.panel_title}' panel",
                           file=rel,
                           hint="check post.panel_title — 001 uses \"clues\""))
    numbers = [i.number for i in items]
    if numbers and numbers != list(range(1, len(numbers) + 1)):
        out.append(finding("W404", f"evidence numbering is not contiguous: {numbers}",
                           file=rel, line=items[0].line))

    by_number = {i.number: i for i in items}
    claimed: dict[int, int] = {}
    for clue in puzzle.clues:
        for pos, number in enumerate(clue.post_numbers):
            if number not in by_number:
                out.append(finding("E404",
                                   f"clue {clue.number}: post_number {number} is not in the "
                                   f"evidence list (1..{len(items)})",
                                   file=str(puzzle.path), line=clue.line,
                                   clue_index=clue.index))
                continue
            if number in claimed:
                out.append(finding("E404",
                                   f"evidence item {number} is claimed by clue "
                                   f"{claimed[number] + 1} and clue {clue.number}",
                                   file=str(puzzle.path), line=clue.line,
                                   clue_index=clue.index))
            claimed[number] = clue.index
            if number in puzzle.post.narrative_only:
                out.append(finding("E404",
                                   f"evidence item {number} is both encoded and listed in "
                                   f"post.narrative_only",
                                   file=str(puzzle.path), line=puzzle.post.line))
            if pos < len(clue.prose):
                want = normalize_prose(clue.prose[pos])
                got = normalize_prose(by_number[number].text)
                if want != got:
                    out.append(finding(
                        "E403",
                        f"evidence item {number} text differs between post and yaml",
                        file=rel, line=by_number[number].line, clue_index=clue.index,
                        hint=f"- yaml: {want}\n       + post: {got}"))

    for number in puzzle.post.narrative_only:
        if number not in by_number:
            out.append(finding("E404",
                               f"post.narrative_only lists item {number}, which is not in the "
                               f"evidence list",
                               file=str(puzzle.path), line=puzzle.post.line))

    for item in items:
        if item.number not in claimed and item.number not in puzzle.post.narrative_only:
            out.append(finding(
                "E402",
                f"evidence item {item.number} is neither encoded nor listed in "
                f"post.narrative_only",
                file=rel, line=item.line,
                data={"prose": item.text},
                hint=f"encode it with post_number: {item.number}, or add {item.number} "
                     f"to post.narrative_only"))

    # --- answer attribute -------------------------------------------------
    blocks = split_answer_blocks(text)
    expected = puzzle.answer_tuple
    lowered = [v.lower() for v in expected]
    grid_block = next((b for b in blocks if [v.lower() for v in b[0]] == lowered), None)

    if not blocks:
        out.append(finding("E405", "no data-puzzle-answer attribute found", file=rel))
    elif grid_block is None:
        got = blocks[0][0]
        out.append(finding(
            "E405",
            f"no data-puzzle-answer block matches the puzzle answer {list(expected)}"
            + (f"; the first block is {list(got)}" if got else ""),
            file=rel,
            hint=f"answer order is {', '.join(puzzle.answer_order)}"))
    else:
        if tuple(grid_block[0]) != expected:
            out.append(finding(
                "W405",
                f"data-puzzle-answer differs from the yaml only in case: "
                f"{list(grid_block[0])} vs {list(expected)}",
                file=rel, hint="the JS lowercases both sides, but item strings should be byte-identical "
                     "in the yaml, the grid labels, the option values and this attribute"))
        if len(blocks) > 1:
            out.append(finding(
                "I410",
                f"{len(blocks) - 1} further answer block(s) on the page are story stages "
                f"and are not checked against this puzzle",
                file=rel))

    # --- selects ----------------------------------------------------------
    # only the selects belonging to the graded block
    selects = parse_selects(grid_block[1]) if grid_block else []
    order = puzzle.answer_order
    if len(selects) != len(order):
        out.append(finding("E406",
                           f"found {len(selects)} answer selects, expected {len(order)}",
                           file=rel))
    else:
        dims = [d for d, _, _ in selects]
        if dims != list(range(len(order))):
            out.append(finding("E406", f"data-answer-dim values are {dims}, expected "
                                       f"{list(range(len(order)))}", file=rel))
        for (dim, values, placeholder), name in zip(selects, order):
            want = list(puzzle.items_of(name))
            if [v.lower() for v in values] != [v.lower() for v in want]:
                out.append(finding(
                    "E406",
                    f"select {dim} options {values} do not match category '{name}' {want}",
                    file=rel, hint="same items, same order, as option value attributes"))
            answer_value = puzzle.answer.get(name, "")
            if answer_value and answer_value.lower() not in [v.lower() for v in values]:
                out.append(finding("E406",
                                   f"select {dim} has no option for the answer "
                                   f"'{answer_value}'", file=rel))

    # --- grid -------------------------------------------------------------
    grid = parse_zebra(text)
    if grid is None:
        out.append(finding("E407", "no zebra-table include found", file=rel))
    else:
        out.extend(_grid_findings(puzzle, grid, rel))

    # --- permalink --------------------------------------------------------
    permalink = PERMALINK_RE.search(text)
    if permalink:
        slug = puzzle.path.stem
        if slug not in permalink.group(1):
            out.append(finding("W408",
                               f"permalink {permalink.group(1)} does not contain the puzzle "
                               f"slug '{slug}'", file=rel))
    return out
