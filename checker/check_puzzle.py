#!/usr/bin/env python3
import sys
from pathlib import Path

from zebra_checker.loader import load_puzzle
from zebra_checker.verifier import verify_puzzle


def main():
    if len(sys.argv) < 2:
        print("Usage: check_puzzle.py <puzzle.yaml | puzzles_dir/>")
        sys.exit(1)

    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    paths = [a for a in sys.argv[1:] if not a.startswith("-")]

    files = []
    for p in paths:
        path = Path(p)
        if path.is_dir():
            files.extend(sorted(path.glob("*.yaml")))
        elif path.is_file():
            files.append(path)
        else:
            print(f"Not found: {p}")
            sys.exit(1)

    if not files:
        print("No puzzle files found.")
        sys.exit(1)

    results = []
    for f in files:
        puzzle = load_puzzle(f)
        ok = verify_puzzle(puzzle, verbose=verbose)
        results.append((f.name, ok))

    print("\n" + "=" * 40)
    all_pass = all(ok for _, ok in results)
    for name, ok in results:
        status = "PASS" if ok else "FAIL"
        print(f"  {name}: {status}")

    print("=" * 40)
    if all_pass:
        print(f"All {len(results)} puzzle(s) passed.")
    else:
        failed = sum(1 for _, ok in results if not ok)
        print(f"{failed}/{len(results)} puzzle(s) failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
