from zebra_checker import clues
from zebra_checker.loader import load_puzzle
from conftest import FIXTURES


def test_every_registered_type_is_complete():
    """A new clue type cannot ship without being wired into every table."""
    tables = {
        "RELABEL_INVARIANT": clues.RELABEL_INVARIANT,
        "REQUIRED_FIELDS": clues.REQUIRED_FIELDS,
        "_KEYS": clues._KEYS,
        "_DESCRIBE": clues._DESCRIBE,
        "_ENDPOINTS": clues._ENDPOINTS,
    }
    for name, table in tables.items():
        assert set(table) == set(clues.ENCODERS), f"{name} disagrees with ENCODERS"


def test_direct_and_link_share_a_canonical_key():
    puzzle = load_puzzle(FIXTURES / "dup_syntactic.yaml")
    direct = puzzle.clues[0]          # direct proc:p1 = tok:t1
    link = puzzle.clues[-1]           # conditional if tok:t1 then proc:p1
    assert clues.normal_key(direct) == clues.normal_key(link)


def test_negation_key_differs_from_direct():
    puzzle = load_puzzle(FIXTURES / "overconstrained.yaml")
    assert clues.normal_key(puzzle.clues[0]) != clues.normal_key(puzzle.clues[-1])


def test_conjuncts_split_multi_atom_clues():
    from zebra_checker.encoder import build_variables

    puzzle = load_puzzle(FIXTURES / "vacuous_conjunct.yaml")
    assign = build_variables(puzzle)
    atoms = clues.conjuncts(puzzle.clues[-1], assign)
    assert len(atoms) == 2
    assert len(clues.conjuncts(puzzle.clues[0], assign)) == 1
