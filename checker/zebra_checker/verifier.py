"""Orchestration: load -> analyse -> post lint, returning a report."""

from dataclasses import dataclass, field
from pathlib import Path

from .analysis import AnalysisResult, analyse
from .errors import PuzzleSchemaError
from .findings import Finding, Severity
from .loader import load_puzzle
from .model import Puzzle
from .postlint import lint_post

CHECK_ORDER = ["schema", "satisfiable", "answer", "uniqueness", "quality", "post_sync"]


@dataclass
class PuzzleReport:
    path: str
    name: str
    dimensions: int = 0
    size: int = 0
    findings: list[Finding] = field(default_factory=list)
    analysis: AnalysisResult | None = None
    puzzle: Puzzle | None = None
    solver_calls: int = 0
    elapsed_ms: int = 0

    def by_severity(self, severity: Severity) -> list[Finding]:
        return [f for f in self.findings if f.severity is severity]

    @property
    def errors(self) -> list[Finding]:
        return self.by_severity(Severity.ERROR)

    @property
    def warnings(self) -> list[Finding]:
        return self.by_severity(Severity.WARN)

    @property
    def infos(self) -> list[Finding]:
        return self.by_severity(Severity.INFO)

    def failed(self, *, strict: bool) -> bool:
        return bool(self.errors) or (strict and bool(self.warnings))

    def timed_out(self) -> bool:
        return any(f.code == "E205" for f in self.findings)

    def check_status(self, check: str, *, strict: bool) -> str:
        relevant = [f for f in self.findings if f.check == check]
        if any(f.severity is Severity.ERROR for f in relevant):
            return "error"
        if any(f.severity is Severity.WARN for f in relevant):
            return "error" if strict else "warn"
        return "ok"


def check_puzzle_file(path: Path, *, repo_root: Path, timeout_ms: int = 10_000,
                      semantic_dup: bool = True, post_lint: bool = True,
                      checks: set[str] | None = None) -> PuzzleReport:
    import time

    started = time.time()
    path = Path(path)
    try:
        puzzle = load_puzzle(path)
    except PuzzleSchemaError as exc:
        return PuzzleReport(path=str(path), name=path.stem, findings=exc.findings,
                            elapsed_ms=int((time.time() - started) * 1000))

    report = PuzzleReport(
        path=str(path), name=puzzle.name, dimensions=puzzle.dimensions,
        size=puzzle.size, puzzle=puzzle,
    )
    report.findings.extend(getattr(puzzle, "schema_findings", []))

    result = analyse(puzzle, timeout_ms=timeout_ms, semantic_dup=semantic_dup, checks=checks)
    report.analysis = result
    report.findings.extend(result.findings)
    report.solver_calls = result.solver_calls

    if post_lint and (checks is None or "postsync" in checks):
        report.findings.extend(lint_post(puzzle, repo_root))

    report.elapsed_ms = int((time.time() - started) * 1000)
    return report


def verify_puzzle(puzzle, verbose: bool = False) -> bool:
    """Back-compatible entry point: True when the puzzle has no errors."""
    from .report import render_text

    if isinstance(puzzle, (str, Path)):
        report = check_puzzle_file(Path(puzzle), repo_root=Path.cwd().parent)
    else:
        report = PuzzleReport(path=str(getattr(puzzle, "path", "?")),
                              name=getattr(puzzle, "name", "?"))
        result = analyse(puzzle)
        report.analysis = result
        report.findings.extend(result.findings)
    print(render_text(report, verbose=verbose, strict=False))
    return not report.errors
