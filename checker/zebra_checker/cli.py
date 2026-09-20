"""Command line entry point."""

import argparse
import sys
from pathlib import Path

from .report import EXIT_USAGE, exit_code, render_json, render_summary, render_text
from .verifier import check_puzzle_file

ALL_CHECKS = {"core", "vacuity", "duplication", "redundancy", "minimality", "postsync"}


def find_repo_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / "_config.yml").exists():
            return candidate
    return start


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="check_puzzle.py",
        description="Verify zebra puzzles: solvable, correct, unique, and free of "
                    "vacuous, duplicate or redundant clues.",
    )
    p.add_argument("paths", nargs="*", default=["puzzles"],
                   help="puzzle files or directories (default: puzzles)")
    p.add_argument("-v", "--verbose", action="store_true",
                   help="print the solution and INFO findings")
    p.add_argument("-q", "--quiet", action="store_true", help="only the summary")
    p.add_argument("--json", action="store_true", help="machine-readable report on stdout")
    p.add_argument("--strict", action="store_true", help="treat warnings as errors")
    p.add_argument("--explain", action="store_true",
                   help="alias for --verbose: show the minimal subset and INFO findings")
    p.add_argument("--checks", help=f"comma-separated subset of {sorted(ALL_CHECKS)}")
    p.add_argument("--skip", help="comma-separated checks to skip")
    p.add_argument("--no-deep-dup", action="store_true",
                   help="skip the pairwise semantic duplication pass")
    p.add_argument("--posts", "--posts-dir", dest="posts", default=None,
                   help="directory holding the posts (default: <repo>/_posts)")
    p.add_argument("--no-post-lint", action="store_true", help="skip the post <-> yaml lint")
    p.add_argument("--timeout", type=int, default=10_000, help="per-solver-call timeout in ms")
    return p


def collect(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            files.extend(sorted(path.glob("*.yaml")))
        elif path.is_file():
            files.append(path)
        else:
            print(f"Not found: {raw}", file=sys.stderr)
            sys.exit(EXIT_USAGE)
    return files


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    verbose = args.verbose or args.explain

    files = collect(args.paths)
    if not files:
        print("No puzzle files found.", file=sys.stderr)
        return EXIT_USAGE

    checks = set(ALL_CHECKS)
    if args.checks:
        checks = {c.strip() for c in args.checks.split(",") if c.strip()}
        unknown = checks - ALL_CHECKS
        if unknown:
            print(f"Unknown check(s): {', '.join(sorted(unknown))}", file=sys.stderr)
            return EXIT_USAGE
    if args.skip:
        checks -= {c.strip() for c in args.skip.split(",") if c.strip()}

    repo_root = find_repo_root(files[0].resolve().parent)
    if args.posts:
        posts_root = Path(args.posts).resolve()
        # the yaml stores "_posts/<file>", so the lint root is the posts dir's parent
        repo_root = posts_root.parent if posts_root.name == "_posts" else posts_root

    reports = []
    for path in files:
        report = check_puzzle_file(
            path, repo_root=repo_root, timeout_ms=args.timeout,
            semantic_dup=not args.no_deep_dup,
            post_lint=not args.no_post_lint,
            checks=checks,
        )
        reports.append(report)
        if not args.json and not args.quiet:
            print()
            print(render_text(report, verbose=verbose, strict=args.strict))

    if args.json:
        print(render_json(reports, strict=args.strict))
    else:
        print(render_summary(reports, strict=args.strict))

    return exit_code(reports, strict=args.strict)


if __name__ == "__main__":
    sys.exit(main())
