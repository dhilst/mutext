import pytest

from conftest import FIXTURES, codes, messages

EXPECTED = {
    "post_good.yaml": set(),
    "post_narrative_only.yaml": set(),
    "post_missing_number.yaml": {"E402"},
    "post_wrong_prose.yaml": {"E403"},
    "post_wrong_answer.yaml": {"E405"},
    "post_case_answer.yaml": {"W405"},
    "post_wrong_selects.yaml": {"E406"},
    "post_wrong_grid.yaml": {"E407"},
}


@pytest.mark.parametrize("name,expected", sorted(EXPECTED.items()))
def test_post_sync_fixture(check, name, expected):
    report = check(name)
    assert expected <= codes(report), f"{name}: got {sorted(codes(report))}"
    if not expected:
        assert not report.failed(strict=True), sorted(codes(report))


def test_missing_number_names_the_item_and_the_fix(check):
    report = check("post_missing_number.yaml")
    hit = next(f for f in report.findings if f.code == "E402")
    assert "item 5" in hit.message
    assert "narrative_only" in hit.hint
    assert hit.line and hit.file.endswith("post_missing_number.md")


def test_wrong_grid_names_the_self_pairing(check):
    report = check("post_wrong_grid.yaml")
    text = " ".join(messages(report, "E407"))
    assert "with itself" in text or "exactly once" in text


def test_missing_post_block_is_skipped_not_failed(check):
    report = check("good.yaml")
    assert "I401" in codes(report)
    assert not report.failed(strict=True)


def test_parsers_handle_the_shipped_posts():
    from pathlib import Path
    from zebra_checker.postlint import parse_evidence_items, parse_selects, parse_zebra

    posts = FIXTURES.parents[2] / "_posts"
    for path in sorted(posts.glob("*.md")):
        text = path.read_text()
        title = "clues" if "title=\"clues\"" in text else "evidence"
        assert parse_evidence_items(text.splitlines(), title), path.name
        assert parse_selects(text), path.name
        assert parse_zebra(text), path.name
