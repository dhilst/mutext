import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

FIXTURES = Path(__file__).parent / "fixtures"
REPO_ROOT = ROOT.parent


@pytest.fixture
def fixtures() -> Path:
    return FIXTURES


@pytest.fixture
def check():
    from zebra_checker.verifier import check_puzzle_file

    def run(name: str, *, repo_root: Path = FIXTURES, **kw):
        return check_puzzle_file(FIXTURES / name, repo_root=repo_root, **kw)

    return run


def codes(report) -> set[str]:
    return {f.code for f in report.findings}


def messages(report, code: str) -> list[str]:
    return [f.message for f in report.findings if f.code == code]
