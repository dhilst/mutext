# SAT Checker Specification

## Purpose

Verify that every puzzle is:

1. **Satisfiable** — the clues do not contradict each other
2. **Correct** — the solution matches the expected answer
3. **Unique** — exactly one solution exists

## Encoding Strategy

### Variables

Each item gets an integer variable representing which "entity" (0..N-1) it belongs to. Two items from different categories are matched iff they share the same entity number.

```python
assign[category_name][item_name] = Int(...)
```

For a 3D puzzle with 3 items per category, this creates 9 integer variables total.

### Axiom I — Permutation matrix per block

Within each category, all items map to distinct entities in range `[0, N)`:

```python
for each category:
    Distinct(all variables in category)
    each variable >= 0, < N
```

### Symmetry breaking

Entity numbers are arbitrary labels. To eliminate equivalent re-numberings, the first category's items are pinned to canonical order:

```python
assign[first_category][item_0] == 0
assign[first_category][item_1] == 1
...
```

This does not restrict the solution space — it only fixes the labeling.

---

## Clue Types

| Type | Meaning | Z3 |
|------|---------|-----|
| `direct` | "X has Y" | `assign[catA][X] == assign[catB][Y]` |
| `negation` | "X not Y" | `assign[catA][X] != assign[catB][Y]` |
| `conditional` | "whoever has Y also has Z" | `assign[catA][Y] == assign[catB][Z]` |
| `self_exclusion` | "no X maps to its own Y" | per-pair `!=` from a mapping dict |

All clue types reduce to equality or inequality between entity-assignment variables.

---

## Verification Procedure

```
1. Build variables + axioms
2. Encode all clues as Z3 assertions
3. solver.check() → must be SAT
4. Extract model → all answer items must share the same entity number
5. Block the found model, re-check → must be UNSAT (uniqueness)
```

### Uniqueness check

After finding the first model, add a constraint that at least one variable must differ:

```python
Or(var != model_value for all variables)
```

If the solver finds another model, the puzzle is under-constrained.

---

## Puzzle Definition Format (YAML)

```yaml
name: "INC-0001 Tutorial"
dimensions: 3
size: 3

categories:
  - name: process
    items: [parser, crawler, renderer]
  - name: token
    items: [token-alpha, token-beta, token-gamma]
  - name: resource
    items: [/cache, /logs, /models]

answer:
  process: parser
  token: token-beta
  resource: /models

clues:
  - type: negation
    subject: { category: process, item: parser }
    object: { category: token, item: token-alpha }

  - type: conditional
    if: { category: resource, item: /cache }
    then: { category: token, item: token-gamma }

  - type: direct
    subject: { category: process, item: crawler }
    object: { category: resource, item: /cache }

  - type: self_exclusion
    category_a: process
    category_b: call_target
    mapping:
      P1: "→P1"
      P2: "→P2"
      P3: "→P3"
```

---

## CLI Usage

```bash
cd checker
uv run check_puzzle.py puzzles/001-tutorial.yaml
uv run check_puzzle.py puzzles/                    # all puzzles
uv run check_puzzle.py puzzles/ --verbose           # show full solution
```

## Output

```
=== INC-0001 Tutorial (3×3) ===
Categories: process(3), token(3), resource(3)
Clues: 5

[1/3] Solving... SAT ✓
[2/3] Answer check... MATCH ✓
[3/3] Uniqueness... UNIQUE ✓

PASS
```

---

## File Structure

```
checker/
├── pyproject.toml
├── puzzles/
│   ├── 001-tutorial.yaml
│   └── 002-the-lockup.yaml
├── zebra_checker/
│   ├── __init__.py
│   ├── loader.py
│   ├── encoder.py
│   ├── clues.py
│   └── verifier.py
└── check_puzzle.py
```

## Adding New Puzzles

1. Create `checker/puzzles/NNN-slug.yaml` following the schema above
2. Run `cd checker && uv run check_puzzle.py puzzles/NNN-slug.yaml`
3. All three checks must pass before the puzzle ships
