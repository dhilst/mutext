"""Clue-quality analysis: vacuity, contradiction, duplication, entailment,
leave-one-out minimality and a minimal sufficient subset."""

from dataclasses import dataclass, field
from itertools import combinations

from z3 import Bool, BoolRef, Implies, Not, Or, Solver, sat, unknown, unsat

from . import clues as clue_grammar
from .encoder import axioms, build_variables
from .findings import Finding, finding
from .model import Puzzle


@dataclass
class ClueReport:
    index: int
    type: str
    describe: str
    vacuous: bool = False
    contradictory: bool = False
    redundant: bool = False
    removable: bool = False
    duplicate_of: int | None = None
    in_minimal_subset: bool = True


@dataclass
class AnalysisResult:
    status: str = "ok"                    # ok | unsat | unknown
    model = None
    solution: list[dict] = field(default_factory=list)
    answer_entity: int | None = None
    clue_reports: list[ClueReport] = field(default_factory=list)
    minimal_subset: list[int] = field(default_factory=list)
    findings: list[Finding] = field(default_factory=list)
    solver_calls: int = 0
    pinned: bool = True


class Analyzer:
    def __init__(self, puzzle: Puzzle, *, timeout_ms: int = 10_000, pin: bool | None = None):
        self.puzzle = puzzle
        self.timeout_ms = timeout_ms
        self.rel = str(puzzle.path)
        self.calls = 0
        self.findings: list[Finding] = []

        invariant = all(
            clue_grammar.RELABEL_INVARIANT.get(c.type, False) for c in puzzle.clues
        )
        self.pinned = invariant if pin is None else pin
        if pin is None and not invariant:
            offenders = sorted({
                c.type for c in puzzle.clues
                if not clue_grammar.RELABEL_INVARIANT.get(c.type, False)
            })
            self.findings.append(finding(
                "W310",
                "symmetry break disabled for entailment: position-sensitive clue type(s) "
                + ", ".join(offenders),
                file=self.rel,
            ))

        self.assign = build_variables(puzzle)
        self.ax = axioms(self.assign, puzzle, pin=self.pinned)
        self.f: list[BoolRef] = [
            clue_grammar.constraint(c, self.assign) for c in puzzle.clues
        ]
        self.p = [Bool(f"clue__{i}") for i in range(len(self.f))]

        self.base = self._solver()
        self.base.add(*self.ax)
        for indicator, formula in zip(self.p, self.f):
            self.base.add(Implies(indicator, formula))

    # -- plumbing ----------------------------------------------------------

    def _solver(self) -> Solver:
        s = Solver()
        s.set("timeout", self.timeout_ms)
        return s

    def _check(self, solver: Solver, *assumptions):
        self.calls += 1
        return solver.check(*assumptions)

    def _all_p(self):
        return list(self.p)

    def _block(self, model) -> BoolRef:
        return Or(*[
            self.assign[cat.name][item] != model.eval(self.assign[cat.name][item])
            for cat in self.puzzle.categories
            for item in cat.items
        ])

    def _clue_label(self, i: int) -> str:
        return f"clue {i + 1} ({clue_grammar.describe(self.puzzle.clues[i])})"

    def _clue_line(self, i: int):
        return self.puzzle.clues[i].line

    def add(self, code: str, message: str, *, clue_index=None, hint=None, line=None, **data):
        self.findings.append(finding(
            code, message, file=self.rel,
            line=line if line is not None else (
                self._clue_line(clue_index) if clue_index is not None else None),
            hint=hint, clue_index=clue_index, data=data,
        ))

    # -- core --------------------------------------------------------------

    def solve(self):
        result = self._check(self.base, *self._all_p())
        if result == unknown:
            self.add("E205", "solver returned unknown (timeout) while solving",
                     hint="raise --timeout, or simplify the clue set")
            return "unknown", None
        if result == unsat:
            self.add("E201", "no solution exists — the clues contradict each other",
                     hint="run with --explain; a contradictory single clue is reported as E302")
            return "unsat", None
        return "ok", self.base.model()

    def solution_rows(self, model) -> list[dict]:
        entities: dict[int, dict] = {}
        for cat in self.puzzle.categories:
            for item in cat.items:
                e = model.eval(self.assign[cat.name][item]).as_long()
                entities.setdefault(e, {})[cat.name] = item
        return [dict(entity=e, **entities[e]) for e in sorted(entities)]

    def check_answer(self, model) -> int | None:
        numbers = {
            name: model.eval(self.assign[name][item]).as_long()
            for name, item in self.puzzle.answer.items()
        }
        if len(set(numbers.values())) != 1:
            detail = ", ".join(f"{k}={self.puzzle.answer[k]}@{v}" for k, v in numbers.items())
            self.add("E202",
                     "the declared answer items do not describe one entity: " + detail,
                     hint="the answer tuple must be a single row of the solution")
            return None
        return next(iter(numbers.values()))

    def check_unique(self, model) -> bool:
        self.base.push()
        self.base.add(self._block(model))
        result = self._check(self.base, *self._all_p())
        alt = self.base.model() if result == sat else None
        self.base.pop()
        if result == unknown:
            self.add("E205", "solver returned unknown (timeout) during the uniqueness check")
            return False
        if result == sat:
            rows = ", ".join(
                "/".join(str(v) for k, v in row.items() if k != "entity")
                for row in self.solution_rows(alt)
            )
            self.add("E204", "multiple solutions exist — the puzzle is under-constrained",
                     hint=f"a second solution: {rows}")
            return False
        return True

    # -- per-clue checks ---------------------------------------------------

    def find_contradictory(self) -> set[int]:
        hits = set()
        for i, formula in enumerate(self.f):
            s = self._solver()
            s.add(*self.ax)
            s.add(formula)
            if self._check(s) == unsat:
                hits.add(i)
                self.add("E302", f"{self._clue_label(i)} can never be true",
                         clue_index=i,
                         hint="the grid rules already rule this out — check the categories")
        return hits

    def find_vacuous(self, skip: set[int]) -> set[int]:
        hits = set()
        for i, formula in enumerate(self.f):
            if i in skip:
                continue
            s = self._solver()
            s.add(*self.ax)
            s.add(Not(formula))
            if self._check(s) == unsat:
                hits.add(i)
                self.add("E301",
                         f"{self._clue_label(i)} is vacuous — the grid rules already say it",
                         clue_index=i,
                         hint="delete it, or move it to post.narrative_only as flavour")
                continue
            atoms = clue_grammar.conjuncts(self.puzzle.clues[i], self.assign)
            if len(atoms) > 1:
                for label, atom in atoms:
                    s2 = self._solver()
                    s2.add(*self.ax)
                    s2.add(Not(atom))
                    if self._check(s2) == unsat:
                        self.add("W306",
                                 f"clue {i + 1}: conjunct '{label}' is vacuous",
                                 clue_index=i)
        return hits

    def find_duplicates(self, *, semantic: bool = True, pair_limit: int = 300) -> dict[int, int]:
        dupes: dict[int, int] = {}
        seen: dict[object, int] = {}
        keys = []
        for i, clue in enumerate(self.puzzle.clues):
            key = clue_grammar.normal_key(clue)
            keys.append(key)
            if key in seen:
                first = seen[key]
                dupes[i] = first
                self.add("E303", f"clue {i + 1} repeats clue {first + 1} "
                                 f"({clue_grammar.describe(clue)})",
                         clue_index=i, hint="delete one of them")
            else:
                seen[key] = i

        # a clue that is literally one of another clue's conjuncts
        conj_keys: dict[int, set] = {}
        for i, clue in enumerate(self.puzzle.clues):
            atoms = clue_grammar.conjuncts(clue, self.assign)
            if len(atoms) > 1 and isinstance(keys[i], tuple) and keys[i][0] == "AND":
                conj_keys[i] = set(keys[i][1])
        for i, key in enumerate(keys):
            for j, members in conj_keys.items():
                if i != j and i not in dupes and key in members:
                    self.add("W311", f"clue {i + 1} is a conjunct of clue {j + 1}",
                             clue_index=i)

        if not semantic:
            return dupes
        pairs = list(combinations(range(len(self.f)), 2))
        if len(pairs) > pair_limit:
            return dupes
        for i, j in pairs:
            if i in dupes or j in dupes or keys[i] == keys[j]:
                continue
            s = self._solver()
            s.add(*self.ax)
            s.add(self.f[i] != self.f[j])
            if self._check(s) == unsat:
                dupes[j] = i
                self.add("E304",
                         f"clue {j + 1} is logically equivalent to clue {i + 1}",
                         clue_index=j, hint="delete one of them")
        return dupes

    def find_redundant(self, skip: set[int], keep: set[int] | None = None) -> set[int]:
        """Entailed by the other clues plus the grid rules.

        Mutual entailment means several clues in an over-determined cluster are
        each individually removable while only some can go together, so the
        warning is raised for the clues the minimisation actually drops.  The
        rest are named in the I307 line instead.
        """
        keep = set(range(len(self.f))) if keep is None else keep
        hits = set()
        for i in range(len(self.f)):
            if i in skip:
                continue
            others = [self.p[j] for j in range(len(self.f)) if j != i]
            self.base.push()
            self.base.add(Not(self.f[i]))
            result = self._check(self.base, *others)
            core = []
            if result == unsat:
                core = [str(c) for c in self.base.unsat_core()]
            self.base.pop()
            if result == unsat:
                implied_by = sorted(
                    int(name.split("__")[1]) + 1 for name in core if name.startswith("clue__")
                )
                hits.add(i)
                because = (" + ".join(f"clue {n}" for n in implied_by) + " + grid rules"
                           if implied_by else "the grid rules")
                clue = self.puzzle.clues[i]
                if clue.keep_redundant:
                    self.add("I305",
                             f"{self._clue_label(i)} is implied by {because}; kept deliberately"
                             + (f" — {clue.note}" if clue.note else ""),
                             clue_index=i)
                elif i not in keep:
                    self.add("W305",
                             f"{self._clue_label(i)} is implied by {because}",
                             clue_index=i,
                             hint="delete it, or set keep_redundant: true with a note "
                                  "saying why the player needs it restated")
                else:
                    self.add("I305",
                             f"{self._clue_label(i)} is implied by {because}, but the "
                             f"minimal subset keeps it and drops another clue instead",
                             clue_index=i)
        for i, clue in enumerate(self.puzzle.clues):
            if clue.keep_redundant and i not in hits:
                self.add("W314",
                         f"clue {i + 1} is marked keep_redundant but is load-bearing",
                         clue_index=i, hint="drop the marker")
        return hits

    def find_removable(self, model, skip: set[int]) -> set[int]:
        """Uniqueness survives without the clue.  One call per clue: the answer
        model already satisfies the reduced set, so blocking it suffices."""
        hits = set()
        for i in range(len(self.f)):
            if i in skip:
                continue
            others = [self.p[j] for j in range(len(self.f)) if j != i]
            self.base.push()
            self.base.add(self._block(model))
            result = self._check(self.base, *others)
            self.base.pop()
            if result == unsat:
                hits.add(i)
        return hits

    def minimal_subset(self, model, skip: set[int]) -> list[int]:
        keep = [i for i in range(len(self.f)) if i not in skip]
        for i in list(keep):
            trial = [j for j in keep if j != i]
            self.base.push()
            self.base.add(self._block(model))
            result = self._check(self.base, *[self.p[j] for j in trial])
            self.base.pop()
            if result == unsat:
                keep = trial
        return keep


def analyse(puzzle: Puzzle, *, timeout_ms: int = 10_000, semantic_dup: bool = True,
            checks: set[str] | None = None) -> AnalysisResult:
    checks = checks or {"core", "vacuity", "duplication", "redundancy", "minimality"}
    az = Analyzer(puzzle, timeout_ms=timeout_ms)
    result = AnalysisResult(pinned=az.pinned)

    status, model = az.solve()
    result.status = status
    if status != "ok":
        contradictory = az.find_contradictory() if "vacuity" in checks else set()
        for i, clue in enumerate(puzzle.clues):
            result.clue_reports.append(ClueReport(
                index=i, type=clue.type,
                describe=clue_grammar.describe(clue),
                contradictory=i in contradictory,
                in_minimal_subset=False,
            ))
        result.findings = az.findings
        result.solver_calls = az.calls
        return result

    result.model = model
    result.solution = az.solution_rows(model)
    result.answer_entity = az.check_answer(model)
    unique = az.check_unique(model)

    contradictory: set[int] = set()
    if "vacuity" in checks:
        contradictory = az.find_contradictory()
        vacuous = az.find_vacuous(contradictory)
    else:
        vacuous = set()

    dupes: dict[int, int] = {}
    if "duplication" in checks:
        dupes = az.find_duplicates(semantic=semantic_dup)

    skip = contradictory | vacuous | set(dupes)

    keep: list[int] = list(range(len(puzzle.clues)))
    if unique and "minimality" in checks:
        keep = az.minimal_subset(model, skip)
        result.minimal_subset = keep
    else:
        result.minimal_subset = keep

    redundant: set[int] = set()
    removable: set[int] = set()
    if unique and "redundancy" in checks:
        redundant = az.find_redundant(skip, set(keep))
        removable = az.find_removable(model, skip)
        for i in sorted(redundant ^ removable):
            az.add("W309",
                   f"clue {i + 1}: entailment and leave-one-out disagree "
                   f"(entailed={i in redundant}, removable={i in removable})",
                   clue_index=i,
                   hint="for a unique puzzle these are the same property — "
                        "suspect an encoder bug")

    if unique and "minimality" in checks:
        droppable = [i for i in range(len(puzzle.clues))
                     if i not in keep and i not in skip
                     and not puzzle.clues[i].keep_redundant]
        az.add("I307",
               "minimal sufficient subset: "
               + ", ".join(f"clue {i + 1}" for i in keep)
               + f" ({len(keep)} of {len(puzzle.clues)} load-bearing)")
        if droppable:
            az.add("W308",
                   f"clue set is not minimal: {len(droppable)} clue(s) can be dropped "
                   "while keeping a unique solution — "
                   + ", ".join(f"clue {i + 1}" for i in droppable))

    for i, clue in enumerate(puzzle.clues):
        result.clue_reports.append(ClueReport(
            index=i, type=clue.type, describe=clue_grammar.describe(clue),
            vacuous=i in vacuous, contradictory=i in contradictory,
            redundant=i in redundant, removable=i in removable,
            duplicate_of=dupes.get(i),
            in_minimal_subset=i in result.minimal_subset,
        ))

    result.findings = az.findings
    result.solver_calls = az.calls
    return result
