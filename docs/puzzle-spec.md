# Puzzle Framework Specification

## Overview

Each puzzle is a zebra-logic deduction grid with D categories of N items each.
The player solves by elimination and cross-referencing, then submits a D-tuple answer via select boxes.

---

## Dimensions

D and N are independent — nothing couples the number of categories to the number
of items, so the ladder is finer than three rungs:

| D×N | Grid size | Active blocks | Active cells | Minimal clues (typical) |
|-----|-----------|---------------|--------------|-------------------------|
| 3×3 | 6×6       | 3             | 27           | 4–6                     |
| 3×4 | 8×8       | 3             | 48           | 6–8                     |
| 4×4 | 12×12     | 6             | 96           | 7–12                    |
| 4×5 | 15×15     | 6             | 150          | 11–16                   |
| 5×4 | 16×16     | 10            | 160          | 12–18                   |
| 5×5 | 20×20     | 10            | 250          | 15–20                   |

Grid is `(D-1)N × (D-1)N`; active blocks are `C(D,2)`; active cells are
`C(D,2) × N²`. The clue counts are measured minimal sets using only
`direct`/`negation`; richer clue types bring them down.

### Compact labels at 5D

With 16–20 columns, items need short labels (≤3 chars). Prefer a **two-character
alphanumeric token** per category over a glyph:

| Category | Token | Items |
|----------|-------|-------|
| Replica  | `r`   | `r1 r2 r3 r4 r5` |
| Digest   | `d`   | `d1 d2 d3 d4 d5` |
| Epoch    | `e`   | `e1 e2 e3 e4 e5` |
| Key      | `k`   | `k1 k2 k3 k4 k5` |
| Stream   | `s`   | `s1 s2 s3 s4 s5` |

Tokens are typeable and speakable, and — unlike glyphs — they can be reused
verbatim as `<option value>` attributes, so the grid and the answer widget
cannot drift apart. Keep the readable name in the option *text*:

```html
<option value="k4">k4 — r.sato</option>
```

Pair a 5D grid with a **registry panel** in the same column: a plain
`panel.html` holding a token → name table. It removes the memory load and reads
as an in-world lookup table rather than a legend.

Glyph prefixes (`◆ ▲ ● ■ ✦`) still render, but they cannot be typed and make the
answer values illegible in the page source.

---

## Grid Topology

The grid is divided into `(D-1)²` blocks, each of size `N×N`.

### 3 dimensions (6×6)

```
 A | B
---+---
 C | .
```

- Active blocks: A, B, C (3 = C(3,2))
- Disabled blocks: 1 (bottom-right corner)

### 4 dimensions (12×12)

```
 A | B | C
---+---+---
 D | E | .
---+---+---
 F | . | .
```

- Active blocks: A, B, C, D, E, F (6 = C(4,2))
- Disabled blocks: 3 (lower-right triangle)

### 5 dimensions (20×20)

```
 A | B | C | D
---+---+---+---
 E | F | G | .
---+---+---+---
 H | I | . | .
---+---+---+---
 J | . | . | .
```

- Active blocks: A–J (10 = C(5,2))
- Disabled blocks: 6 (lower-right triangle)

### Disable rule

A block at position `(row_idx, col_idx)` (0-indexed) is disabled when:

```
row_idx + col_idx >= D - 1
```

Disabled blocks render as dark empty cells with no interaction.

---

## Category-to-Block Mapping

Pick a grid order `G1 … GD` for the puzzle's categories — it does not have to be
the order they appear in the YAML. Then:

- **Column groups** (left to right): `G1, G2, …, G(D-1)`
- **Row groups** (top to bottom): `GD, G(D-1), …, G2` — **reverse order**

The reverse row order is load-bearing, not a style choice. The include disables a
block at `row_idx + col_idx >= number of column groups`, so listing the rows
forward puts a category against itself in an *active* block and leaves other
pairs uncrossed. Listing them in reverse makes the active blocks cover each of
the `C(D,2)` category pairs exactly once, which is the property the checker
enforces (`E407`).

Each active block represents a pairwise relationship between two different
categories. The disabled blocks sit where a category would cross itself.

### Example: 3 categories, grid order Process, Token, Resource

- Columns: Process, Token
- Rows: Resource, Token  (reverse of G3, G2)
- Block (0,0): Resource × Process — active
- Block (0,1): Resource × Token — active
- Block (1,0): Token × Process — active
- Block (1,1): Token × Token — disabled

Three active blocks, three category pairs, no self-pairing.

### Example: 4 categories, grid order Process, Token, Resource, Host

- Columns: Process, Token, Resource
- Rows: Host, Resource, Token  (reverse of G4, G3, G2)

Applying `row_idx + col_idx >= 3`:

| | Process | Token | Resource |
|---|---|---|---|
| **Host** | active | active | active |
| **Resource** | active | active | disabled |
| **Token** | active | disabled | disabled |

Six active blocks covering all six pairs: Host×Process, Host×Token,
Host×Resource, Resource×Process, Resource×Token, Token×Process. ✓

Listing the rows forward (Token, Resource, Host) instead gives an active
Token×Token block and never crosses Host with Token or Resource.

---

## Cell States

Each active cell cycles through 3 states on click:

| State | Class      | Label | Meaning      |
|-------|------------|-------|--------------|
| 0     | (none)     | (empty) | Unknown    |
| 1     | `is-x`    | ✕     | Eliminated   |
| 2     | `is-check` | ✓    | Confirmed    |

Cell state is persisted in localStorage keyed by `mutext-grid-{pathname}`.

---

## Answer Input Component

The answer is a D-tuple. Each dimension is a `<select>` element populated with that category's items.

### Structure

```html
<div data-puzzle-answer="parser, token-beta, /models">
  <div class="flex flex-wrap items-center gap-3">
    <select data-answer-dim="0">
      <option value="">— process —</option>
      <option value="parser">parser</option>
      <option value="crawler">crawler</option>
      <option value="renderer">renderer</option>
    </select>
    <select data-answer-dim="1">
      <option value="">— token —</option>
      <option value="token-alpha">token-alpha</option>
      <option value="token-beta">token-beta</option>
      <option value="token-gamma">token-gamma</option>
    </select>
    <select data-answer-dim="2">
      <option value="">— resource —</option>
      <option value="/cache">/cache</option>
      <option value="/logs">/logs</option>
      <option value="/models">/models</option>
    </select>
    <button class="button-primary" type="button" data-fake-action="SUBMIT">SUBMIT</button>
  </div>
</div>
```

### Validation logic

The JS iterates all `[data-puzzle-answer]` elements on the page, wiring each independently:

```js
document.querySelectorAll("[data-puzzle-answer]").forEach((answerEl) => {
  const expected = answerEl.getAttribute("data-puzzle-answer")
    .split(",").map(s => s.trim().toLowerCase());
  const submitBtn = answerEl.querySelector('[data-fake-action="SUBMIT"]');
  const selects = answerEl.querySelectorAll("select[data-answer-dim]");
});
```

Validation is **exact positional match** against the select values:

```js
const selected = Array.from(selects).map(s => s.value.trim().toLowerCase());
const correct = expected.length === selected.length
  && expected.every((val, i) => val === selected[i]);
```

### Multi-stage chapters

An answer block may name the section it unhides:

```html
<div data-puzzle-answer="r3, d2, e4, k1, s5" data-reveal="#lore-reveal-2">
```

`data-reveal` defaults to `#lore-reveal`, so every single-stage chapter is
unaffected. Put the second stage's answer block *inside* the first stage's
reveal section: it is then invisible — and unspoilable — until stage one is
solved, and the NEXT INCIDENT link lives in the second reveal so the chapter
gates on both.

### Behavior

- On correct: button shows "CORRECT" with `button-correct` class, confetti fires, the reveal target unhides
- On incorrect: button shows "INCORRECT" with `button-incorrect` class for 3s, then resets
- Multiple answer sections per page are supported independently

---

## Page Layout

### Small screens (stacked, single column)

```
┌─────────────────────────────┐
│           LORE              │
├─────────────────────────────┤
│           CLUES             │
├─────────────────────────────┤
│          MESSAGES           │
├─────────────────────────────┤
│        PUZZLE GRID          │
│                             │
│                             │
│              [clear board]  │
├─────────────────────────────┤
│       ANSWER INPUT          │
│   [select] [select] [...]   │
│   [submit]                  │
├─────────────────────────────┤
│    LORE END (after solve)   │
└─────────────────────────────┘
```

### Large screens (two-column)

```
┌──────────────────────────────────────────────┐
│                    LORE                       │
├──────────────┬───────────────────────────────┤
│              │                               │
│   CLUES      │        PUZZLE GRID            │
│              │                               │
├──────────────┤                               │
│              │                               │
│  MESSAGES    ├───────────────────────────────┤
│              │       ANSWER INPUT            │
│              │   [select] [select] [...]     │
│              │   [submit]                    │
├──────────────┴───────────────────────────────┤
│              LORE END (after solve)          │
└──────────────────────────────────────────────┘
```

### Implementation

The layout uses existing includes:

```liquid
{% include lore-block.html %}
  ...narrative...
{% include lore-block_end.html %}

{% include puzzle-grid.html %}
  {% include puzzle-col.html %}
    (clues panel)
    (messages panel)
  {% include puzzle-col_end.html %}
  {% include puzzle-col.html %}
    (grid panel with zebra-table include)
    (answer input panel)
  {% include puzzle-col_end.html %}
{% include puzzle-grid_end.html %}

<section id="lore-reveal" class="mt-5 hidden">
  ...post-solve content...
</section>
```

- `puzzle-grid.html` = `<section class="grid gap-5 lg:grid-cols-[minmax(14rem,0.7fr)_minmax(0,1.3fr)]">`
- `puzzle-col.html` = `<div class="space-y-5">`
- On mobile: columns stack vertically (left column first, then right)
- On `lg:` breakpoint: side-by-side with left column narrower

---

## Zebra Table Include

File: `_includes/zebra-table.html`

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `cols_a`  | yes      | Pipe-delimited items for column group 1 |
| `cols_b`  | yes      | Pipe-delimited items for column group 2 |
| `cols_c`  | no       | Pipe-delimited items for column group 3 (4D+) |
| `rows_a`  | yes      | Pipe-delimited items for row group 1 |
| `rows_b`  | yes      | Pipe-delimited items for row group 2 |
| `rows_c`  | no       | Pipe-delimited items for row group 3 (4D+) |

### Usage

3D puzzle:
```liquid
{% include zebra-table.html
   cols_a="parser|crawler|renderer"
   cols_b="/cache|/logs|/models"
   rows_a="token-alpha|token-beta|token-gamma"
   rows_b="/cache|/logs|/models"
%}
```

4D puzzle (rows in reverse grid order — host, res, tok):
```liquid
{% include zebra-table.html
   cols_a="proc-A|proc-B|proc-C|proc-D"
   cols_b="tok-1|tok-2|tok-3|tok-4"
   cols_c="res-W|res-X|res-Y|res-Z"
   rows_a="host-α|host-β|host-γ|host-δ"
   rows_b="res-W|res-X|res-Y|res-Z"
   rows_c="tok-1|tok-2|tok-3|tok-4"
%}
```

### Disabled block rendering

- Active cells: `<button class="zebra-cell" data-grid-cell>` — interactive
- Disabled cells: empty `<td>` with `bg-slate-950/80` — no button, no interaction
- Group separators: `border-l-2 border-l-slate-600` (vertical) and `border-t-2 border-t-slate-600` (horizontal)

### 5D support

The include accepts `cols_d`/`rows_d` for 5D grids. The disable rule generalizes: disabled when `row_group_idx + col_group_idx >= num_col_groups`.

5D example (compact labels, rows reversed):
```liquid
{% include zebra-table.html
   cols_a="◆1|◆2|◆3|◆4|◆5"
   cols_b="▲a|▲b|▲c|▲d|▲e"
   cols_c="●α|●β|●γ|●δ|●ε"
   cols_d="■Ⅰ|■Ⅱ|■Ⅲ|■Ⅳ|■Ⅴ"
   rows_a="✦1|✦2|✦3|✦4|✦5"
   rows_b="■Ⅰ|■Ⅱ|■Ⅲ|■Ⅳ|■Ⅴ"
   rows_c="●α|●β|●γ|●δ|●ε"
   rows_d="▲a|▲b|▲c|▲d|▲e"
%}
```

---

## Puzzle Post Data Format

Each puzzle is a Jekyll post in `_posts/` with this structure:

### Front matter

```yaml
---
title: "INC-XXXX Title"
description: "One-line description for meta tags"
permalink: /puzzles/NNN-slug.html
---
```

The post date in the filename sets archive order; chapter N is
`2026-05-(14+N)`. Every puzzle post is paired with `checker/puzzles/NNN-slug.yaml`,
which names the post and carries each clue's prose. The checker fails the build
if the two disagree — see `docs/sat-checker.md`.

### Required sections

1. **Lore intro** — narrative framing (chapter, label)
2. **Clues panel** — numbered evidence list
3. **Messages panel** — 2–3 chat messages from Bob explaining the grid
4. **Grid panel** — incident metadata + `zebra-table.html` include + clear button
5. **Answer panel** — question text + select boxes + submit button
6. **Lore reveal** — hidden section shown after correct answer

### Answer encoding

The correct answer is stored as a `data-puzzle-answer` attribute on a wrapper div.
Value is comma-separated, positional, case-insensitive:

```html
<div data-puzzle-answer="parser, token-beta, /models">
```

---

## JavaScript Contract

File: `assets/js/main.js`

### Grid system (already generic)

- Queries all `[data-grid-cell]` on the page
- State cycles: 0 → 1 → 2 → 0 (empty → ✕ → ✓)
- Persistence: `localStorage["mutext-grid-" + pathname]` — array of state integers
- Clear: `[data-clear-grid]` button resets all cells with confirmation

### Answer validation

- Iterates all `[data-puzzle-answer]` elements, wires each independently
- Validates `select[data-answer-dim]` values by exact positional match
- On correct: adds `button-correct` class, fires `spawnConfetti()`, unhides `#lore-reveal`
- On incorrect: shows `button-incorrect` for 3s, then resets

### No puzzle-specific code

The JS is fully generic. All puzzle-specific data lives in the HTML (grid structure, answer value, category items in selects).

---

## Stored state

Two keys, both per-browser and both optional — nothing the site does depends on
them being present.

| Key | Holds | Written when |
|---|---|---|
| `mutext-grid-<pathname>` | the grid marks on that page, as a positional array | any cell is clicked |
| `mutext-solved` | the slugs of closed incidents, e.g. `["005-starvation"]` | a chapter's **final** answer block is solved |

`mutext-solved` stores slugs rather than pathnames so a local build and the
deployed site (which carries a `/mutext` baseurl) agree. A two-stage chapter is
recorded only once its last answer block is solved, so solving chapter 10's grid
without the archive query does not close it.

The archive and the operator panel render from it: rows carry `data-chapter`
plus a `[data-solved-badge]`, the panel carries `[data-progress-count]`,
`[data-progress-bar]` and a `[data-clear-progress]` reset. All of it is wired
generically in `main.js` — there is still no per-chapter JavaScript.

## Constraints

- No note-taking required — all deduction must be trackable on the grid alone
- No backend — all validation is client-side
- Answer is visible in page source (acceptable for prototype)
- Grid marks and closed-incident state persist via localStorage (see above); a
  reveal is not persisted, so returning to a solved chapter means solving it again
- Each puzzle page must be self-contained (no shared state between puzzles)

---

## Axioms

### Axiom I — One match per row and column in every block

For each N×N block, exactly one ✓ must appear in every row and exactly one ✓ in every column. All other cells are ✕.

Valid (3×3 block):

```
✓ | ✕ | ✕
--+---+---
✕ | ✕ | ✓
--+---+---
✕ | ✓ | ✕
```

Valid (3×3 block):

```
✕ | ✕ | ✓
--+---+---
✓ | ✕ | ✕
--+---+---
✕ | ✓ | ✕
```

Invalid — row 1 has two ✓:

```
✓ | ✓ | ✕
--+---+---
✕ | ✕ | ✓
--+---+---
✕ | ✕ | ✕
```

Invalid — column 1 has two ✓:

```
✓ | ✕ | ✕
--+---+---
✓ | ✕ | ✕
--+---+---
✕ | ✕ | ✓
```

Invalid — row 3 has no ✓:

```
✓ | ✕ | ✕
--+---+---
✕ | ✓ | ✕
--+---+---
✕ | ✕ | ✕
```

Invalid — column 2 has no ✓:

```
✓ | ✕ | ✕
--+---+---
✕ | ✕ | ✓
--+---+---
✕ | ✕ | ✕
```

This constraint holds for every active block independently. A valid solution is a permutation matrix in each block.

### Axiom II — Answer dimensionality matches puzzle dimensionality

The answer is always a D-tuple for a D-dimensional puzzle:

- 3D puzzle → 3 selects (one value per category)
- 4D puzzle → 4 selects (one value per category)
- 5D puzzle → 5 selects (one value per category)

---

## Examples

| Chapter | Categories | D×N | Clues |
|---|---|---|---|
| 001 tutorial | process, token, resource | 3×3 | 5 encoded + 1 narrative |
| 002 the lockup | process, lock, call target | 3×3 | 5 |
| 003 race condition | process, queue, result | 3×3 | 5 encoded over 6 items |
| 004 cache poisoning | tenant, edge, route | 3×3 | 5 encoded + 1 narrative |

---

## Authoring order

Each chapter is written in this order, and never out of it — the puzzle is made
to work before a word of prose is written around it.

1. **`docs/puzzles/NNN-slug.md`** — the design doc. Lore start; grid
   instantiation (D, N, grid order, the exact include line, a category → token →
   option-text table); the identification rule that singles out the answer row
   and where the player meets it; entities; clues in final wording; the solve
   path; the answer tuple; continuity (what the chapter consumes from
   `_data/evidence.yml` and what it plants); the reveal.
2. **`checker/puzzles/NNN-slug.yaml`** — categories, answer, clues with
   `post_number` and `prose`. `checker/make_puzzle.py` turns an intended
   solution into a minimal clue set.
3. **`npm run check:puzzles`** until green. Iterate here, never in the post.
4. **Back-port** any clue change into the design doc.
5. **`_posts/2026-05-DD-slug.md`** — prose copied verbatim from the YAML, the
   include line pasted from the design doc.
6. **Ledger** — add or consume `_data/evidence.yml` entries. Every string two
   chapters must agree on is rendered from there, never typed twice.
7. **`npm run check:puzzles`** again, now with the post lint, then load the page
   and solve it once.
8. **Link the chain** — point the previous chapter's NEXT INCIDENT at this one.

### Things that bite

- **Never change a shipped grid's shape.** Grid marks are a positional array in
  `localStorage["mutext-grid-" + pathname]`, so reordering items, or changing D
  or N, silently re-maps a returning player's marks onto the wrong cells. If a
  shipped grid really must change, change the permalink. While authoring, hit
  CLEAR BOARD after every edit.
- **One clear button per page.** `main.js` wires `[data-clear-grid]` with
  `querySelector`, not `querySelectorAll`, and the button is emitted by the grid
  include — so a page with two grids only clears the first.
- **One grid's marks per pathname.** Two grids on one page share a single saved
  array.
