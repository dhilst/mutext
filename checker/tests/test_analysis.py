import pytest

from conftest import FIXTURES, codes
from zebra_checker.analysis import analyse
from zebra_checker.loader import load_puzzle

EXPECTED = {
    "good.yaml": set(),
    "vacuous.yaml": {"E301"},
    "vacuous_conjunct.yaml": {"W306"},
    "self_exclusion_same_cat.yaml": {"E313"},
    "dup_syntactic.yaml": {"E303"},
    "dup_semantic.yaml": {"E304"},
    "redundant.yaml": {"W305", "W308"},
    "nonunique.yaml": {"E204"},
    "overconstrained.yaml": {"E201"},
    "contradictory.yaml": {"E201", "E302"},
}


@pytest.mark.parametrize("name,expected", sorted(EXPECTED.items()))
def test_fixture_raises_its_code(check, name, expected):
    report = check(name, post_lint=False)
    assert expected <= codes(report), f"{name}: got {sorted(codes(report))}"


def test_good_fixture_is_clean_under_strict(check):
    report = check("good.yaml", post_lint=False)
    assert not report.failed(strict=True), sorted(codes(report))


def test_redundant_fails_strict_but_passes_lenient(check):
    report = check("redundant.yaml", post_lint=False)
    assert not report.failed(strict=False)
    assert report.failed(strict=True)


def test_keep_redundant_downgrades_to_info(check):
    report = check("redundant_kept.yaml", post_lint=False)
    kept = [f for f in report.findings if f.code == "I305"]
    assert kept and "kept deliberately" in kept[0].message
    dropped = [f for f in report.findings if f.code == "W308"]
    # the marked clue is never named as droppable
    assert all("clue 5" not in f.message for f in dropped)


def test_removable_matches_entailed_on_unique_puzzles(check):
    """For a unique clue set the two notions coincide; W309 flags a mismatch."""
    for name in ("good.yaml", "redundant.yaml", "post_good.yaml"):
        report = check(name, post_lint=False)
        assert "W309" not in codes(report)
        for clue in report.analysis.clue_reports:
            assert clue.redundant == clue.removable, (name, clue.index)


def test_pin_does_not_change_verdicts():
    """The symmetry-breaking pin is a relabeling, so findings must be identical."""
    from zebra_checker.analysis import Analyzer
    from zebra_checker.errors import PuzzleSchemaError

    for name in sorted(EXPECTED):
        try:
            puzzle = load_puzzle(FIXTURES / name)
            puzzle2 = load_puzzle(FIXTURES / name)
        except PuzzleSchemaError:
            continue        # rejected before any solving happens
        pinned = analyse(puzzle)

        unpinned = Analyzer(puzzle2, pin=False)
        assert unpinned.pinned is False
        # vacuity and contradiction must agree with or without the pin
        contradictory = unpinned.find_contradictory()
        vacuous = unpinned.find_vacuous(contradictory)
        assert {c.index for c in pinned.clue_reports if c.contradictory} == contradictory
        assert {c.index for c in pinned.clue_reports if c.vacuous} == vacuous


def test_minimal_subset_is_sufficient_and_minimal(check):
    from zebra_checker.analysis import Analyzer

    puzzle = load_puzzle(FIXTURES / "redundant.yaml")
    az = Analyzer(puzzle)
    status, model = az.solve()
    assert status == "ok"
    keep = az.minimal_subset(model, set())

    from z3 import Solver, Or, unsat, sat

    def unique(indices):
        s = Solver()
        s.add(*az.ax, *[az.f[i] for i in indices])
        assert s.check() == sat
        m = s.model()
        s.add(az._block(m))
        return s.check() == unsat

    assert unique(keep)
    for i in keep:
        assert not unique([j for j in keep if j != i])


def test_shipped_puzzles_have_no_errors(check):
    from pathlib import Path
    from zebra_checker.verifier import check_puzzle_file

    root = FIXTURES.parents[1]
    for path in sorted((root / "puzzles").glob("*.yaml")):
        report = check_puzzle_file(path, repo_root=root.parent)
        assert not report.errors, f"{path.name}: {[f.code for f in report.errors]}"
