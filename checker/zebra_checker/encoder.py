"""Variables and axioms as pure values — no Solver is touched here."""

from z3 import BoolRef, Distinct, Int, Solver

from .model import Puzzle

Assign = dict[str, dict[str, object]]


def build_variables(puzzle: Puzzle) -> Assign:
    """One Int per item; two items match iff they share an entity number."""
    return {
        cat.name: {item: Int(f"{cat.name}__{item}") for item in cat.items}
        for cat in puzzle.categories
    }


def base_axioms(assign: Assign, puzzle: Puzzle) -> list[BoolRef]:
    """Axiom I: every category is a permutation of the entity numbers."""
    out: list[BoolRef] = []
    n = puzzle.size
    for cat in puzzle.categories:
        variables = [assign[cat.name][item] for item in cat.items]
        for v in variables:
            out.append(v >= 0)
            out.append(v < n)
        out.append(Distinct(*variables))
    return out


def symmetry_break(assign: Assign, puzzle: Puzzle) -> list[BoolRef]:
    """Entity numbers are arbitrary labels; pin the first category's order.

    This is a relabeling, not a restriction: it selects one representative per
    orbit.  Sound for every relabeling-invariant clue type (see clues.py), and
    it shrinks the model space by n!.
    """
    first = puzzle.categories[0]
    return [assign[first.name][item] == i for i, item in enumerate(first.items)]


def axioms(assign: Assign, puzzle: Puzzle, *, pin: bool = True) -> list[BoolRef]:
    out = base_axioms(assign, puzzle)
    if pin:
        out += symmetry_break(assign, puzzle)
    return out


def add_axioms(solver: Solver, assign: Assign, puzzle: Puzzle) -> None:
    solver.add(*axioms(assign, puzzle))
