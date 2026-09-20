"""Clue grammar: encoding, canonical form, decomposition and description.

Every clue type must appear in ENCODERS, RELABEL_INVARIANT, REQUIRED_FIELDS,
_KEYS, _CONJUNCTS, _DESCRIBE and _ENDPOINTS.  A registry test enforces that, so
a new type cannot be added without wiring it into the analyses.
"""

from collections.abc import Callable, Iterator, Hashable

from z3 import And, BoolRef, Implies, Or, Sum, If, Xor, Solver

from .errors import UnknownClueType
from .model import Clue, Endpoint

Assign = dict[str, dict[str, object]]

# Deprecated spellings mapped to their canonical type.
ALIASES = {"conditional": "link"}


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def _ep(spec: dict) -> Endpoint:
    return Endpoint(spec["category"], spec["item"])


def _var(assign: Assign, ep: Endpoint):
    return assign[ep.category][ep.item]


def _fact(spec: dict, assign: Assign) -> BoolRef:
    """A fact is {subject, object, negated?} — an equality or an inequality."""
    a = _var(assign, _ep(spec["subject"]))
    b = _var(assign, _ep(spec["object"]))
    return a != b if spec.get("negated") else a == b


def _fact_key(spec: dict) -> Hashable:
    pair = frozenset({
        (spec["subject"]["category"], spec["subject"]["item"]),
        (spec["object"]["category"], spec["object"]["item"]),
    })
    return ("NE" if spec.get("negated") else "EQ", pair)


def _fact_text(spec: dict) -> str:
    op = "!=" if spec.get("negated") else "="
    return f"{_ep(spec['subject'])} {op} {_ep(spec['object'])}"


def _pairs(clue: Clue) -> list[tuple[Endpoint, Endpoint]]:
    """(a, b) pairs for self_exclusion's mapping."""
    ca, cb = clue.raw["category_a"], clue.raw["category_b"]
    return [(Endpoint(ca, a), Endpoint(cb, b)) for a, b in clue.raw["mapping"].items()]


# --------------------------------------------------------------------------
# encoders
# --------------------------------------------------------------------------

def _enc_direct(clue: Clue, assign: Assign) -> BoolRef:
    return _var(assign, _ep(clue.raw["subject"])) == _var(assign, _ep(clue.raw["object"]))


def _enc_negation(clue: Clue, assign: Assign) -> BoolRef:
    return _var(assign, _ep(clue.raw["subject"])) != _var(assign, _ep(clue.raw["object"]))


def _enc_link(clue: Clue, assign: Assign) -> BoolRef:
    return _var(assign, _ep(clue.raw["if"])) == _var(assign, _ep(clue.raw["then"]))


def _enc_self_exclusion(clue: Clue, assign: Assign) -> BoolRef:
    return And(*[_var(assign, a) != _var(assign, b) for a, b in _pairs(clue)])


def _enc_disjunction(clue: Clue, assign: Assign) -> BoolRef:
    s = _var(assign, _ep(clue.raw["subject"]))
    atoms = [s == _var(assign, _ep(o)) for o in clue.raw["any_of"]]
    if clue.raw.get("exclusive"):
        return And(Or(*atoms), Sum([If(a, 1, 0) for a in atoms]) == 1)
    return Or(*atoms)


def _enc_not_equal_any(clue: Clue, assign: Assign) -> BoolRef:
    s = _var(assign, _ep(clue.raw["subject"]))
    return And(*[s != _var(assign, _ep(o)) for o in clue.raw["none_of"]])


def _enc_implication(clue: Clue, assign: Assign) -> BoolRef:
    return Implies(_fact(clue.raw["if"], assign), _fact(clue.raw["then"], assign))


def _enc_exactly_one(clue: Clue, assign: Assign) -> BoolRef:
    facts = [_fact(f, assign) for f in clue.raw["facts"]]
    return Sum([If(f, 1, 0) for f in facts]) == 1


def _enc_either_or(clue: Clue, assign: Assign) -> BoolRef:
    a, b = (_fact(f, assign) for f in clue.raw["facts"])
    return Xor(a, b)


ENCODERS: dict[str, Callable[[Clue, Assign], BoolRef]] = {
    "direct": _enc_direct,
    "negation": _enc_negation,
    "link": _enc_link,
    "self_exclusion": _enc_self_exclusion,
    "disjunction": _enc_disjunction,
    "not_equal_any": _enc_not_equal_any,
    "implication": _enc_implication,
    "exactly_one": _enc_exactly_one,
    "either_or": _enc_either_or,
}

# True when the clue's formula never mentions an entity number, and is therefore
# invariant under relabeling.  The symmetry-breaking pin is only sound for the
# entailment-style analyses while every clue in the puzzle is invariant.
RELABEL_INVARIANT: dict[str, bool] = {t: True for t in ENCODERS}

# Required fields per type, used by the loader for shape validation.
# "ep" = endpoint mapping, "ep[]" = list of endpoints, "fact"/"fact[]" likewise.
REQUIRED_FIELDS: dict[str, dict[str, str]] = {
    "direct": {"subject": "ep", "object": "ep"},
    "negation": {"subject": "ep", "object": "ep"},
    "link": {"if": "ep", "then": "ep"},
    "self_exclusion": {"category_a": "cat", "category_b": "cat", "mapping": "map"},
    "disjunction": {"subject": "ep", "any_of": "ep[]"},
    "not_equal_any": {"subject": "ep", "none_of": "ep[]"},
    "implication": {"if": "fact", "then": "fact"},
    "exactly_one": {"facts": "fact[]"},
    "either_or": {"facts": "fact[]"},
}


# --------------------------------------------------------------------------
# canonical keys (syntactic duplication)
# --------------------------------------------------------------------------

def _pair_key(a: dict, b: dict) -> Hashable:
    return frozenset({(a["category"], a["item"]), (b["category"], b["item"])})


_KEYS: dict[str, Callable[[Clue], Hashable]] = {
    "direct": lambda c: ("EQ", _pair_key(c.raw["subject"], c.raw["object"])),
    "link": lambda c: ("EQ", _pair_key(c.raw["if"], c.raw["then"])),
    "negation": lambda c: ("NE", _pair_key(c.raw["subject"], c.raw["object"])),
    "self_exclusion": lambda c: (
        "AND",
        frozenset(("NE", frozenset({(a.category, a.item), (b.category, b.item)}))
                  for a, b in _pairs(c)),
    ),
    "not_equal_any": lambda c: (
        "AND",
        frozenset(("NE", _pair_key(c.raw["subject"], o)) for o in c.raw["none_of"]),
    ),
    "disjunction": lambda c: (
        "XOR1" if c.raw.get("exclusive") else "OR",
        frozenset(("EQ", _pair_key(c.raw["subject"], o)) for o in c.raw["any_of"]),
    ),
    "implication": lambda c: ("IMP", _fact_key(c.raw["if"]), _fact_key(c.raw["then"])),
    "exactly_one": lambda c: ("XOR1", frozenset(_fact_key(f) for f in c.raw["facts"])),
    "either_or": lambda c: ("XOR", frozenset(_fact_key(f) for f in c.raw["facts"])),
}


def normal_key(clue: Clue) -> Hashable:
    """Canonical syntactic form.  direct{A,B} and link{if:B, then:A} collapse."""
    try:
        return _KEYS[clue.type](clue)
    except KeyError as exc:
        raise UnknownClueType(clue.type) from exc


# --------------------------------------------------------------------------
# conjunct decomposition (per-atom reporting)
# --------------------------------------------------------------------------

def _conj_self_exclusion(clue: Clue, assign: Assign):
    return [(f"{a.item} -> {b.item}", _var(assign, a) != _var(assign, b))
            for a, b in _pairs(clue)]


def _conj_not_equal_any(clue: Clue, assign: Assign):
    s = _var(assign, _ep(clue.raw["subject"]))
    return [(f"{_ep(clue.raw['subject'])} != {_ep(o)}", s != _var(assign, _ep(o)))
            for o in clue.raw["none_of"]]


_CONJUNCTS: dict[str, Callable] = {
    "self_exclusion": _conj_self_exclusion,
    "not_equal_any": _conj_not_equal_any,
}


def conjuncts(clue: Clue, assign: Assign) -> list[tuple[str, BoolRef]]:
    """Labelled top-level conjuncts; a single-atom clue yields itself."""
    fn = _CONJUNCTS.get(clue.type)
    if fn:
        return fn(clue, assign)
    return [(describe(clue), constraint(clue, assign))]


# --------------------------------------------------------------------------
# description and endpoints
# --------------------------------------------------------------------------

_DESCRIBE: dict[str, Callable[[Clue], str]] = {
    "direct": lambda c: f"direct {_ep(c.raw['subject'])} = {_ep(c.raw['object'])}",
    "link": lambda c: f"link {_ep(c.raw['if'])} = {_ep(c.raw['then'])}",
    "negation": lambda c: f"negation {_ep(c.raw['subject'])} != {_ep(c.raw['object'])}",
    "self_exclusion": lambda c: (
        f"self_exclusion {c.raw['category_a']} x {c.raw['category_b']} "
        f"({len(c.raw['mapping'])} pairs)"
    ),
    "disjunction": lambda c: (
        f"disjunction {_ep(c.raw['subject'])} = "
        + " or ".join(str(_ep(o)) for o in c.raw["any_of"])
    ),
    "not_equal_any": lambda c: (
        f"not_equal_any {_ep(c.raw['subject'])} != "
        + ", ".join(str(_ep(o)) for o in c.raw["none_of"])
    ),
    "implication": lambda c: (
        f"implication if {_fact_text(c.raw['if'])} then {_fact_text(c.raw['then'])}"
    ),
    "exactly_one": lambda c: (
        "exactly_one of " + " | ".join(_fact_text(f) for f in c.raw["facts"])
    ),
    "either_or": lambda c: (
        "either_or " + " xor ".join(_fact_text(f) for f in c.raw["facts"])
    ),
}


def describe(clue: Clue) -> str:
    try:
        return _DESCRIBE[clue.type](clue)
    except KeyError as exc:
        raise UnknownClueType(clue.type) from exc


def _eps_fact(spec: dict) -> Iterator[Endpoint]:
    yield _ep(spec["subject"])
    yield _ep(spec["object"])


_ENDPOINTS: dict[str, Callable[[Clue], Iterator[Endpoint]]] = {
    "direct": lambda c: iter((_ep(c.raw["subject"]), _ep(c.raw["object"]))),
    "link": lambda c: iter((_ep(c.raw["if"]), _ep(c.raw["then"]))),
    "negation": lambda c: iter((_ep(c.raw["subject"]), _ep(c.raw["object"]))),
    "self_exclusion": lambda c: (e for pair in _pairs(c) for e in pair),
    "disjunction": lambda c: iter([_ep(c.raw["subject"])] + [_ep(o) for o in c.raw["any_of"]]),
    "not_equal_any": lambda c: iter([_ep(c.raw["subject"])] + [_ep(o) for o in c.raw["none_of"]]),
    "implication": lambda c: iter(list(_eps_fact(c.raw["if"])) + list(_eps_fact(c.raw["then"]))),
    "exactly_one": lambda c: (e for f in c.raw["facts"] for e in _eps_fact(f)),
    "either_or": lambda c: (e for f in c.raw["facts"] for e in _eps_fact(f)),
}


def endpoints(clue: Clue) -> Iterator[Endpoint]:
    try:
        return _ENDPOINTS[clue.type](clue)
    except KeyError as exc:
        raise UnknownClueType(clue.type) from exc


# --------------------------------------------------------------------------
# public encoding entry points
# --------------------------------------------------------------------------

def constraint(clue: Clue, assign: Assign) -> BoolRef:
    """The clue as a single BoolRef — the basis of every analysis."""
    try:
        encoder = ENCODERS[clue.type]
    except KeyError as exc:
        raise UnknownClueType(clue.type) from exc
    return encoder(clue, assign)


def encode_all_clues(solver: Solver, assign: Assign, puzzle) -> None:
    """Kept for callers that just want the constraints pushed into a solver."""
    for clue in puzzle.clues:
        solver.add(constraint(clue, assign))
