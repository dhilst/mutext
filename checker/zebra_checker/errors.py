"""Schema errors carry a list of findings rather than a single traceback."""

from .findings import Finding


class PuzzleSchemaError(Exception):
    def __init__(self, findings: list[Finding]):
        self.findings = findings
        super().__init__(f"{len(findings)} schema error(s)")


class UnknownClueType(Exception):
    pass


def suggest(value: str, options) -> str | None:
    import difflib

    match = difflib.get_close_matches(str(value), [str(o) for o in options], n=1, cutoff=0.6)
    return match[0] if match else None
