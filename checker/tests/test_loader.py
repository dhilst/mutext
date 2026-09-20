import pytest

from conftest import FIXTURES
from zebra_checker.errors import PuzzleSchemaError
from zebra_checker.loader import load_puzzle


def load(name):
    with pytest.raises(PuzzleSchemaError) as exc:
        load_puzzle(FIXTURES / name)
    return {f.code: f for f in exc.value.findings}


def test_unknown_item_is_reported_not_raised_as_keyerror():
    found = load("bad_item.yaml")
    assert "E108" in found
    assert "t9" in found["E108"].message
    # short names are all equally close, so the hint lists them instead
    assert "t1, t2, t3" in found["E108"].hint


def test_close_names_get_a_suggestion():
    from zebra_checker.errors import suggest

    assert suggest("edge-3", ["edge-01", "edge-02", "edge-03"]) == "edge-03"
    assert suggest("zzzz", ["edge-01"]) is None


def test_answer_value_must_be_an_item():
    assert "E106" in load("bad_answer.yaml")


def test_item_with_a_comma_is_rejected():
    assert "E112" in load("comma_item.yaml")


def test_item_reused_across_categories():
    assert "E104" in load("dup_item_cross_cat.yaml")


def test_good_fixture_loads_cleanly():
    puzzle = load_puzzle(FIXTURES / "good.yaml")
    assert puzzle.dimensions == 3
    assert len(puzzle.clues) == 4
    assert puzzle.answer_tuple == ("p2", "t2", "r2")


def test_deprecated_alias_is_resolved_and_flagged():
    puzzle = load_puzzle(FIXTURES / "dup_syntactic.yaml")
    assert puzzle.clues[-1].type == "link"
    assert any(f.code == "W315" for f in puzzle.schema_findings)


def test_every_shipped_puzzle_loads():
    for path in sorted((FIXTURES.parents[1] / "puzzles").glob("*.yaml")):
        load_puzzle(path)
