import json

from conftest import FIXTURES


def test_json_report_shape(check):
    from zebra_checker.report import render_json

    report = check("redundant.yaml", post_lint=False)
    payload = json.loads(render_json([report], strict=False))
    assert payload["schema"] == "zebra-checker/report@1"
    assert payload["summary"]["puzzles"] == 1
    entry = payload["puzzles"][0]
    assert set(entry) >= {
        "path", "name", "dimensions", "size", "status", "checks", "stats",
        "findings", "solution", "answer_entity", "minimal_subset", "clues",
    }
    assert entry["checks"]["uniqueness"] == "ok"
    assert {"code", "severity", "check", "message"} <= set(entry["findings"][0])
    assert all(set(c) >= {"index", "type", "redundant", "removable"} for c in entry["clues"])


def test_exit_codes(check):
    from zebra_checker.report import exit_code

    good = check("good.yaml", post_lint=False)
    bad = check("nonunique.yaml", post_lint=False)
    warn = check("redundant.yaml", post_lint=False)
    assert exit_code([good], strict=False) == 0
    assert exit_code([bad], strict=False) == 1
    assert exit_code([warn], strict=False) == 0
    assert exit_code([warn], strict=True) == 1


def test_cli_runs_the_whole_corpus():
    from zebra_checker.cli import main

    assert main([str(FIXTURES.parents[1] / "puzzles"), "-q", "--no-post-lint"]) == 0
