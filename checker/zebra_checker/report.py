"""Rendering: human text, JSON, and the process exit code."""

import json

from .findings import Severity
from .verifier import CHECK_ORDER, PuzzleReport

TOOL_VERSION = "0.2.0"

EXIT_OK = 0
EXIT_ERROR = 1
EXIT_USAGE = 2
EXIT_TIMEOUT = 3


def _fmt(f) -> str:
    head = f"  {f.code}  {f.check}"
    if f.location():
        head += f"  {f.location()}"
    lines = [head, f"        {f.message}"]
    if f.hint:
        lines.append(f"        fix: {f.hint}")
    return "\n".join(lines)


def render_text(report: PuzzleReport, *, verbose: bool = False, strict: bool = False) -> str:
    out: list[str] = []
    header = f"=== {report.name}"
    if report.dimensions:
        header += f"  {report.dimensions}x{report.size}"
    out.append(f"{header}  {report.path} ===")

    if report.puzzle:
        cats = " ".join(f"{c.name}({len(c.items)})" for c in report.puzzle.categories)
        encoded = len(report.puzzle.clues)
        flavour = len(report.puzzle.post.narrative_only) if report.puzzle.post else 0
        out.append(f"categories  {cats}")
        out.append(f"clues       {encoded} encoded"
                   + (f", {flavour} narrative-only" if flavour else ""))

    skipped = {f.check for f in report.findings if f.code in ("I401",)}
    for check in CHECK_ORDER:
        status = report.check_status(check, strict=strict)
        mark = {"ok": "OK", "warn": "WARN", "error": "FAIL"}[status]
        if check in skipped and status == "ok":
            mark = "SKIP"
        out.append("  " + (check + " ").ljust(24, ".") + f" {mark}")

    if verbose and report.analysis and report.analysis.solution:
        out.append("")
        for row in report.analysis.solution:
            entity = row["entity"]
            parts = ", ".join(f"{k}={v}" for k, v in row.items() if k != "entity")
            tag = "  <- ANSWER" if entity == report.analysis.answer_entity else ""
            out.append(f"  entity {entity}: {parts}{tag}")

    for label, group in (("ERRORS", report.errors), ("WARNINGS", report.warnings)):
        if group:
            out.append("")
            out.append(label)
            out.extend(_fmt(f) for f in group)
    if verbose and report.infos:
        out.append("")
        out.append("INFO")
        out.extend(_fmt(f) for f in report.infos)

    verdict = "FAIL" if report.failed(strict=strict) else "PASS"
    out.append("")
    out.append(f"RESULT  {verdict}   {len(report.errors)} error(s), "
               f"{len(report.warnings)} warning(s)   "
               f"{report.solver_calls} solver calls, {report.elapsed_ms} ms")
    return "\n".join(out)


def render_summary(reports: list[PuzzleReport], *, strict: bool) -> str:
    width = max((len(r.path) for r in reports), default=10)
    out = ["", "=" * (width + 20)]
    for r in reports:
        verdict = "FAIL" if r.failed(strict=strict) else "PASS"
        extra = ""
        if verdict == "PASS" and r.warnings:
            extra = f"  ({len(r.warnings)} warning(s))"
        out.append(f"  {r.path:<{width}}  {verdict}{extra}")
    out.append("=" * (width + 20))
    failed = [r for r in reports if r.failed(strict=strict)]
    if failed:
        out.append(f"{len(failed)}/{len(reports)} puzzle(s) failed.")
    else:
        out.append(f"All {len(reports)} puzzle(s) passed.")
    return "\n".join(out)


def render_json(reports: list[PuzzleReport], *, strict: bool) -> str:
    payload = {
        "schema": "zebra-checker/report@1",
        "tool_version": TOOL_VERSION,
        "strict": strict,
        "summary": {
            "puzzles": len(reports),
            "passed": sum(1 for r in reports if not r.failed(strict=strict)),
            "failed": sum(1 for r in reports if r.failed(strict=strict)),
            "errors": sum(len(r.errors) for r in reports),
            "warnings": sum(len(r.warnings) for r in reports),
            "exit_code": exit_code(reports, strict=strict),
        },
        "puzzles": [],
    }
    for r in reports:
        entry = {
            "path": r.path,
            "name": r.name,
            "dimensions": r.dimensions,
            "size": r.size,
            "status": "fail" if r.failed(strict=strict) else "pass",
            "checks": {c: r.check_status(c, strict=strict) for c in CHECK_ORDER},
            "stats": {"solver_calls": r.solver_calls, "elapsed_ms": r.elapsed_ms},
            "findings": [
                {
                    "code": f.code,
                    "severity": f.severity.value,
                    "check": f.check,
                    "message": f.message,
                    "file": f.file,
                    "line": f.line,
                    "hint": f.hint,
                    "clue_index": f.clue_index,
                    "data": f.data,
                }
                for f in r.findings
            ],
        }
        if r.analysis:
            entry["solution"] = r.analysis.solution
            entry["answer_entity"] = r.analysis.answer_entity
            entry["minimal_subset"] = r.analysis.minimal_subset
            entry["clues"] = [
                {
                    "index": c.index,
                    "type": c.type,
                    "describe": c.describe,
                    "vacuous": c.vacuous,
                    "contradictory": c.contradictory,
                    "redundant": c.redundant,
                    "removable": c.removable,
                    "duplicate_of": c.duplicate_of,
                    "in_minimal_subset": c.in_minimal_subset,
                }
                for c in r.analysis.clue_reports
            ]
        payload["puzzles"].append(entry)
    return json.dumps(payload, indent=2)


def exit_code(reports: list[PuzzleReport], *, strict: bool) -> int:
    if any(r.timed_out() for r in reports):
        return EXIT_TIMEOUT
    if any(r.failed(strict=strict) for r in reports):
        return EXIT_ERROR
    return EXIT_OK
