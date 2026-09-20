# Puzzle Checker Specification

The checker answers one question: **does this puzzle deserve to ship?**

That means more than "is it solvable". A puzzle passes only when it has exactly
one solution, that solution is the declared answer, every clue earns its place,
and the page the player actually reads agrees with the model the solver checked.

```bash
npm run check                  # everything below, in order — what CI runs
npm run check:puzzles          # strict, with the post lint
npm run check:continuity       # the story-arc guard
npm run test:puzzles           # the checker's own unit tests

cd checker
uv run check_puzzle.py puzzles/005-starvation.yaml -v
uv run check_puzzle.py puzzles --strict --posts ../_posts
uv run check_puzzle.py puzzles --json > report.json
```

---

## Encoding

One integer variable per item. Two items are matched iff they hold the same
entity number.

```python
assign[category][item] = Int(f"{category}__{item}")
```

**Axiom I — permutation per category.** Every item of a category takes a
distinct entity number in `[0, N)`. This is the grid rule "one ✓ per row and per
column in every block", expressed once instead of per block.

**Symmetry breaking.** Entity numbers are arbitrary labels, so the first
category is pinned to `0..N-1`. That is a relabeling, not a restriction: it
picks one representative per orbit. It is required for uniqueness to mean
anything (otherwise every solution has `N!` renamings) and it shrinks the model
space by a factor of `N!` — at 5×5, 207k models instead of 24.9M.

The pin is only sound while every clue formula is **relabeling-invariant**, i.e.
compares assignment variables and never mentions an entity number. Every clue
type listed below is. `clues.RELABEL_INVARIANT` records this per type; if a
position-sensitive type is ever added, the analyses fall back to unpinned axioms
and say so (`W310`). `tests/test_analysis.py::test_pin_does_not_change_verdicts`
runs every check both ways and asserts the findings are identical.

---

## Clue types

| Type | Meaning | Encoding |
|------|---------|----------|
| `direct` | X is Y | `a == b` |
| `negation` | X is not Y | `a != b` |
| `link` | whoever has Y also has Z | `a == b` |
| `self_exclusion` | no X maps to its own Y | pairwise `!=` from a mapping |
| `disjunction` | X is A or B | `Or(...)`, `exclusive: true` adds at-most-one |
| `not_equal_any` | X is none of A, B, C | `And(...)` of `!=` |
| `implication` | if fact P then fact Q | `Implies(P, Q)` |
| `exactly_one` | exactly one of these facts holds | `Sum(If(f,1,0)) == 1` |
| `either_or` | exactly one of two facts holds | `Xor(a, b)` |

`conditional` is a deprecated alias for `link` and warns (`W315`). It always
encoded an equality, never an implication — `implication` is the real thing.

A *fact* (used by `implication`, `exactly_one`, `either_or`) is
`{subject, object, negated?}`.

`disjunction` is the type worth reaching for first on 4D/5D puzzles: it is the
only one that does not decide a cell outright, so it adds deduction depth
without adding clue count.

**Not supported on purpose:** ordering predicates (`left_of`, `position`). They
mention entity numbers, break relabeling invariance, and would silently
invalidate the pinned analyses. A category whose *items* are ordered
(`P0..P3`, `03:10`, `611s`) needs no such operator — the order is read off the
label, and plain `direct`/`negation` clues do the work.

---

## What is checked

### Core

| Code | Meaning |
|---|---|
| `E201` | no solution — the clues contradict each other |
| `E202` | the declared answer items are not one row of the solution |
| `E204` | more than one solution; the second is printed |
| `E205` | the solver returned `unknown` (timeout) — **unverified is not passed** |

### Clue quality

| Code | Severity | Meaning |
|---|---|---|
| `E301` | error | **vacuous** — the grid rules alone already imply the clue |
| `E302` | error | **contradictory** — this one clue can never hold |
| `E303` | error | **duplicate** — identical canonical form as an earlier clue |
| `E304` | error | **duplicate** — logically equivalent to an earlier clue |
| `E313` | error | `self_exclusion` with the same category on both sides |
| `W305` | warn | **redundant** — implied by the other clues, and droppable |
| `W306` | warn | a conjunct inside a multi-atom clue is vacuous |
| `W308` | warn | the clue set is not minimal; names the droppable clues |
| `W311` | warn | this clue is literally one conjunct of another |
| `W314` | warn | `keep_redundant` on a clue that is load-bearing |
| `I305` | info | a redundant clue kept deliberately, with its reason |
| `I307` | info | the minimal sufficient subset |

For a puzzle with a unique solution, "removable" and "entailed by the other
clues" are the same property, and the checker computes both and reports a
disagreement (`W309`) because one can only mean a non-unique puzzle or an
encoder bug.

Mutual entailment means several clues in an over-determined cluster are each
individually removable while only some can go together. So `W305` is raised for
the clues the minimisation actually drops; the others are named in the `I307`
line instead.

### Post ↔ page sync

| Code | Meaning |
|---|---|
| `E402` | an evidence item is neither encoded nor declared `narrative_only` |
| `E403` | the prose in the post differs from the `prose:` in the YAML |
| `E404` | a `post_number` is out of range, claimed twice, or also narrative-only |
| `E405` | `data-puzzle-answer` disagrees with the answer (`W405`: case only) |
| `E406` | the `<select>` options are not the category items, in order |
| `E407` | the grid blocks do not cover each category pair exactly once |
| `E409` | the declared post file does not exist |
| `W404` | evidence numbering is not contiguous |
| `W408` | the permalink does not contain the puzzle slug |
| `E411` | a chat message describes the grid wrongly — calls a row a column, or the reverse |
| `E412` | a `Format:` hint in a message disagrees with the dropdown order |

`E411` exists because INC-0001 shipped telling the player "the left three
columns are tokens" when the columns were processes and the tokens were rows.
The check only fires on a sentence that talks about one axis and names a
category living exclusively on the other, so a category on both axes — which is
normal, the shared category appears twice — is never flagged.

**Grid validation is structural.** `zebra-table.html` disables a block when
`row_group + col_group >= number of column groups`, so the covering rule is what
matters, not which argument holds which category:

```
cols = G1, G2, …, G(D-1)
rows = GD, G(D-1), …, G2        ← reverse order
```

Listing the rows forward puts a category against itself and leaves pairs
uncrossed. See `docs/puzzle-spec.md`.

---

## Severity policy

An **error** fails the build. A **warning** fails it under `--strict`, which is
what `npm run check:puzzles` and CI use. Warnings exist so an author can see a
problem mid-authoring without being blocked; nothing reaches `master` with one.

A clue that is genuinely redundant and genuinely wanted is declared, not
silenced:

```yaml
  - type: negation
    post_number: 3
    prose: "P2 does not hold L3."
    keep_redundant: true
    note: "Andy's first real incident: the lock assignment is restated so the
      player can close the cycle by elimination instead of assuming it."
```

That turns `W305` into `I305` and excludes the clue from `W308`'s count. Put the
reason in `note:` — the marker is a claim about the player's experience, so it
should read like one. A marker on a clue that is *not* redundant warns (`W314`),
so it cannot rot.

---

## Puzzle file format

```yaml
name: "INC-0004 Cache Poisoning"
dimensions: 3
size: 3

post:
  path: _posts/2026-05-18-cache-poisoning.md
  panel_title: evidence          # 001 uses "clues"
  answer_order: [tenant, edge, route]   # select order; defaults to answer order
  narrative_only: [6]            # evidence items that carry no constraint

categories:
  - name: tenant
    items: ["helios", "orion", "atlas"]
  ...

answer:
  tenant: atlas
  edge: edge-02
  route: /session

clues:
  - type: negation
    post_number: 1               # int, or a list when one clue covers two items
    prose: "The poisoned `/session` route did not originate from `edge-01`."
    subject: { category: route, item: "/session" }
    object: { category: edge, item: "edge-01" }
```

Omit the `post:` block and the sync lint is skipped (`I401`).

### narrative_only

An evidence item the encoding does not carry — a Nix fragment, one of Bob's
asides, a count the metadata already states. Either form works:

```yaml
  narrative_only: [6]                     # declared, unchecked

  narrative_only:                         # declared and checked
    6: "A malformed telemetry line appears in the edge-03 log."
```

Prefer the mapping. A bare list only asserts that the item is *allowed* to be
unencoded; the post then becomes the item's only source, and an edit to it
drifts silently — which is how chapter 16's "renewed at 02:44" survived a
change to 02:14 in three other places. The mapping pins the text the same way
an encoded clue's `prose` is pinned, and all eleven declarations now use it.

Keys are unquoted integers. That is the one place in these files where a bare
number is wanted: elsewhere, quote everything (`"08:05"` is parsed as an
integer otherwise).

### Authoring rules the checker enforces

- **Quote every item.** PyYAML turns `08:05` into an integer and `no`/`on`/`off`
  into booleans, which silently breaks the item lookup.
- **Item strings are byte-identical** in the YAML, the grid labels, the
  `<option value>` attributes and `data-puzzle-answer`.
- **No commas in item names** — `data-puzzle-answer` is comma-split (`E112`).
- **No item name reused across categories** — it makes prose and the answer
  tuple ambiguous (`E104`; `allow_duplicate_items: true` to override).
- `prose:` must match the post **verbatim**; it is compared after Unicode
  normalisation and whitespace collapsing, and nothing else.

---

## Authoring a new puzzle

```bash
cd checker
uv run make_puzzle.py spec.yaml --prefer-direct 0.3 --tries 24
```

`make_puzzle.py` takes the categories and the intended solution, builds a
candidate pool (every consistent `direct`/`negation` pair, plus any clues you
hand it under `pool:`), picks clues until the solution is unique, then deletes
every clue it can. It prints a minimal clue list ready to paste and fill in with
prose.

`--prefer-direct` is the difficulty dial: a lower share of positive clues means
more clues and more elimination work. A 4×4 lands around 7–10 clues, a 5×5
around 15–20.

Then: write the clues' prose, write the post, and run

```bash
npm run check:puzzles
```

Continuity is checked separately, because it is about the arc rather than any
one puzzle:

```bash
cd checker
uv run check_continuity.py
```

It fails if a ledger entry is never rendered from the ledger, if the chapter that
owns an entry does not render it, if HORUS is named before chapter 10, if the
NEXT INCIDENT chain does not reach every chapter, or if meta-language
("categories", "the grid", "clue 7", "5D") appears in player-facing prose.

After a build, check what Liquid actually rendered:

```bash
cd checker
uv run check_rendered_grid.py ../_site/puzzles/008-split-brain.html \
    --puzzle puzzles/008-split-brain.yaml
```

---

## CLI

```
check_puzzle.py [PATH ...]            files and/or directories (default: puzzles)
  -v, --verbose      print the solution and INFO findings
  -q, --quiet        only the summary
      --json         machine-readable report on stdout
      --strict       treat warnings as errors
      --checks LIST  core,vacuity,duplication,redundancy,minimality,postsync
      --skip LIST    inverse of --checks
      --no-deep-dup  skip the pairwise semantic duplication pass
      --posts DIR    posts directory (default: <repo>/_posts)
      --no-post-lint skip the post <-> yaml lint
      --timeout MS   per-solver-call timeout (default 10000)
```

Exit codes: `0` pass, `1` error, `2` usage or parse failure, `3` solver timeout.

Findings print as `CODE  check  file:line`, a message, and a `fix:` hint, so they
are greppable and stable.

---

## Cost

A 14-clue 5×5 puzzle is roughly 170 solver calls and well under 1.5 s. Measured:
a synthetic 5×5 with 55 clues took 220 calls in 0.69 s, and minimisation 0.36 s.
The only superlinear pass is pairwise semantic duplication (`C(n,2)`), which has
`--no-deep-dup` and an automatic skip above a pair limit.

---

## Layout

```
checker/
  check_puzzle.py          CLI shim
  make_puzzle.py           authoring aid: solution -> minimal clue set
  check_rendered_grid.py   verify a built page's grid structure
  check_continuity.py      ledger, reveal order, link chain, meta-language
  puzzles/                 one YAML per chapter
  tests/                   pytest; fixtures/ holds one puzzle per failure mode
  zebra_checker/
    model.py       Puzzle, Category, Clue, Endpoint, PostRef
    errors.py      schema errors with file:line and suggestions
    loader.py      YAML -> Puzzle, full validation
    encoder.py     variables and axioms as pure values
    clues.py       encoding, canonical keys, conjuncts, descriptions
    analysis.py    vacuity, contradiction, duplication, entailment, minimality
    postlint.py    post <-> yaml sync
    findings.py    Finding and the code table
    report.py      text and JSON rendering, exit codes
    verifier.py    orchestration
    cli.py         argument parsing
```
