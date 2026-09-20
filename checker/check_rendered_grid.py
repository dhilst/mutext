#!/usr/bin/env python3
"""Verify a BUILT page's deduction grid.

The post lint checks the zebra-table arguments in the source; this checks what
Liquid actually rendered.  For every active cell it reads the aria-label
("<row> x <col>"), works out which category each side belongs to, and asserts
that no cell pairs a category with itself and that the active blocks cover each
category pair exactly once.

    uv run check_rendered_grid.py ../_site/puzzles/008-split-brain.html \
        --puzzle puzzles/008-split-brain.yaml
"""

import argparse
import re
import sys
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from zebra_checker.loader import load_puzzle  # noqa: E402

LABEL_RE = re.compile(r'data-grid-cell[^>]*aria-label="([^"]+)"')


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("page", help="a built HTML page under _site/")
    ap.add_argument("--puzzle", required=True, help="the matching puzzle YAML")
    args = ap.parse_args()

    puzzle = load_puzzle(Path(args.puzzle))
    owner = {item: cat.name for cat in puzzle.categories for item in cat.items}

    labels = LABEL_RE.findall(Path(args.page).read_text())
    if not labels:
        print("no active grid cells found", file=sys.stderr)
        return 1

    pairs: set[frozenset] = set()
    bad: list[str] = []
    unknown: list[str] = []
    for label in labels:
        row, _, col = label.partition(" × ")
        row, col = row.strip(), col.strip()
        if row not in owner or col not in owner:
            unknown.append(label)
            continue
        if owner[row] == owner[col]:
            bad.append(label)
        pairs.add(frozenset((owner[row], owner[col])))

    wanted = {frozenset(p) for p in combinations(puzzle.category_names, 2)}
    n = puzzle.size
    expected_cells = len(wanted) * n * n

    print(f"{Path(args.page).name}: {len(labels)} active cells "
          f"(expected {expected_cells})")
    ok = True
    if unknown:
        print(f"  FAIL  {len(unknown)} cell(s) label items no category owns, "
              f"e.g. {unknown[0]!r}")
        ok = False
    if bad:
        print(f"  FAIL  {len(bad)} cell(s) pair a category with itself, "
              f"e.g. {bad[0]!r}")
        ok = False
    if pairs != wanted:
        missing = wanted - pairs
        if missing:
            print("  FAIL  category pairs never crossed: "
                  + ", ".join(" x ".join(sorted(p)) for p in missing))
        ok = False
    if len(labels) != expected_cells:
        print(f"  FAIL  cell count is {len(labels)}, expected {expected_cells}")
        ok = False
    print("  OK" if ok else "  see failures above")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
