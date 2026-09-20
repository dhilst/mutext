"""Finding records and the severity policy shared by every check."""

from dataclasses import dataclass, field
from enum import Enum


class Severity(str, Enum):
    ERROR = "error"
    WARN = "warn"
    INFO = "info"


# code -> (default severity, check name, one-line meaning)
CODES: dict[str, tuple[Severity, str, str]] = {
    # --- schema / loader -------------------------------------------------
    "E101": (Severity.ERROR, "schema", "missing or unknown top-level key"),
    "E102": (Severity.ERROR, "schema", "dimensions/size disagree with categories"),
    "E103": (Severity.ERROR, "schema", "duplicate item within a category"),
    "E104": (Severity.ERROR, "schema", "item name reused across categories"),
    "E105": (Severity.ERROR, "schema", "answer key is not a category"),
    "E106": (Severity.ERROR, "schema", "answer value is not an item of its category"),
    "E107": (Severity.ERROR, "schema", "unknown clue type"),
    "E108": (Severity.ERROR, "schema", "clue references an unknown category or item"),
    "E109": (Severity.ERROR, "schema", "clue is missing a required field"),
    "E110": (Severity.ERROR, "schema", "post_number/prose are malformed"),
    "E112": (Severity.ERROR, "schema", "item name contains a comma"),
    # --- core solve ------------------------------------------------------
    "E201": (Severity.ERROR, "satisfiable", "no solution exists (over-constrained)"),
    "E202": (Severity.ERROR, "answer", "solution does not match the declared answer"),
    "E204": (Severity.ERROR, "uniqueness", "multiple solutions exist"),
    "E205": (Severity.ERROR, "satisfiable", "solver returned unknown (timeout)"),
    # --- clue quality ----------------------------------------------------
    "E301": (Severity.ERROR, "quality", "clue is vacuous (implied by the grid rules)"),
    "E302": (Severity.ERROR, "quality", "clue can never hold"),
    "E303": (Severity.ERROR, "quality", "duplicate clue (identical encoding)"),
    "E304": (Severity.ERROR, "quality", "duplicate clue (logically equivalent)"),
    "E313": (Severity.ERROR, "quality", "self_exclusion within a single category"),
    "W305": (Severity.WARN, "quality", "clue is redundant (implied by the others)"),
    "W306": (Severity.WARN, "quality", "vacuous conjunct inside a clue"),
    "I307": (Severity.INFO, "quality", "minimal sufficient clue subset"),
    "W308": (Severity.WARN, "quality", "clue set is not minimal"),
    "W309": (Severity.WARN, "quality", "removable/entailed disagree (internal)"),
    "W310": (Severity.WARN, "quality", "symmetry break disabled: position-sensitive clue"),
    "W311": (Severity.WARN, "quality", "clue is a conjunct of another clue"),
    "I305": (Severity.INFO, "quality", "redundant clue kept deliberately"),
    "W314": (Severity.WARN, "quality", "stale keep_redundant marker"),
    "W315": (Severity.WARN, "schema", "deprecated clue type"),
    # --- post sync -------------------------------------------------------
    "I401": (Severity.INFO, "post_sync", "no post declared; sync lint skipped"),
    "E402": (Severity.ERROR, "post_sync", "prose item is neither encoded nor narrative_only"),
    "E403": (Severity.ERROR, "post_sync", "prose text differs between post and yaml"),
    "E404": (Severity.ERROR, "post_sync", "post_number is out of range or claimed twice"),
    "E405": (Severity.ERROR, "post_sync", "data-puzzle-answer disagrees with the answer"),
    "W405": (Severity.WARN, "post_sync", "data-puzzle-answer differs only in case"),
    "E406": (Severity.ERROR, "post_sync", "select options disagree with the categories"),
    "E407": (Severity.ERROR, "post_sync", "grid does not cover each category pair once"),
    "E409": (Severity.ERROR, "post_sync", "post file not found"),
    "W404": (Severity.WARN, "post_sync", "evidence numbering is not contiguous"),
    "W408": (Severity.WARN, "post_sync", "permalink does not match the puzzle slug"),
    "I410": (Severity.INFO, "post_sync", "extra answer blocks belong to story stages"),
}


@dataclass(frozen=True)
class Finding:
    code: str
    message: str
    file: str | None = None
    line: int | None = None
    hint: str | None = None
    clue_index: int | None = None
    data: dict = field(default_factory=dict)

    @property
    def severity(self) -> Severity:
        return CODES[self.code][0]

    @property
    def check(self) -> str:
        return CODES[self.code][1]

    def promoted(self) -> "Finding":
        """Under --strict a WARN counts as an ERROR; INFO stays INFO."""
        return self

    def location(self) -> str:
        if not self.file:
            return ""
        return f"{self.file}:{self.line}" if self.line else self.file


def finding(code: str, message: str, **kw) -> Finding:
    if code not in CODES:
        raise KeyError(f"unregistered finding code: {code}")
    return Finding(code=code, message=message, **kw)
